from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QHBoxLayout

class CoordinatesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        coords_layout = QFormLayout(self)

        self.smiles_input = QLineEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES string here (e.g., C for methane)")
        coords_layout.addRow("SMILES Input:", self.smiles_input)

        self.generate_from_smiles_button = QPushButton("Generate Structure from SMILES")
        coords_layout.addRow(self.generate_from_smiles_button)

        self.mol_image_label = QLabel("2D depiction will be shown here.")
        self.mol_image_label.setFixedSize(300, 300)
        self.mol_image_label.setStyleSheet("border: 1px solid grey; padding: 5px;")
        self.mol_image_label.setScaledContents(True)
        coords_layout.addRow("2D Depiction:", self.mol_image_label)

        self.coordinates_input = QTextEdit()
        self.coordinates_input.setReadOnly(True)
        self.coordinates_input.setPlaceholderText("Generated 3D coordinates will appear here...")
        coords_header_layout = QHBoxLayout()
        coords_header_layout.addWidget(QLabel("3D Coordinates:"))
        coords_header_layout.addStretch()
        self.view_3d_button = QPushButton("View 3D")
        coords_header_layout.addWidget(self.view_3d_button)
        coords_layout.addRow(coords_header_layout)
        coords_layout.addRow(self.coordinates_input)
