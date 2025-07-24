import sys
from PyQt6.QtWidgets import QApplication
from orcaview.gui import MainWindow

def main():
    """Main function to start the ORCAView application."""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
