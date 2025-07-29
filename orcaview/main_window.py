import sys
import os
import time
import traceback

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QTabWidget, QMessageBox, QFileDialog
)

from rdkit import Chem
from rdkit.Chem import Draw, AllChem

from . import config
from .tabs.job_type_tab import JobTypeTab
from .tabs.method_tab import MethodTab
from .tabs.solvation_tab import SolvationTab
from .tabs.advanced_options_tab import AdvancedOptionsTab
from .tabs.coordinates_tab import CoordinatesTab
from .tabs.submission_tab import SubmissionTab
from .tabs.input_blocks_tab import InputBlocksTab
from .job_queue import JobQueueManager, OrcaJob
from .job_queue_tab import JobQueueTab
from .menu import MainMenu
from .signals import AppSignals
from .input_generator import OrcaInputGenerator
from .viewer_3d import MoleculeViewer3D

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ORCAView - UI Redesign")
        self.setGeometry(100, 100, 800, 600)
        self.settings = QSettings("MyCompany", "ORCAView")

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Tab widgets
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Instantiate tab widgets using data from config.py
        self.job_type_tab = JobTypeTab(config.JOB_TYPES)
        self.method_tab = MethodTab(
            config.METHODS, config.DFT_FUNCTIONALS, config.BASIS_SETS, 
            config.SEMIEMPIRICAL_METHODS, config.XTB_METHODS
        )
        self.solvation_tab = SolvationTab()
        self.advanced_options_tab = AdvancedOptionsTab()
        self.coordinates_tab = CoordinatesTab()
        self.input_blocks_tab = InputBlocksTab()
        self.submission_tab = SubmissionTab(self.settings)

        # Ensure solvation models are filtered for the initial method
        initial_method = self.method_tab.method_combo.currentText()
        self._on_method_changed(initial_method)
        self.job_queue_manager = JobQueueManager(on_update_callback=self._refresh_job_queue_tab)
        self.job_queue_tab = JobQueueTab(self.job_queue_manager)

        # Add tabs to the main tab widget
        self.tabs.addTab(self.job_type_tab, "Job Type")
        self.tabs.addTab(self.method_tab, "Method")
        self.tabs.addTab(self.solvation_tab, "Solvation")
        self.tabs.addTab(self.advanced_options_tab, "Advanced")
        self.tabs.addTab(self.input_blocks_tab, "Input Blocks")
        self.tabs.addTab(self.coordinates_tab, "Coordinates")
        self.tabs.addTab(self.submission_tab, "Submission")
        self.tabs.addTab(self.job_queue_tab, "Job Queue")

        # Menu bar
        self.menu = MainMenu(self)

        # Signals
        self.signals = AppSignals()
        self._connect_signals()

        # Internal state
        self.current_molecule = None

    def _connect_signals(self):
        # Job type selection
        self.job_type_tab.job_type_combo.currentTextChanged.connect(
            lambda text: self.signals.job_type_changed.emit(text)
        )
        # Method selection
        self.method_tab.method_combo.currentTextChanged.connect(self._on_method_changed)
        self.signals.method_changed.connect(self._on_method_changed)
        # Solvation model selection
        self.solvation_tab.solvation_model_combo.currentTextChanged.connect(
            lambda text: self.signals.solvation_model_changed.emit(text)
        )
        # Coordinates generation
        self.coordinates_tab.generate_from_smiles_button.clicked.connect(self._generate_structure_from_smiles)
        self.coordinates_tab.view_3d_button.clicked.connect(self._open_3d_viewer)
        # Input generation
        self.submission_tab.generate_button.clicked.connect(self._generate_input)
        self.submission_tab.save_button.clicked.connect(self._save_and_submit)
        self.submission_tab.input_file_browse_button.clicked.connect(self._browse_for_input_file)
        self.submission_tab.output_file_browse_button.clicked.connect(self._browse_for_output_file)
        self._output_path_autoupdate_enabled = True
        self.submission_tab.input_file_path_input.textChanged.connect(self._auto_update_output_path)
        self.submission_tab.output_file_path_input.textEdited.connect(self._disable_output_path_autoupdate)
        self.submission_tab.add_prepared_input_button.clicked.connect(self._add_prepared_input_to_queue)
        self.submission_tab.prepared_input_browse_button.clicked.connect(self._browse_for_prepared_input_file)

    def _browse_for_prepared_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Prepared ORCA Input File", "", "ORCA Input Files (*.inp);;All Files (*)")
        if file_path:
            self.submission_tab.prepared_input_path_input.setText(file_path)

    def _generate_structure_from_smiles(self):
        smiles = self.coordinates_tab.smiles_input.text()
        if not smiles:
            QMessageBox.warning(self, "Input Error", "Please enter a SMILES string.")
            return
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES string")
            temp_img_file = "_temp_mol.png"
            Draw.MolToFile(mol, temp_img_file, size=(300, 300))
            if os.path.exists(temp_img_file):
                pixmap = QPixmap(temp_img_file)
                self.coordinates_tab.mol_image_label.setPixmap(pixmap)
                os.remove(temp_img_file)
            else:
                self.coordinates_tab.mol_image_label.setText("2D depiction could not be generated.")
            mol_with_h = Chem.AddHs(mol, addCoords=True)
            params = AllChem.ETKDGv3()
            params.randomSeed = 1
            AllChem.EmbedMolecule(mol_with_h, params)
            AllChem.MMFFOptimizeMolecule(mol_with_h)
            xyz_block = Chem.MolToXYZBlock(mol_with_h)
            xyz_coords = "\n".join(xyz_block.strip().split('\n')[2:])
            self.coordinates_tab.coordinates_input.setPlainText(xyz_coords)
            self.current_molecule = mol_with_h
            self.signals.coordinates_generated.emit(xyz_coords)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate structure: {e}")
            self.coordinates_tab.mol_image_label.setText("Error generating depiction.")
            self.coordinates_tab.coordinates_input.clear()

    def _generate_input(self):
        try:
            generator = OrcaInputGenerator()
            # Gather all UI state from tabs
            job_type = self.job_type_tab.job_type_combo.currentText()
            method = self.method_tab.method_combo.currentText()
            dft_functional = self.method_tab.dft_functional_combo.currentText()
            # Select basis set combo depending on method
            if method == "DFT":
                basis_set = self.method_tab.dft_basis_set_combo.currentText()
            elif method == "HF":
                basis_set = self.method_tab.hf_basis_set_combo.currentText()
            else:
                basis_set = ""

            se_method = self.method_tab.semiempirical_combo.currentText()
            xtb_method = self.method_tab.xtb_combo.currentText()
            solvation_model = self.solvation_tab.solvation_model_combo.currentText()
            solvent = self.solvation_tab.solvent_combo.currentText()
            other_keywords = self.advanced_options_tab.other_keywords_input.text()
            charge = self.advanced_options_tab.charge_input.value()
            multiplicity = self.advanced_options_tab.multiplicity_input.value()
            nprocs = self.advanced_options_tab.nprocs_input.value()
            memory = self.advanced_options_tab.memory_input.text()
            coords_text = self.coordinates_tab.coordinates_input.toPlainText().strip()
            # Compose keywords
            keyword_parts = [config.JOB_TYPES.get(job_type, "")]
            if method == "DFT":
                keyword_parts.append(dft_functional if not dft_functional.startswith("---") else "")
                keyword_parts.append(basis_set if not basis_set.startswith("---") else "def2-SVP")
            elif method == "HF":
                keyword_parts.append("HF")
                keyword_parts.append(basis_set if not basis_set.startswith("---") else "def2-SVP")
            elif method == "Semi-Empirical":
                keyword_parts.append(config.SEMIEMPIRICAL_METHODS.get(se_method, ""))
            elif method == "xTB":
                keyword_parts.append(config.XTB_METHODS.get(xtb_method, ""))
            if solvation_model and solvation_model != "None":
                model_keyword = "CPCM" if solvation_model == "CPCMC" else solvation_model
                if solvent:
                    keyword_parts.append(f"{model_keyword}({solvent})")
            if other_keywords:
                keyword_parts.extend(other_keywords.split())
            generator.set_keywords([part for part in keyword_parts if part])
            generator.set_charge_and_multiplicity(charge, multiplicity)
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
            if not coordinates:
                QMessageBox.warning(self, "Input Error", "No coordinates provided. Please generate or paste molecular coordinates.")
                return
            generator.set_coordinates(coordinates)
            # Add custom input blocks
            custom_blocks = self.input_blocks_tab.input_blocks
            for block_name, block_content in custom_blocks.items():
                generator.add_block(block_name, block_content)

            generator.add_block("pal", f"nprocs {nprocs}")
            if memory.isdigit():
                generator.add_block("maxcore", memory)
            self.submission_tab.output_text.setReadOnly(False)
            self.submission_tab.output_text.setFont(QFont("Courier New", 10))
            generated_input = generator.generate_input()
            self.submission_tab.output_text.setPlainText(generated_input)
            self.signals.input_generated.emit(generated_input)
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            QMessageBox.critical(self, "Input Generation Error", f"An error occurred while generating the input file:\n{e}\n\n{tb}")

    def _open_3d_viewer(self):
        if self.current_molecule:
            self.viewer_3d_window = MoleculeViewer3D(self.current_molecule)
            self.viewer_3d_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.viewer_3d_window.show()
            self.signals.view_3d_requested.emit(self.current_molecule)
        else:
            QMessageBox.warning(self, "Structure Error", "No structure has been generated yet.")

    def _enqueue_job(self, input_path, output_path, orca_path):
        """Centralized method to create a batch file and queue an ORCA job."""
        try:
            input_dir = os.path.dirname(input_path) or os.getcwd()
            bat_path = os.path.join(input_dir, f"_orca_job_{int(time.time())}.bat")
            
            # Ensure paths are suitable for Windows batch files
            orca_path_win = orca_path.replace('/', '\\')
            input_path_win = input_path.replace('/', '\\')
            output_path_win = output_path.replace('/', '\\')

            orca_cmd = f'"{orca_path_win}" "{input_path_win}" > "{output_path_win}"'
            
            with open(bat_path, 'w') as bat_file:
                bat_file.write(f'@echo off\n{orca_cmd}\n')

            job = OrcaJob(input_path, output_path, bat_path, orca_path)
            self.job_queue_manager.add_job(job)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Job Error", f"Failed to create and queue job: {e}")
            return False

    def _add_prepared_input_to_queue(self):
        input_path = self.submission_tab.prepared_input_path_input.text().strip()
        if not input_path or not os.path.isfile(input_path):
            QMessageBox.warning(self, "Input Error", "Please specify a valid prepared input file.")
            return

        default_out = os.path.splitext(input_path)[0] + ".out"
        output_path, _ = QFileDialog.getSaveFileName(self, "Select Output File", default_out, "Output Files (*.out);;All Files (*)")
        if not output_path:
            return

        orca_path = self.settings.value("orca_path", "").strip()
        if not orca_path or not os.path.isfile(orca_path):
            QMessageBox.warning(self, "Configuration Error", "ORCA executable path is not set or invalid. Please set it in the Settings menu.")
            return

        if self._enqueue_job(input_path, output_path, orca_path):
            QMessageBox.information(self, "Job Queued", f"Job has been added to the queue.")
            self.signals.job_submitted.emit(input_path, output_path)

    def _save_and_submit(self):
        input_text = self.submission_tab.output_text.toPlainText().strip()
        if not input_text:
            QMessageBox.warning(self, "Input Error", "Please generate the input file first.")
            return

        input_filename = self.submission_tab.input_file_path_input.text().strip()
        output_filename = self.submission_tab.output_file_path_input.text().strip()
        if not input_filename or not output_filename:
            QMessageBox.warning(self, "File Error", "Please specify both input and output file paths.")
            return

        orca_path = self.settings.value("orca_path", "").strip()
        if not orca_path or not os.path.isfile(orca_path):
            QMessageBox.warning(self, "Configuration Error", "ORCA executable path is not set or invalid. Please set it in the Settings menu.")
            return

        try:
            with open(input_filename, 'w') as f:
                f.write(input_text)
        except Exception as e:
            QMessageBox.critical(self, "File Error", f"Failed to save input file: {e}")
            return

        if self._enqueue_job(input_filename, output_filename, orca_path):
            self.signals.job_submitted.emit(input_filename, output_filename)

    def _on_method_changed(self, method):
        # Show only solvation models relevant to the selected method
        if method == "xTB":
            models = config.SOLVATION_MODELS.get("xTB", [])
            relevant_models = {"xTB": models}
        elif method in ["DFT", "HF", "Semi-Empirical"]:
            models = config.SOLVATION_MODELS.get("Other", [])
            relevant_models = {"Other": models}
        else:
            # For other methods, show no solvation models
            relevant_models = {"Other": ["None"]}
        self.solvation_tab.update_method(method)

    def _browse_for_input_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Select Input File", "", "ORCA Input Files (*.inp);;All Files (*)")
        if filename:
            self.submission_tab.input_file_path_input.setText(filename)

    def _browse_for_output_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Select Output File", "", "ORCA Output Files (*.out);;All Files (*)")
        if filename:
            self.submission_tab.output_file_path_input.setText(filename)

    def _auto_update_output_path(self):
        if not getattr(self, '_output_path_autoupdate_enabled', True):
            return
        input_path = self.submission_tab.input_file_path_input.text().strip()
        if input_path:
            base, _ = os.path.splitext(input_path)
            output_path = base + '.out'
            self.submission_tab.output_file_path_input.setText(output_path)

    def _disable_output_path_autoupdate(self):
        self._output_path_autoupdate_enabled = False

    def _refresh_job_queue_tab(self):
        self.job_queue_tab.refresh()
