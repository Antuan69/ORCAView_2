import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSignal

class KetcherWindow(QMainWindow):
    """A window to display the Ketcher molecular editor."""
    molecule_updated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ketcher Molecular Editor")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("http://127.0.0.1:5000"))

        self.get_mol_button = QPushButton("Get Molfile and Close")
        self.get_mol_button.clicked.connect(self.get_molfile)

        self.layout.addWidget(self.web_view)
        self.layout.addWidget(self.get_mol_button)

    def get_molfile(self):
        """
        Executes JavaScript to get the molecule data from Ketcher
        and emits the molecule_updated signal.
        """
        script = "ketcher.getMolfile()"
        self.web_view.page().runJavaScript(script, self._handle_molfile)

    def _handle_molfile(self, molfile):
        if molfile:
            self.molecule_updated.emit(molfile)
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
