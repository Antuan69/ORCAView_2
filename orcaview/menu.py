from PyQt6.QtWidgets import QMenuBar, QFileDialog, QMessageBox

class MainMenu:
    def __init__(self, main_window):
        self.menu_bar = main_window.menuBar()
        self.settings_menu = self.menu_bar.addMenu("&Settings")
        self.set_orca_path_action = self.settings_menu.addAction("Set ORCA Path")
        # Add more menu actions as needed

    def set_orca_path(self, main_window):
        file_path, _ = QFileDialog.getOpenFileName(
            main_window, "Select ORCA Executable", main_window.settings.value("orca_path", ""), "All Files (*)"
        )
        if file_path:
            main_window.settings.setValue("orca_path", file_path)
            QMessageBox.information(main_window, "Success", f"ORCA path set to {file_path}")
