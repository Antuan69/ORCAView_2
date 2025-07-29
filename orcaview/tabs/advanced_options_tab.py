from PyQt6.QtWidgets import QWidget, QFormLayout, QSpinBox, QLineEdit

class AdvancedOptionsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        advanced_layout = QFormLayout(self)
        self.charge_input = QSpinBox()
        self.multiplicity_input = QSpinBox()
        self.multiplicity_input.setMinimum(1)
        self.nprocs_input = QSpinBox()
        self.nprocs_input.setMinimum(1)
        self.memory_input = QLineEdit("4000")
        self.other_keywords_input = QLineEdit()
        advanced_layout.addRow("Charge:", self.charge_input)
        advanced_layout.addRow("Multiplicity:", self.multiplicity_input)
        advanced_layout.addRow("Processors:", self.nprocs_input)
        advanced_layout.addRow("Memory (MB):", self.memory_input)
        advanced_layout.addRow("Other Keywords:", self.other_keywords_input)
