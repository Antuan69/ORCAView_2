import sys
import os
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget
from PyQt6.QtGui import QFont

from .tabs.job_type_tab import JobTypeTab
from .tabs.method_tab import MethodTab
from .tabs.solvation_tab import SolvationTab
from .tabs.advanced_options_tab import AdvancedOptionsTab
from .tabs.coordinates_tab import CoordinatesTab
from .tabs.submission_tab import SubmissionTab
from .job_queue import JobQueueManager, OrcaJob
from .job_queue_tab import JobQueueTab
from .menu import MainMenu
from .signals import AppSignals
from .input_generator import OrcaInputGenerator
from .viewer_3d import MoleculeViewer3D
from PyQt6.QtWidgets import QMessageBox
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
import os
import time

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

        # Data dictionaries (should be loaded from config or static)
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

        # Instantiate tab widgets
        self.job_type_tab = JobTypeTab(self.job_types)
        self.method_tab = MethodTab(self.methods, self.dft_functionals, self.basis_sets, self.semiempirical_methods, self.xtb_methods)
        self.solvation_tab = SolvationTab(self.solvation_models, self.solvents_by_model)
        self.advanced_options_tab = AdvancedOptionsTab()
        self.coordinates_tab = CoordinatesTab()
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
        from PyQt6.QtWidgets import QFileDialog
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
            from PyQt6.QtGui import QPixmap
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

    def _add_prepared_input_to_queue(self):
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        input_path = self.submission_tab.prepared_input_path_input.text().strip()
        if not input_path or not os.path.isfile(input_path):
            QMessageBox.warning(self, "Input Error", "Please specify a valid prepared input file.")
            return
        # Suggest output file path
        default_out = os.path.splitext(input_path)[0] + ".out"
        output_path, _ = QFileDialog.getSaveFileName(self, "Select Output File", default_out, "Output Files (*.out);;All Files (*)")
        if not output_path:
            return
        orca_path = self.submission_tab.orca_path_input.text().strip()
        if not orca_path or not os.path.isfile(orca_path):
            QMessageBox.warning(self, "Input Error", "Please specify a valid ORCA executable path.")
            return
        # Generate a batch file for this job
        input_dir = os.path.dirname(input_path) or os.getcwd()
        bat_path = os.path.join(input_dir, f"_orca_job_{int(time.time())}.bat")
        orca_path_win = orca_path.replace('/', '\\')
        input_path_win = input_path.replace('/', '\\')
        output_path_win = output_path.replace('/', '\\')
        orca_cmd = f'{orca_path_win} {input_path_win} > {output_path_win}'
        try:
            with open(bat_path, 'w') as bat_file:
                bat_file.write(f"@echo off\n{orca_cmd}\n")
        except Exception as e:
            QMessageBox.critical(self, "Batch File Error", f"Failed to write batch file: {e}")
            return
        job = OrcaJob(input_path, output_path, bat_path, orca_path)
        self.job_queue_manager.add_job(job)
        QMessageBox.information(self, "Job Queued", f"Prepared input file has been added to the queue.")

    def _maybe_auto_submit_job(self):
        """
        Automatically submit a job when the input file is saved (Ctrl+S, File->Save, or editing finished).
        """
        input_text = self.submission_tab.output_text.toPlainText().strip()
        input_filename = self.submission_tab.input_file_path_input.text().strip()
        output_filename = self.submission_tab.output_file_path_input.text().strip()
        orca_path = self.submission_tab.orca_path_input.text().strip()
        # Only submit if all required fields are present and file exists
        if not input_text or not input_filename or not output_filename or not orca_path or not os.path.isfile(orca_path):
            return
        # Only submit if the input file was just saved
        try:
            with open(input_filename, 'r') as f:
                file_content = f.read().strip()
            if file_content != input_text:
                return  # Don't submit if file content doesn't match editor (not saved)
        except Exception:
            return
        # All checks passed, enqueue the job
        input_dir = os.path.dirname(input_filename) or os.getcwd()
        bat_path = os.path.join(input_dir, f"_orca_job_{int(time.time())}.bat")
        orca_path_win = orca_path.replace('/', '\\')
        input_filename_win = input_filename.replace('/', '\\')
        output_filename_win = output_filename.replace('/', '\\')
        orca_cmd = f'{orca_path_win} {input_filename_win} > {output_filename_win}'
        try:
            with open(bat_path, 'w') as bat_file:
                bat_file.write(
                    "@echo on\n"
                    f"echo Running: {orca_cmd}\n"
                    f"{orca_cmd}\n"
                    "echo Exit code: %errorlevel%\n"
                    "pause\n"
                )
        except Exception as e:
            QMessageBox.critical(self, "Batch File Error", f"Failed to write batch file: {e}")
            return
        job = OrcaJob(input_filename, output_filename, bat_path, orca_path)
        self.job_queue_manager.add_job(job)
        self.signals.job_submitted.emit(input_filename, output_filename)

    def _save_and_submit(self):
        input_text = self.submission_tab.output_text.toPlainText().strip()
        if not input_text:
            QMessageBox.warning(self, "Warning", "Please generate the input file first.")
            return
        orca_path = self.submission_tab.orca_path_input.text().strip()
        if not orca_path or not os.path.isfile(orca_path):
            QMessageBox.warning(self, "Input Error", "Please specify a valid ORCA executable path.")
            return
        input_filename = self.submission_tab.input_file_path_input.text().strip()
        output_filename = self.submission_tab.output_file_path_input.text().strip()
        try:
            with open(input_filename, 'w') as f:
                f.write(input_text)
        except Exception as e:
            QMessageBox.critical(self, "File Error", f"Failed to save input file: {e}")
            return
        input_dir = os.path.dirname(input_filename) or os.getcwd()
        bat_path = os.path.join(input_dir, f"_orca_job_{int(time.time())}.bat")
        # Ensure all file paths use backslashes for Windows batch
        orca_path_win = orca_path.replace('/', '\\')
        input_filename_win = input_filename.replace('/', '\\')
        output_filename_win = output_filename.replace('/', '\\')
        # Strict ORCA batch syntax: no quotes, no 2>&1
        orca_cmd = f'{orca_path_win} {input_filename_win} > {output_filename_win}'
        try:
            with open(bat_path, 'w') as bat_file:
                bat_file.write(
                    "@echo on\n"
                    f"echo Running: {orca_cmd}\n"
                    f"{orca_cmd}\n"
                    "echo Exit code: %errorlevel%\n"
                    "pause\n"
                )
        except Exception as e:
            QMessageBox.critical(self, "Batch File Error", f"Failed to write batch file: {e}")
            return
        job = OrcaJob(input_filename, output_filename, bat_path, orca_path)
        self.job_queue_manager.add_job(job)
        # Remove the information dialog, as submission is now fully automatic
        self.signals.job_submitted.emit(input_filename, output_filename)

    def _on_method_changed(self, method):
        # Show only solvation models relevant to the selected method
        if method == "xTB":
            models = self.solvation_models.get("xTB", [])
            relevant_models = {"xTB": models}
        elif method == "DFT" or method == "HF":
            models = self.solvation_models.get("Other", [])
            relevant_models = {"Other": models}
        else:
            # For semi-empirical and other methods, show no solvation models
            relevant_models = {"Other": ["None"]}
        self.solvation_tab.update_models(relevant_models, self.solvents_by_model)

    def _browse_for_input_file(self):
        from PyQt6.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Select Input File", "", "ORCA Input Files (*.inp);;All Files (*)")
        if filename:
            self.submission_tab.input_file_path_input.setText(filename)

    def _browse_for_output_file(self):
        from PyQt6.QtWidgets import QFileDialog
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
