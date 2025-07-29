"""
This file is a stub. All MainWindow logic has been moved to main_window.py.
To launch the application, import MainWindow from this module.
"""
from .main_window import MainWindow

    def _refresh_job_queue_tab(self):
        self.job_queue_tab.refresh()

    def _create_menu(self):
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("&Settings")
        set_orca_path_action = settings_menu.addAction("Set ORCA Path")
        # ... (other menu creation code)

    def _set_orca_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select ORCA Executable", self.settings.value("orca_path", ""), "All Files (*)"
        )
        if file_path:
            self.settings.setValue("orca_path", file_path)
            self.submitter.orca_path = file_path
            QMessageBox.information(self, "Success", f"ORCA path set to {file_path}")

    def closeEvent(self, event):
        self.settings.sync()
        super().closeEvent(event)

