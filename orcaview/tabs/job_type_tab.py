from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox

class JobTypeTab(QWidget):
    def __init__(self, job_types, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        self.job_type_combo = QComboBox()
        self.job_type_combo.addItems(job_types.keys())
        layout.addRow("Job Type:", self.job_type_combo)
