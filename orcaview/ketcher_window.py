import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSignal, QObject, pyqtSlot
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtWebChannel import QWebChannel

class WebEnginePage(QWebEnginePage):
    """Custom WebEnginePage to capture JavaScript console messages."""
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS Console ({sourceID}:{lineNumber}): {message}")


class Bridge(QObject):
    smiles_requested = pyqtSignal()
    smiles_received = pyqtSignal(str)

    @pyqtSlot()
    def get_smiles(self):
        """Called from JS when the button is clicked."""
        self.smiles_requested.emit()

    @pyqtSlot(str)
    def receive_smiles(self, smiles):
        """Called from JS with the SMILES string."""
        self.smiles_received.emit(smiles)

class KetcherWindow(QMainWindow):
    """A window to display the Ketcher molecular editor."""
    smiles_updated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ketcher Molecular Editor")
        self.setGeometry(100, 100, 1200, 800)

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Set custom page to capture JS console logs
        self.page = WebEnginePage(self)
        self.web_view.setPage(self.page)

        # Setup QWebChannel to allow JS to call Python
        self.bridge = Bridge()
        self.channel = QWebChannel(self.page)
        self.page.setWebChannel(self.channel)
        self.channel.registerObject("bridge", self.bridge)

        # Connect signals
        self.page.loadFinished.connect(self.on_load_finished)
        self.bridge.smiles_requested.connect(self.get_smiles)
        self.bridge.smiles_received.connect(self._handle_smiles)

        self.web_view.setUrl(QUrl("http://127.0.0.1:5000"))

    def on_load_finished(self, ok):
        if ok:
            script = """
                // Load the qwebchannel.js script
                var script = document.createElement('script');
                script.src = 'qrc:///qtwebchannel/qwebchannel.js';
                document.head.appendChild(script);

                script.onload = function() {
                    new QWebChannel(qt.webChannelTransport, function(channel) {
                        window.bridge = channel.objects.bridge;

                        // Create and style the button
                        var button = document.createElement('button');
                        button.innerHTML = 'Get SMILES';
                        button.style.position = 'fixed';
                        button.style.bottom = '10px';
                        button.style.right = '10px';
                        button.style.zIndex = '1000';
                        button.style.padding = '10px 20px';
                        button.style.backgroundColor = '#4CAF50';
                        button.style.color = 'white';
                        button.style.border = 'none';
                        button.style.borderRadius = '5px';
                        button.style.cursor = 'pointer';

                        // Add button to the page
                        document.body.appendChild(button);

                        // Connect button click to Python
                        button.onclick = function() {
                            window.bridge.get_smiles();
                        };
                    });
                }
            """
            self.page.runJavaScript(script)

    def get_smiles(self):
        """
        Executes JavaScript to get the SMILES string from Ketcher
        and emits the smiles_updated signal.
        """
        script = "(async () => { const smiles = await ketcher.getSmiles(); window.bridge.receive_smiles(smiles); })();"
        self.page.runJavaScript(script)

    def _handle_smiles(self, smiles):
        if smiles:
            self.smiles_updated.emit(smiles)
        self.close()

if __name__ == '__main__':
    # For testing purposes
    from orcaview.ketcher_server import run_server
    import threading

    app = QApplication(sys.argv)

    # Run Flask server in a background thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    window = KetcherWindow()
    window.show()
    sys.exit(app.exec())
