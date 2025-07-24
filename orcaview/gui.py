import sys
import os
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
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
from PyQt6.QtGui import QPixmap
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
import json
import os
import logging
import subprocess

from .input_generator import OrcaInputGenerator
from .job_submitter import JobSubmitter
from .syntax_highlighter import OrcaSyntaxHighlighter


logging.basicConfig(level=logging.INFO)



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
        coords_layout = QFormLayout()

        # SMILES input
        self.smiles_input = QLineEdit()
        self.smiles_input.setPlaceholderText("Enter SMILES string here (e.g., C for methane)")
        coords_layout.addRow("SMILES Input:", self.smiles_input)

        # Generate button
        self.generate_from_smiles_button = QPushButton("Generate Structure from SMILES")
        coords_layout.addRow(self.generate_from_smiles_button)

        # 2D depiction view
        self.mol_image_label = QLabel("2D depiction will be shown here.")
        self.mol_image_label.setMinimumSize(400, 300)
        self.mol_image_label.setStyleSheet("border: 1px solid grey; padding: 5px;")
        coords_layout.addRow("2D Depiction:", self.mol_image_label)

        # Coordinates output
        self.coordinates_input = QTextEdit()
        self.coordinates_input.setReadOnly(True)
        self.coordinates_input.setPlaceholderText("Generated 3D coordinates will appear here...")
        coords_layout.addRow("3D Coordinates (XYZ):", self.coordinates_input)
        
        self.layout.addLayout(coords_layout)

    def _create_submission_section(self):
        submission_layout = QFormLayout()

        # ORCA executable path
        path_layout = QHBoxLayout()
        self.orca_path_input = QLineEdit()
        self.orca_path_input.setText(self.settings.value("orca_path", ""))
        path_layout.addWidget(self.orca_path_input)
        self.orca_path_button = QPushButton("Browse...")
        path_layout.addWidget(self.orca_path_button)
        submission_layout.addRow("ORCA Executable Path:", path_layout)

        # Input File Path
        input_path_layout = QHBoxLayout()
        self.input_file_path_input = QLineEdit()
        self.input_file_path_input.setPlaceholderText("Path to save .inp file")
        input_path_layout.addWidget(self.input_file_path_input)
        self.input_file_browse_button = QPushButton("Browse...")
        input_path_layout.addWidget(self.input_file_browse_button)
        submission_layout.addRow("Input File:", input_path_layout)

        # Output File Path
        output_path_layout = QHBoxLayout()
        self.output_file_path_input = QLineEdit()
        self.output_file_path_input.setPlaceholderText("Path to save .out file")
        output_path_layout.addWidget(self.output_file_path_input)
        self.output_file_browse_button = QPushButton("Browse...")
        output_path_layout.addWidget(self.output_file_browse_button)
        submission_layout.addRow("Output File:", output_path_layout)

        # Buttons and output text
        self.generate_button = QPushButton("Generate Input")
        self.save_button = QPushButton("Save and Submit to ORCA")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier New", 10))

        # Add widgets in a way that QFormLayout understands
        submission_layout.addRow(self.generate_button)
        submission_layout.addRow(self.output_text)
        submission_layout.addRow(self.save_button)

        self.layout.addLayout(submission_layout)

    def _initialize_backend(self):
        self.highlighter = OrcaSyntaxHighlighter(self.output_text.document())

    def _connect_signals(self):
        self.method_combo.currentTextChanged.connect(self._update_ui_for_method)
        self.solvation_model_combo.currentTextChanged.connect(self._update_solvent_dropdown)
        self.generate_from_smiles_button.clicked.connect(self._generate_structure_from_smiles)
        self.orca_path_button.clicked.connect(self._browse_for_orca)
        self.generate_button.clicked.connect(self._generate_input)
        self.save_button.clicked.connect(self._save_and_submit)
        self.input_file_browse_button.clicked.connect(self._browse_for_input_file)
        self.output_file_browse_button.clicked.connect(self._browse_for_output_file)

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
        # Create a new generator for every run to ensure a clean state
        generator = OrcaInputGenerator()

        # 1. Set Keywords
        job_type = self.job_type_combo.currentText()
        method = self.method_combo.currentText()
        other_keywords = self.other_keywords_input.text()
        dft_functional = self.dft_functional_combo.currentText()
        basis_set = self.basis_set_combo.currentText()
        se_method = self.semiempirical_combo.currentText()
        xtb_method = self.xtb_combo.currentText()
        solvation_model = self.solvation_model_combo.currentText()
        solvent = self.solvent_combo.currentText()

        keyword_parts = [self.job_types.get(job_type, "")]
        if method == "DFT":
            keyword_parts.append(dft_functional if not dft_functional.startswith("---") else "")
            keyword_parts.append(basis_set if not basis_set.startswith("---") else "def2-SVP")
        elif method == "HF":
            keyword_parts.append("HF")
            keyword_parts.append(basis_set if not basis_set.startswith("---") else "def2-SVP")
        elif method == "Semi-Empirical":
            keyword_parts.append(self.semiempirical_methods.get(se_method, ""))
        elif method == "xTB":
            keyword_parts.append(self.xtb_methods.get(xtb_method, ""))

        if solvation_model and solvation_model != "None":
            model_keyword = "CPCM" if solvation_model == "CPCMC" else solvation_model
            if solvent:
                keyword_parts.append(f"{model_keyword}({solvent})")

        if other_keywords:
            keyword_parts.extend(other_keywords.split())

        generator.set_keywords([part for part in keyword_parts if part])

        # 2. Set Charge and Multiplicity
        charge = self.charge_input.value()
        multiplicity = self.multiplicity_input.value()
        generator.set_charge_and_multiplicity(charge, multiplicity)

        # 3. Set Coordinates
        coords_text = self.coordinates_input.toPlainText().strip()
        if not coords_text:
            QMessageBox.warning(self, "Input Error", "Coordinates are missing. Please generate a structure first.")
            return
        
        coordinates = []
        for line in coords_text.split('\n'):
            parts = line.split()
            if len(parts) == 4:
                try:
                    atom = parts[0]
                    x, y, z = map(float, parts[1:])
                    coordinates.append([atom, x, y, z])
                except (ValueError, IndexError):
                    QMessageBox.warning(self, "Coordinate Error", f"Could not parse coordinate line: {line}")
                    return
        generator.set_coordinates(coordinates)

        # 4. Set Blocks
        nprocs = self.nprocs_input.value()
        generator.add_block("pal", f"nprocs {nprocs}")
        memory = self.memory_input.text()
        if memory.isdigit():
            generator.add_block("maxcore", memory)

        # 5. Generate and Display
        generated_input = generator.generate_input()
        self.output_text.setPlainText(generated_input)

    def _generate_structure_from_smiles(self):
        """Generates and optimizes a 3D structure from a SMILES string."""
        smiles = self.smiles_input.text()
        if not smiles:
            QMessageBox.warning(self, "Input Error", "Please enter a SMILES string.")
            return

        try:
            # Create molecule from SMILES
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES string")

            # --- Generate 2D Depiction by saving to a temporary file ---
            temp_img_file = "_temp_mol.png"
            Draw.MolToFile(mol, temp_img_file, size=(400, 300))
            pixmap = QPixmap(temp_img_file)
            self.mol_image_label.setPixmap(pixmap)
            # Clean up the temporary file
            if os.path.exists(temp_img_file):
                os.remove(temp_img_file)

            # --- Generate 3D Coordinates ---
            mol_with_h = Chem.AddHs(mol, addCoords=True)
            # Use ETKDGv3 for better coordinate generation
            params = AllChem.ETKDGv3()
            params.randomSeed = 1 # for reproducibility
            AllChem.EmbedMolecule(mol_with_h, params)
            
            # Optimize the structure with MMFF94 force field
            AllChem.MMFFOptimizeMolecule(mol_with_h)
            
            # Get XYZ coordinates
            xyz_block = Chem.MolToXYZBlock(mol_with_h)
            # Remove the header lines (atom count and comment)
            xyz_coords = "\n".join(xyz_block.strip().split('\n')[2:])
            
            self.coordinates_input.setPlainText(xyz_coords)
            logging.info(f"Successfully generated structure for SMILES: {smiles}")

        except Exception as e:
            error_msg = f"Failed to generate structure: {e}"
            logging.error(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            self.mol_image_label.setText("Error generating depiction.")
            self.coordinates_input.clear()

    def _browse_for_orca(self):
        executable_filter = "ORCA Executable (orca.exe)" if sys.platform == "win32" else "ORCA Executable (orca)"
        path, _ = QFileDialog.getOpenFileName(self, "Select ORCA Executable", "", executable_filter)
        if path:
            self.orca_path_input.setText(path)

    def _browse_for_input_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save ORCA Input File", "", "ORCA Input Files (*.inp);;All Files (*)")
        if path:
            self.input_file_path_input.setText(path)
            # Automatically set the output file path
            output_path = os.path.splitext(path)[0] + ".out"
            self.output_file_path_input.setText(output_path)

    def _browse_for_output_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save ORCA Output File", "", "ORCA Output Files (*.out);;All Files (*)")
        if path:
            self.output_file_path_input.setText(path)

    def _save_and_submit(self):
        # First, ensure the input is generated
        if not self.output_text.toPlainText().strip():
            QMessageBox.warning(self, "Warning", "Please generate the input file first.")
            return

        # Get ORCA path
        orca_path = self.orca_path_input.text()
        if not orca_path or not os.path.exists(orca_path):
            QMessageBox.warning(self, "ORCA Path Error", "Please provide a valid path to the ORCA executable.")
            return

        # Get the input and output file paths
        input_filename = self.input_file_path_input.text().strip()
        output_filename = self.output_file_path_input.text().strip()

        if not input_filename or not output_filename:
            QMessageBox.warning(self, "Input Error", "Please specify both input and output file paths.")
            return
        try:
            with open(input_filename, 'w') as f:
                f.write(self.output_text.toPlainText())
        except Exception as e:
            QMessageBox.critical(self, "File Error", f"Failed to save input file: {e}")
            return

        # Run the ORCA calculation
        try:
            logging.info(f"Starting ORCA calculation: {orca_path} {input_filename}")
            with open(output_filename, 'w') as outfile:
                # Use Popen for non-blocking execution
                process = subprocess.Popen(
                    [orca_path, input_filename],
                    stdout=outfile,
                    stderr=subprocess.PIPE,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
                )
            self.orca_process = process # Store for potential future management
            QMessageBox.information(self, "Submission Successful", 
                                    f"ORCA calculation has been started.\n"
                                    f"Output will be written to {output_filename}")
        except Exception as e:
            QMessageBox.critical(self, "Submission Error", f"Failed to start ORCA process: {e}")

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

