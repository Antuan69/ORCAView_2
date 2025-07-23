import sys
import os
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QTextEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
)

from .input_generator import OrcaInputGenerator
from .job_submitter import JobSubmitter
from .syntax_highlighter import OrcaSyntaxHighlighter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ORCAView")
        self.setGeometry(100, 100, 800, 600)

        self.settings = QSettings("ORCAView", "main")

        self._create_menu()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self._create_input_widgets()
        self._create_output_widgets()

        self.generator = OrcaInputGenerator()
        orca_path = self.settings.value("orca_path", "path/to/orca.exe")
        self.submitter = JobSubmitter(orca_path=orca_path)


    def _create_input_widgets(self):
        input_layout = QFormLayout()

        self.keywords_input = QLineEdit("B3LYP def2-SVP Opt")
        self.charge_input = QSpinBox()
        self.charge_input.setValue(0)
        self.multiplicity_input = QSpinBox()
        self.multiplicity_input.setValue(1)
        self.multiplicity_input.setMinimum(1)

        self.nprocs_input = QSpinBox()
        self.nprocs_input.setValue(1)
        self.nprocs_input.setMinimum(1)

        self.memory_input = QLineEdit("4000") # Memory in MB

        self.coordinates_input = QTextEdit("C 0.0 0.0 0.0\nH 0.0 0.0 1.09")

        input_layout.addRow(QLabel("Keywords:"), self.keywords_input)
        input_layout.addRow(QLabel("Charge:"), self.charge_input)
        input_layout.addRow(QLabel("Multiplicity:"), self.multiplicity_input)
        input_layout.addRow(QLabel("Number of Processors:"), self.nprocs_input)
        input_layout.addRow(QLabel("Memory (MB):"), self.memory_input)
        input_layout.addRow(QLabel("Coordinates (XYZ):"), self.coordinates_input)

        self.layout.addLayout(input_layout)

        self.load_xyz_button = QPushButton("Load XYZ")
        self.load_xyz_button.clicked.connect(self._load_xyz)
        self.layout.addWidget(self.load_xyz_button)

    def _create_output_widgets(self):
        self.generate_button = QPushButton("Generate Input")
        self.generate_button.clicked.connect(self._generate_input)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.highlighter = OrcaSyntaxHighlighter(self.output_text.document())

        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(QLabel("Generated Input:"))
        self.layout.addWidget(self.output_text)

        self.save_button = QPushButton("Save and Submit")
        self.save_button.clicked.connect(self._save_and_submit)
        self.layout.addWidget(self.save_button)

    def _generate_input(self):
        keywords = self.keywords_input.text().split()
        self.generator.set_keywords(keywords)

        charge = self.charge_input.value()
        multiplicity = self.multiplicity_input.value()
        self.generator.set_charge_and_multiplicity(charge, multiplicity)

        coords_text = self.coordinates_input.toPlainText().strip().split('\n')
        coordinates = []
        for line in coords_text:
            parts = line.split()
            if len(parts) == 4:
                atom = parts[0]
                x, y, z = map(float, parts[1:])
                coordinates.append([atom, x, y, z])
        self.generator.set_coordinates(coordinates)

        # Add PAL block for processors
        nprocs = self.nprocs_input.value()
        self.generator.add_block("pal", f"nprocs {nprocs}")

        # Add maxcore block for memory
        memory = self.memory_input.text()
        if memory.isdigit():
            self.generator.add_block("maxcore", memory)

        generated_input = self.generator.generate_input()
        self.output_text.setPlainText(generated_input)

    def _load_xyz(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load XYZ File", "", "XYZ Files (*.xyz);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()
                
                # XYZ format: first two lines are atom count and a comment
                coord_lines = lines[2:]
                self.coordinates_input.setPlainText("".join(coord_lines))
                QMessageBox.information(
                    self, "Success", f"Coordinates loaded from {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not load XYZ file: {e}")

    def _create_menu(self):
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("&Settings")

        set_orca_path_action = settings_menu.addAction("Set ORCA Path")
        set_orca_path_action.triggered.connect(self._set_orca_path)

    def _set_orca_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select ORCA Executable", "", "Executables (*.exe);;All Files (*)"
        )
        if file_path:
            self.settings.setValue("orca_path", file_path)
            self.submitter.orca_path = file_path
            QMessageBox.information(
                self, "Success", f"ORCA path set to {file_path}"
            )

    def _save_and_submit(self):
        # First, ensure the input is generated
        self._generate_input()
        generated_input = self.output_text.toPlainText()

        if not generated_input:
            QMessageBox.warning(self, "Warning", "No input file generated.")
            return

        # Open file dialog to save the input file
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save ORCA Input File",
            "",
            "ORCA Input Files (*.inp);;All Files (*)",
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(generated_input)

                job_name = os.path.splitext(os.path.basename(file_path))[0]
                script_path = self.submitter.create_submission_script(job_name, file_path)

                QMessageBox.information(
                    self,
                    "Success",
                    f"Input file saved to {file_path}\nSubmission script created at {script_path}",
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

