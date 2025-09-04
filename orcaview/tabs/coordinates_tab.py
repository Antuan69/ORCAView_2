from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QHBoxLayout

class CoordinatesTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        coords_layout = QFormLayout(self)

        self.smiles_input = QLineEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES string here (e.g., C for methane)")
        coords_layout.addRow("SMILES Input:", self.smiles_input)

        self.generate_from_smiles_button = QPushButton("Generate Structure from SMILES")

        # Buttons for loading coordinates
        load_buttons_layout = QHBoxLayout()
        self.load_from_file_button = QPushButton("Load from XYZ File")
        self.load_from_paste_button = QPushButton("Paste XYZ Coordinates")
        load_buttons_layout.addWidget(self.generate_from_smiles_button)
        load_buttons_layout.addWidget(self.load_from_file_button)
        load_buttons_layout.addWidget(self.load_from_paste_button)
        coords_layout.addRow(load_buttons_layout)

        # Widget for pasting XYZ coordinates
        self.xyz_paste_input = QTextEdit()
        self.xyz_paste_input.setPlaceholderText("Or paste XYZ coordinates here...")
        self.xyz_paste_input.setVisible(False) # Initially hidden
        coords_layout.addRow(self.xyz_paste_input)


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
        self.draw_molecule_button = QPushButton("Draw Molecule (Ketcher)")
        coords_header_layout.addWidget(self.draw_molecule_button)
        coords_layout.addRow(coords_header_layout)
        coords_layout.addRow(self.coordinates_input)
