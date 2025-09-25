import sys
import os
import time
import traceback
import threading

from PyQt6.QtCore import QSettings, Qt, QBuffer
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
from .ketcher_server import run_server
from .ketcher_window import KetcherWindow

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
        self.job_queue_manager = JobQueueManager(on_update_callback=self._refresh_job_queue_tab)
        self.job_queue_tab = JobQueueTab(self.job_queue_manager)

        # Add tabs to the main tab widget
        self.tabs.addTab(self.coordinates_tab, "Coordinates")
        self.tabs.addTab(self.job_type_tab, "Job Type")
        self.tabs.addTab(self.method_tab, "Method")
        self.tabs.addTab(self.solvation_tab, "Solvation")
        self.tabs.addTab(self.advanced_options_tab, "Advanced")
        self.tabs.addTab(self.input_blocks_tab, "Input Blocks")
        self.tabs.addTab(self.submission_tab, "Submission")
        self.tabs.addTab(self.job_queue_tab, "Job Queue")

        # Menu bar
        self.menu = MainMenu(self)

        # Signals
        self.signals = AppSignals()
        self._connect_signals()

        # Internal state
        self.current_molecule = None
        self.ketcher_window = None

        # Start the Ketcher server in a background thread
        self._start_ketcher_server()
        self._on_method_changed(initial_method)

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
        self.coordinates_tab.load_from_file_button.clicked.connect(self._load_from_xyz_file)
        self.coordinates_tab.load_from_paste_button.clicked.connect(self._toggle_paste_xyz_input)
        self.coordinates_tab.view_3d_button.clicked.connect(self._open_3d_viewer)
        self.coordinates_tab.draw_molecule_button.clicked.connect(self._open_ketcher_window)
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
        self.submission_tab.orca_path_button.clicked.connect(self._browse_for_orca_executable)
        # Save ORCA path when manually entered
        self.submission_tab.orca_path_input.textChanged.connect(self._save_orca_path)

    def _browse_for_prepared_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Prepared ORCA Input File", "", "ORCA Input Files (*.inp);;All Files (*)")
        if file_path:
            self.submission_tab.prepared_input_path_input.setText(file_path)

    def _load_from_xyz_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load XYZ File", "", "XYZ Files (*.xyz);;All Files (*)")
        if not file_path:
            return
        try:
            with open(file_path, 'r') as f:
                xyz_block = f.read()
            self._process_molecule_from_xyz(xyz_block)
        except Exception as e:
            QMessageBox.critical(self, "File Error", f"Failed to read or process XYZ file.\n\nError: {e}")

    def _load_from_pasted_xyz(self):
        xyz_block = self.coordinates_tab.xyz_paste_input.toPlainText().strip()
        if not xyz_block:
            QMessageBox.warning(self, "Input Error", "The XYZ input box is empty.")
            return
        self._process_molecule_from_xyz(xyz_block)

    def _process_molecule_from_xyz(self, xyz_block):
        """A robust method to parse XYZ data (from file or paste) and update the UI."""
        try:
            # Sanitize the block and split into non-empty lines using splitlines()
            lines = [line.strip() for line in xyz_block.splitlines() if line.strip()]
            
            # If the first line is not a digit, assume it's raw coordinates
            if not lines[0].isdigit():
                num_atoms = len(lines)
                # Add the atom count and a blank comment line to create a valid XYZ block
                xyz_data_for_rdkit = f"{num_atoms}\n\n" + "\n".join(lines)
            else:
                # The first line is the atom count. The second is a comment.
                # The rest are the coordinates.
                num_atoms = int(lines[0])
                # Ensure the number of coordinate lines matches the atom count
                if len(lines) - 2 != num_atoms:
                    raise ValueError(
                        f"XYZ format error: Atom count is {num_atoms}, but {len(lines) - 2} coordinates were found."
                    )
                # Reconstruct the block to ensure it's in a standard format for RDKit
                xyz_data_for_rdkit = "\n".join(lines)

            # Create a molecule from the XYZ block. This molecule has no bonds yet.
            mol_no_bonds = Chem.MolFromXYZBlock(xyz_data_for_rdkit)
            if mol_no_bonds is None:
                raise ValueError("RDKit could not parse the XYZ data. Please check the format.")

            # Create a molecule from the XYZ block. This molecule has no bonds yet.
            mol = Chem.MolFromXYZBlock(xyz_data_for_rdkit)
            if mol is None:
                raise ValueError("RDKit could not parse the XYZ data.")

            try:
                # Determine connectivity based on atomic distances
                from rdkit.Chem import rdDetermineBonds
                rdDetermineBonds.DetermineConnectivity(mol)
                Chem.SanitizeMol(mol)
            except Exception as bond_error:
                print(f"Could not infer bonds: {bond_error}")
                # Fallback to the molecule without bonds if inference fails

            self._update_ui_with_molecule(mol)

        except Exception as e:
            QMessageBox.critical(self, "XYZ Processing Error", f"Failed to load structure from XYZ data.\n\nError: {e}")
            self.current_molecule = None
            self.coordinates_tab.mol_image_label.setText("2D depiction failed.")
            self.coordinates_tab.coordinates_input.clear()

    def _update_ui_with_molecule(self, mol):
        """Updates the coordinates tab UI with the new molecule."""
        self.current_molecule = mol

        # Update 2D depiction using a more robust method
        try:
            # Create a copy for drawing and remove hydrogens
            mol_for_drawing = Chem.Mol(mol)
            mol_for_drawing = Chem.RemoveHs(mol_for_drawing)
            pil_img = Draw.MolToImage(mol_for_drawing, size=(300, 300))
            # Convert PIL image to QPixmap
            buffer = QBuffer()
            buffer.open(QBuffer.OpenModeFlag.ReadWrite)
            pil_img.save(buffer, "PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.data(), "PNG")
            self.coordinates_tab.mol_image_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Failed to generate 2D depiction: {e}")
            self.coordinates_tab.mol_image_label.setText("2D depiction failed.")

        # Update 3D coordinates text
        xyz = Chem.MolToXYZBlock(mol)
        self.coordinates_tab.coordinates_input.setText(xyz)

    def _generate_structure_from_smiles(self):
        smiles = self.coordinates_tab.smiles_input.text()
        if not smiles:
            QMessageBox.warning(self, "Input Error", "SMILES input is empty.")
            return

        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES string")

            mol = Chem.AddHs(mol)

            # Set up multithreading parameters for conformer generation
            num_conformers = 50
            num_cores = os.cpu_count() or 1
            params = AllChem.ETKDG()
            params.numThreads = num_cores

            # Generate and optimize conformers using multithreading
            AllChem.EmbedMultipleConfs(mol, numConfs=num_conformers, params=params)
            results = AllChem.UFFOptimizeMoleculeConfs(mol, numThreads=num_cores)

            # Find the conformer with the lowest energy
            min_energy = float('inf')
            min_energy_id = -1
            for i, result in enumerate(results):
                if not result[0] and result[1] < min_energy:
                    min_energy = result[1]
                    min_energy_id = i

            # If all optimizations failed, fallback to the first conformer
            if min_energy_id == -1:
                min_energy_id = 0

            # Create a new molecule containing only the lowest-energy conformer
            final_mol = Chem.Mol(mol)
            final_mol.RemoveAllConformers()
            conf = mol.GetConformer(min_energy_id)
            final_mol.AddConformer(conf, assignId=True)

            self._update_ui_with_molecule(final_mol)

        except Exception as e:
            QMessageBox.critical(self, "SMILES Error", f"Failed to generate structure: {e}")
            self.current_molecule = None
            self.coordinates_tab.mol_image_label.setText("2D depiction failed.")
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

            orca_cmd = f'"{orca_path_win}" "{input_path_win}" > "{output_path_win}" 2>&1'
            
            with open(bat_path, 'w') as bat_file:
                bat_file.write(f'@echo off\n')
                bat_file.write(f'echo Starting ORCA calculation...\n')
                bat_file.write(f'echo ORCA Path: "{orca_path_win}"\n')
                bat_file.write(f'echo Input File: "{input_path_win}"\n')
                bat_file.write(f'echo Output File: "{output_path_win}"\n')
                bat_file.write(f'if not exist "{orca_path_win}" (\n')
                bat_file.write(f'    echo ERROR: ORCA executable not found at "{orca_path_win}"\n')
                bat_file.write(f'    exit /b 1\n')
                bat_file.write(f')\n')
                bat_file.write(f'if not exist "{input_path_win}" (\n')
                bat_file.write(f'    echo ERROR: Input file not found at "{input_path_win}"\n')
                bat_file.write(f'    exit /b 1\n')
                bat_file.write(f')\n')
                bat_file.write(f'{orca_cmd}\n')
                bat_file.write(f'set ORCA_EXIT_CODE=%ERRORLEVEL%\n')
                bat_file.write(f'echo ORCA finished with exit code: %ORCA_EXIT_CODE%\n')
                bat_file.write(f'exit /b %ORCA_EXIT_CODE%\n')

            job = OrcaJob(input_path, output_path, bat_path, orca_path)
            self.job_queue_manager.add_job(job)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Job Error", f"Failed to create and queue job: {e}")
            return False

    def _toggle_paste_xyz_input(self):
        paste_input = self.coordinates_tab.xyz_paste_input
        is_visible = paste_input.isVisible()
        paste_input.setVisible(not is_visible)

        if is_visible:
            # If it was visible, now it's hidden, so process the text
            self._load_from_pasted_xyz()
            self.coordinates_tab.load_from_paste_button.setText("Paste XYZ Coordinates")
        else:
            # If it was hidden, now it's visible
            self.coordinates_tab.load_from_paste_button.setText("Load Pasted XYZ")

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
        if not orca_path:
            QMessageBox.warning(self, "Configuration Error", "ORCA executable path is not set. Please browse for the ORCA executable in the Submission tab.")
            return
        if not os.path.isfile(orca_path):
            QMessageBox.warning(self, "Configuration Error", f"ORCA executable not found at: {orca_path}\n\nPlease browse for the correct ORCA executable in the Submission tab.")
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
        if not orca_path:
            QMessageBox.warning(self, "Configuration Error", "ORCA executable path is not set. Please browse for the ORCA executable in the Submission tab.")
            return
        if not os.path.isfile(orca_path):
            QMessageBox.warning(self, "Configuration Error", f"ORCA executable not found at: {orca_path}\n\nPlease browse for the correct ORCA executable in the Submission tab.")
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

    def _browse_for_orca_executable(self):
        """Browse for ORCA executable file."""
        filename, _ = QFileDialog.getOpenFileName(self, "Select ORCA Executable", "", "Executable Files (*.exe);;All Files (*)")
        if filename:
            self.submission_tab.orca_path_input.setText(filename)
            # Save the ORCA path to settings
            self.settings.setValue("orca_path", filename)

    def _save_orca_path(self, path):
        """Save ORCA path to settings when manually entered."""
        if path.strip():
            self.settings.setValue("orca_path", path.strip())

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

    def _start_ketcher_server(self):
        """Runs the Flask server for Ketcher in a background thread."""

        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()

    def _open_ketcher_window(self):
        """Opens the Ketcher molecular editor window."""
        if self.ketcher_window is None or not self.ketcher_window.isVisible():
            self.ketcher_window = KetcherWindow()
            self.ketcher_window.smiles_updated.connect(self._handle_smiles_from_ketcher)
            self.ketcher_window.show()
        else:
            self.ketcher_window.activateWindow()

    def _handle_smiles_from_ketcher(self, smiles):
        """Handles the SMILES string received from the Ketcher window."""
        if smiles:
            # Set the SMILES string in the coordinates tab's input field
            self.coordinates_tab.smiles_input.setText(smiles)
            # Automatically trigger the structure generation
            self.coordinates_tab.generate_from_smiles_button.click()
