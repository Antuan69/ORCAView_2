/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the QtWebChannel module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

var QWebChannel = function(transport, initCallback)
{
    if (typeof transport !== 'object' || typeof transport.send !== 'function') {
        console.error("The QWebChannel transport object is missing a send function.");
        return;
    }

    var channel = this;
    this.transport = transport;

    this.send = function(data)
    {
        if (typeof data !== 'string') {
            data = JSON.stringify(data);
        }
        channel.transport.send(data);
    }

    this.transport.onmessage = function(message)
    {
        var data = message.data;
        if (typeof data === 'string') {
            data = JSON.parse(data);
        }
        channel.handleMessage(data);
    }

    this.objects = {};

    this.handleMessage = function(data)
    {
        if (data.type === QWebChannel.Signal) {
            channel.handleSignal(data);
        } else if (data.type === QWebChannel.Response) {
            channel.handleResponse(data);
        } else if (data.type === QWebChannel.PropertyUpdate) {
            channel.handlePropertyUpdate(data);
        } else if (data.object) {
            channel.handleObjectInitialization(data);
        } else {
            console.error("invalid message received:", JSON.stringify(data));
        }
    }

    this.handleObjectInitialization = function(data)
    {
        var objectName;
        for (objectName in data) {
            if (!data.hasOwnProperty(objectName)) {
                continue;
            }
            var object = new QObject(objectName, data[objectName], channel);
        }
    }

    this.handleSignal = function(message)
    {
        var object = channel.objects[message.object];
        if (object) {
            object.signalEmitted(message.signal, message.args);
        } else {
            console.warn("received signal for unknown object", message.object);
        }
    }

    this.handleResponse = function(message)
    {
        var object = channel.objects[message.object];
        if (!object) {
            console.warn("received response for unknown object", message.object);
            return;
        }
        object.responseReceived(message.id, message.data);
    }

    this.handlePropertyUpdate = function(message)
    {
        for (var i in message.data) {
            var data = message.data[i];
            var object = channel.objects[data.object];
            if (object) {
                object.propertyUpdate(data.signal, data.args);
            } else {
                console.warn("received property update for unknown object", data.object);
            }
        }
    }

    this.debug = function(message)
    {
        this.send({type: QWebChannel.Debug, data: message});
    };

    this.send({type: QWebChannel.Initialize});

    if (initCallback) {
        initCallback(this);
    }
};

QWebChannel.Initialize = 0;
QWebChannel.Signal = 1;
QWebChannel.Response = 2;
QWebChannel.PropertyUpdate = 3;
QWebChannel.Debug = 4;

var QObject = function(name, data, webChannel)
{
    this.__id__ = name;
    webChannel.objects[name] = this;

    this.__objectSignals__ = {};
    this.__propertyCache__ = {};

    var object = this;

    // __properties__ is an array of property names
    var propertyNames = data.properties || [];
    var property;
    for (var i = 0; i < propertyNames.length; i++) {
        property = propertyNames[i];
        // initial value is stored in propertyCache
        object[property] = data.properties[property];
        object.__propertyCache__[property] = object[property];

        // register setter
        if (data.properties[property].writeable) {
            Object.defineProperty(object, property, {
                configurable: true,
                get: function() { return object.__propertyCache__[property]; },
                set: function(value) {
                    if (value === undefined) {
                        // Setting a property to undefined should be ignored,
                        // as it is not a valid JSON value.
                        return;
                    }
                    object.__propertyCache__[property] = value;
                    webChannel.send({
                        type: QWebChannel.PropertyUpdate,
                        object: object.__id__,
                        signal: property,
                        args: [value]
                    });
                }
            });
        }
    }

    // __methods__ is an array of method signatures
    var methodSignatures = data.methods || [];
    var createMethod = function(methodSignature, methodIdx) {
        var methodName = methodSignature.substring(0, methodSignature.indexOf('('));
        object[methodName] = function() {
            var args = [];
            var callback;
            for (var i = 0; i < arguments.length; i++) {
                if (typeof arguments[i] === 'function')
                    callback = arguments[i];
                else
                    args.push(arguments[i]);
            }

            var id = object.__nextId__++;
            if (callback) {
                object.__pendingCallbacks__[id] = callback;
            }

            webChannel.send({
                type: QWebChannel.Signal,
                object: object.__id__,
                signal: methodIdx,
                args: args,
                id: id
            });
        };
    }

    this.__nextId__ = 0;
    this.__pendingCallbacks__ = {};

    for (var i = 0; i < methodSignatures.length; i++) {
        createMethod(methodSignatures[i], i + 1);
    }

    // __signals__ is an array of signal signatures
    var signalSignatures = data.signals || [];
    var createSignal = function(signalSignature, signalIdx) {
        var signalName = signalSignature.substring(0, signalSignature.indexOf('('));
        object[signalName] = {
            connect: function(callback) {
                if (typeof callback !== 'function') {
                    console.error("Bad callback given to connect to signal " + signalName);
                    return;
                }

                var signalList = object.__objectSignals__[signalIdx];
                if (signalList === undefined) {
                    signalList = object.__objectSignals__[signalIdx] = [];
                }
                signalList.push(callback);
            },
            disconnect: function(callback) {
                var signalList = object.__objectSignals__[signalIdx];
                if (signalList === undefined) {
                    return;
                }

                var idx = signalList.indexOf(callback);
                if (idx === -1) {
                    console.error("Bad callback given to disconnect from signal " + signalName);
                    return;
                }
                signalList.splice(idx, 1);
                if (!signalList.length) {
                    delete object.__objectSignals__[signalIdx];
                }
            }
        };
    }

    for (var i = 0; i < signalSignatures.length; i++) {
        createSignal(signalSignatures[i], i + 1);
    }

    this.propertyUpdate = function(name, value) {
        var signalList = object.__objectSignals__[name];
        if (signalList) {
            signalList.forEach(function(callback) {
                callback(value);
            });
        }
    }

    this.signalEmitted = function(name, args)
    {
        var signalList = this.__objectSignals__[name];
        if (signalList) {
            signalList.forEach(function(callback) {
                callback.apply(callback, args);
            });
        }
    }

    this.responseReceived = function(id, data)
    {
        var callback = object.__pendingCallbacks__[id];
        if (callback) {
            callback(data);
            delete object.__pendingCallbacks__[id];
        }
    }
};
