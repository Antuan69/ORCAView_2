import sys
import vispy
vispy.use(app='pyqt6')  # Configure Vispy to use PyQt6 backend before other imports

from PyQt6.QtWidgets import QApplication
from orcaview.main_window import MainWindow

def main():
    """Main function to start the ORCAView application."""
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
