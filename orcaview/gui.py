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
    QPushButton,
    QTextEdit,
    QComboBox,
    QLabel,
    QSpinBox,
    QTabWidget,
    QStackedWidget,
    QFileDialog,
    QMessageBox
)
from PyQt6.QtGui import QFont

from .input_generator import OrcaInputGenerator
from .job_submitter import JobSubmitter
from .syntax_highlighter import OrcaSyntaxHighlighter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ORCAView - UI Redesign")
        self.setGeometry(100, 100, 800, 600)
        self.settings = QSettings("MyCompany", "ORCAView")

        # Phase 1: Initialize all data structures first
        self._initialize_data()

        # Phase 2: Create UI components in a structured way
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self._create_main_tabs()
        self._create_job_type_tab()
        self._create_method_tab()
        self._create_solvation_tab()
        self._create_advanced_options_section()
        self._create_coordinates_section()
        self._create_submission_section()
        self._create_menu()

        # Phase 3: Initialize backend components
        self._initialize_backend()

        # Phase 4: Connect signals and set initial UI state
        self._connect_signals()
        self._update_ui_for_method(self.method_combo.currentText())

    def _initialize_data(self):
        """Defines all data dictionaries needed for the UI, preventing startup crashes."""
        self.job_types = {
            "Single Point": "SP", "Geometry Optimization": "Opt", "Frequency Analysis": "Freq",
            "Transition State Search": "OptTS", "Composite Methods": "", "NEB": "NEB", "IRC": "IRC"
        }
        self.methods = ["DFT", "HF", "Semi-Empirical", "xTB"]
        self.dft_functionals = {
            "Hybrid": ["B3LYP", "PBE0", "TPSSh", "HSE06", "CAM-B3LYP", "wB97X-D3"],
            "GGA": ["BP86", "PBE", "revPBE", "B97-D3"],
            "Meta-GGA": ["TPSS", "revTPSS", "M06-L", "SCAN"],
            "Double-Hybrid": ["B2PLYP", "DSD-PBEP86-D3"]
        }
        self.basis_sets = {
            "Pople": ["6-31G(d)", "6-311G(d,p)", "6-311++G(2d,2p)"],
            "Dunning": ["cc-pVDZ", "aug-cc-pVDZ", "cc-pVTZ", "aug-cc-pVTZ"],
            "Karlsruhe": ["def2-SVP", "def2-TZVP", "def2-QZVP"]
        }
        self.semiempirical_methods = {
            "AM1": "AM1", "PM3": "PM3", "MNDO": "MNDO", "OM3": "OM3", "PM7": "PM7", "GFN2-xTB": "GFN2-xTB"
        }
        self.xtb_methods = {"GFN1-xTB": "GFN1-xTB", "GFN2-xTB": "GFN2-xTB"}
        self.solvation_models = {
            "xTB": ["None", "ALPB", "DDCOSMO", "CPCMX"],
            "Other": ["None", "CPCM", "SMD"]
        }
        self.solvents_by_model = {
            "ALPB": ["Acetone", "Acetonitrile", "H2O", "Hexane", "Methanol", "Toluene"],
            "DDCOSMO": ["acetone", "acetonitrile", "h2o", "hexane", "methanol", "toluene"],
            "CPCMX": ["Acetonitrile", "DMSO", "H2O", "Methanol", "THF"],
            "CPCM": ["acetone", "acetonitrile", "benzene", "ch2cl2", "dmso", "h2o", "hexane", "methanol"],
            "SMD": ["water", "acetonitrile", "methanol", "ethanol", "chloroform", "benzene", "toluene", "dmso"]
        }

    def _create_main_tabs(self):
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

    def _create_job_type_tab(self):
        self.job_tab = QWidget()
        layout = QFormLayout(self.job_tab)
        self.job_type_combo = QComboBox()
        self.job_type_combo.addItems(self.job_types.keys())
        layout.addRow("Job Type:", self.job_type_combo)
        self.tabs.addTab(self.job_tab, "Job Type")

    def _create_method_tab(self):
        self.method_tab = QWidget()
        layout = QFormLayout(self.method_tab)
        self.method_combo = QComboBox()
        self.method_combo.addItems(self.methods)
        layout.addRow("Method:", self.method_combo)

        self.method_stack = QStackedWidget()
        layout.addRow(self.method_stack)

        # Pane 0: DFT/HF
        self.dft_hf_pane = QWidget()
        self.dft_hf_layout = QFormLayout(self.dft_hf_pane)
        self.dft_functional_combo = QComboBox()
        for group, items in self.dft_functionals.items():
            self.dft_functional_combo.addItem(f"-- {group} --")
            self.dft_functional_combo.addItems(items)
        self.basis_set_combo = QComboBox()
        for group, items in self.basis_sets.items():
            self.basis_set_combo.addItem(f"-- {group} --")
            self.basis_set_combo.addItems(items)
        self.dft_hf_layout.addRow("DFT Functional:", self.dft_functional_combo)
        self.dft_hf_layout.addRow("Basis Set:", self.basis_set_combo)
        self.method_stack.addWidget(self.dft_hf_pane)

        # Pane 1: Semi-Empirical
        self.semi_pane = QWidget()
        semi_layout = QFormLayout(self.semi_pane)
        self.semiempirical_combo = QComboBox()
        self.semiempirical_combo.addItems(self.semiempirical_methods.keys())
        semi_layout.addRow("Semi-Empirical Method:", self.semiempirical_combo)
        self.method_stack.addWidget(self.semi_pane)

        # Pane 2: xTB
        self.xtb_pane = QWidget()
        xtb_layout = QFormLayout(self.xtb_pane)
        self.xtb_combo = QComboBox()
        self.xtb_combo.addItems(self.xtb_methods.keys())
        xtb_layout.addRow("xTB Method:", self.xtb_combo)
        self.method_stack.addWidget(self.xtb_pane)

        # Pane 3: Empty (for methods with no options)
        self.no_options_pane = QWidget()
        self.method_stack.addWidget(self.no_options_pane)

        self.tabs.addTab(self.method_tab, "Method")

    def _create_solvation_tab(self):
        self.solvation_tab = QWidget()
        self.solvation_layout = QFormLayout(self.solvation_tab)
        self.solvation_model_combo = QComboBox()
        self.solvent_combo = QComboBox()
        self.solvation_layout.addRow("Solvation Model:", self.solvation_model_combo)
        self.solvation_layout.addRow("Solvent:", self.solvent_combo)
        self.tabs.addTab(self.solvation_tab, "Solvation")

    def _create_advanced_options_section(self):
        advanced_layout = QFormLayout()
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
        self.layout.addLayout(advanced_layout)

    def _create_coordinates_section(self):
        self.layout.addWidget(QLabel("Coordinates (XYZ format):"))
        self.coordinates_input = QTextEdit()
        self.load_xyz_button = QPushButton("Load XYZ")
        self.layout.addWidget(self.coordinates_input)
        self.layout.addWidget(self.load_xyz_button)

    def _create_submission_section(self):
        self.generate_button = QPushButton("Generate Input")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.save_button = QPushButton("Save and Submit")
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(QLabel("Generated Input:"))
        self.layout.addWidget(self.output_text)
        self.layout.addWidget(self.save_button)

    def _initialize_backend(self):
        self.generator = OrcaInputGenerator()
        orca_path = self.settings.value("orca_path", "path/to/orca.exe")
        self.submitter = JobSubmitter(orca_path=orca_path)
        self.highlighter = OrcaSyntaxHighlighter(self.output_text.document())

    def _connect_signals(self):
        self.method_combo.currentTextChanged.connect(self._update_ui_for_method)
        self.solvation_model_combo.currentTextChanged.connect(self._update_solvent_dropdown)
        self.load_xyz_button.clicked.connect(self._load_xyz)
        self.generate_button.clicked.connect(self._generate_input)
        self.save_button.clicked.connect(self._save_and_submit)

    def _update_ui_for_method(self, method):
        is_dft = method == "DFT"
        is_hf = method == "HF"

        if is_dft or is_hf:
            self.method_stack.setCurrentWidget(self.dft_hf_pane)
            self.dft_functional_combo.setVisible(is_dft)
            # Also toggle the label's visibility for a clean UI
            label = self.dft_hf_layout.labelForField(self.dft_functional_combo)
            if label:
                label.setVisible(is_dft)
        elif method == "Semi-Empirical":
            self.method_stack.setCurrentWidget(self.semi_pane)
        elif method == "xTB":
            self.method_stack.setCurrentWidget(self.xtb_pane)
        else:
            self.method_stack.setCurrentWidget(self.no_options_pane)

        # Update solvation options based on the selected method
        show_solvation = method in ["DFT", "HF", "Semi-Empirical", "xTB"]
        self.tabs.setTabVisible(self.tabs.indexOf(self.solvation_tab), show_solvation)

        current_models = []
        if method == "xTB":
            current_models = self.solvation_models["xTB"]
        elif show_solvation:
            current_models = self.solvation_models["Other"]

        self.solvation_model_combo.blockSignals(True)
        self.solvation_model_combo.clear()
        if current_models:
            self.solvation_model_combo.addItems(current_models)
        else:
            self.solvation_model_combo.addItem("None")
        self.solvation_model_combo.blockSignals(False)

        # Manually trigger the update for the new state, since signals were blocked.
        self._update_solvent_dropdown(self.solvation_model_combo.currentText())

    def _update_solvent_dropdown(self, model):
        self.solvent_combo.clear()
        is_solvation_selected = model and model != "None"

        self.solvent_combo.setVisible(is_solvation_selected)
        solvent_label = self.solvation_layout.labelForField(self.solvent_combo)
        if solvent_label:
            solvent_label.setVisible(is_solvation_selected)

        if is_solvation_selected:
            solvents = self.solvents_by_model.get(model, [])
            self.solvent_combo.addItems(solvents)
            if "water" in [s.lower() for s in solvents]:
                # Find the actual case-sensitive solvent name to set it
                water_actual = next((s for s in solvents if s.lower() == "water"), None)
                if water_actual:
                    self.solvent_combo.setCurrentText(water_actual)

    def _generate_input(self):
        job_type = self.job_type_combo.currentText()
        method = self.method_combo.currentText()
        other_keywords = self.other_keywords_input.text()

        dft_functional = self.dft_functional_combo.currentText()
        if dft_functional.startswith("---"):
            dft_functional = ""

        basis_set = self.basis_set_combo.currentText()

        if basis_set.startswith("---"):
            basis_set = "def2-SVP" # Default basis set

        method_keyword = ""
        if method == "DFT":
            method_keyword = dft_functional
        elif method == "HF":
            method_keyword = "HF"
        elif method == "Semi-Empirical":
            se_method = self.semiempirical_combo.currentText()
            method_keyword = self.semiempirical_methods.get(se_method, "")
        elif method == "xTB":
            xtb_method = self.xtb_combo.currentText()
            method_keyword = self.xtb_methods.get(xtb_method, "")

        # Basis sets are often implicit for Semi-Empirical and xTB methods
        basis_set_keyword = basis_set if method in ["DFT", "HF"] else ""

        solvation_keyword = ""
        solvation_model = self.solvation_model_combo.currentText()
        if solvation_model and solvation_model != "None":
            solvent = self.solvent_combo.currentText()
            # CPCMC is a shortcut for CPCM with a specific epsilon function
            model_keyword = "CPCM" if solvation_model == "CPCMC" else solvation_model
            if solvent:
                solvation_keyword = f"{model_keyword}({solvent})"

        # Collect all keyword parts into a list
        keyword_parts = [self.job_types.get(job_type, ""), method_keyword, basis_set_keyword, solvation_keyword]
        
        # Add user-defined keywords, splitting them by space to handle multiple keywords
        if other_keywords:
            keyword_parts.extend(other_keywords.split())

        # Filter out any empty strings from the list of keyword parts
        final_keywords = [part for part in keyword_parts if part]

        self.generator.set_keywords(final_keywords)

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

                # Ask user if they want to submit the job
                reply = QMessageBox.question(self, 'Submit Job',
                                           'Do you want to submit this job to ORCA?',
                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                           QMessageBox.StandardButton.No)

                if reply == QMessageBox.StandardButton.Yes:
                    self.submitter.submit(file_path)
                    QMessageBox.information(self, "Success", f"Job submitted for file: {file_path}")
                else:
                    QMessageBox.information(self, "Info", f"Input file saved to {file_path}. Job not submitted.")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def _create_menu(self):
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("&Settings")
        set_orca_path_action = settings_menu.addAction("Set ORCA Path")
        set_orca_path_action.triggered.connect(self._set_orca_path)

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

