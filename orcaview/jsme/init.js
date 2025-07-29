console.log("init.js loaded");
// This function will be called by the JSME script once it's loaded and ready.
function jsmeOnLoad() {
    console.log("jsmeOnLoad called – initializing editor");
    window.jsmeApplet = new JSApplet.JSME("jsme_container", "100%", "100%", {
        "options": "oldlook,star",
        // Tell JSME to call our setupBridge function once the editor is initialized.
        "oninit": "setupBridge"
    });
    // Fallback: ensure setupBridge runs even if 'oninit' is not triggered
    setTimeout(setupBridge, 0);
}

// This function is called by JSME as a callback when the editor is ready.
function setupBridge() {
    console.log("setupBridge called – attempting to connect to QWebChannel");
    if (typeof qt !== 'undefined' && typeof qt.webChannelTransport !== 'undefined') {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            window.bridge = channel.objects.bridge;

            // Forward console.log messages to Python
            const origLog = console.log;
            console.log = function (...args) {
                origLog.apply(console, args);
                if (window.bridge && typeof window.bridge.jsLog === 'function') {
                    window.bridge.jsLog(args.join(' '));
                }
            };
        });

        // Poll until the bridge is ready, then send the signal
        const readyInterval = setInterval(function() {
            if (window.bridge) {
                console.log("Bridge is ready, sending editorReady signal to Python.");
                window.bridge.editorReady();
                clearInterval(readyInterval);
            } else {
                console.log("Waiting for Python-JS bridge...");
            }
        }, 100); // Check every 100ms
    } else {
        console.error("QWebChannel is not available. qt or qt.webChannelTransport undefined");
    }
}

// This function is called by Python to retrieve the molecule data.
function getMolfileFromEditor() {
    if (window.jsmeApplet && window.bridge) {
        const molfile = window.jsmeApplet.molFile();
        const lines = molfile.trim().split('\n');
        if (lines.length <= 4) {
            window.bridge.receiveMolfile("");
        } else {
            window.bridge.receiveMolfile(molfile);
        }
    } else {
        console.error("JSME applet or bridge not ready.");
    }
}
