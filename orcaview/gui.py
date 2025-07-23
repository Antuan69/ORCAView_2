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
    QComboBox,
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
        self.input_layout = QFormLayout()

        self.job_type_combo = QComboBox()
        self.job_types = {
            "Single Point Energy": "SP",
            "Energy and Gradient": "EnGrad",
            "Geometry Optimization": "Opt",
            "Transition State Search": "OptTS",
            "Frequency Analysis": "Freq",
            "Molecular Dynamics": "MD",
            "Thermochemistry": "PrintThermoChem",
            "Host-Guest Docking": "Docker",
            "Energy Decomposition Analysis": "EDA"
        }
        self.job_type_combo.addItems(self.job_types.keys())
        self.job_type_combo.setCurrentText("Geometry Optimization")

        # Method Dropdown
        self.method_combo = QComboBox()
        self.methods = ["DFT", "HF", "Semi-Empirical", "xTB"]
        self.method_combo.addItems(self.methods)
        self.method_combo.currentTextChanged.connect(self._update_ui_for_method)

        # DFT Functional Dropdown
        # DFT Functional Dropdown
        self.dft_functional_combo = QComboBox()
        self.dft_functionals = {
            "LDA": ["LDA", "VWN5", "VWN3", "PWLDA"],
            "GGA": ["BP86", "BLYP", "OLYP", "GLYP", "XLYP", "PW91", "PBE", "RPBE", "REVPBE"],
            "meta-GGA": ["B97M-V", "B97M-D3BJ", "B97M-D4", "SCANFUNC", "RSCAN", "R2SCAN", "M06L", "TPSS", "REVTPSS", "R2SCAN-3C"],
            "Hybrid": ["B3LYP", "PBE0", "B1LYP", "O3LYP", "X3LYP", "BHANDHLYP", "M06", "M062X", "TPSSH"],
            "Double-Hybrid": ["B2PLYP", "mPW2PLYP", "DSD-PBEP86-D3BJ", "PWPB95"]
        }
        self._populate_dft_functionals()

        # Semi-Empirical Dropdown
        self.semiempirical_combo = QComboBox()
        self.semiempirical_methods = {
            "AM1": "AM1",
            "PM3": "PM3",
            "MNDO": "MNDO",
            "ZINDO/1": "ZINDO/1",
            "ZINDO/S": "ZINDO/S"
        }
        self.semiempirical_combo.addItems(self.semiempirical_methods.keys())

        # xTB Dropdown
        self.xtb_combo = QComboBox()
        self.xtb_methods = {
            "GFN2-xTB": "GFN2-xTB",
            "GFN1-xTB": "GFN1-xTB",
            "GFN0-xTB": "GFN0-xTB",
            "GFN-FF": "GFN-FF"
        }
        self.xtb_combo.addItems(self.xtb_methods.keys())

        # Solvation options (for xTB)
        self.solvation_model_combo = QComboBox()
        self.solvation_models = {
            "xTB": ["None", "ALPB", "DDCOSMO", "CPCMX"],
            "Other": ["None", "CPCM", "CPCMC", "SMD"]
        }
        self.solvation_model_combo.currentTextChanged.connect(self._update_solvent_dropdown)

        self.solvent_combo = QComboBox()
        self._populate_solvents()

        self.basis_set_combo = QComboBox()
        self._populate_basis_sets()

        self.keywords_input = QLineEdit("")
        self.charge_input = QSpinBox()
        self.charge_input.setValue(0)
        self.multiplicity_input = QSpinBox()
        self.multiplicity_input.setValue(1)
        self.multiplicity_input.setMinimum(1)
        self.input_layout.addRow("Job Type:", self.job_type_combo)
        self.input_layout.addRow("Method:", self.method_combo)
        self.dft_row = self.input_layout.addRow("DFT Functional:", self.dft_functional_combo)
        self.semiempirical_row = self.input_layout.addRow("Semi-Empirical Method:", self.semiempirical_combo)
        self.xtb_row = self.input_layout.addRow("xTB Method:", self.xtb_combo)
        self.solvation_model_row = self.input_layout.addRow("Solvation Model:", self.solvation_model_combo)
        self.solvent_row = self.input_layout.addRow("Solvent:", self.solvent_combo)
        self.input_layout.addRow("Basis Set:", self.basis_set_combo)
        self.input_layout.addRow("Other Keywords:", self.keywords_input)
        self.input_layout.addRow("Charge:", self.charge_input)
        self.input_layout.addRow("Multiplicity:", self.multiplicity_input)

        self.nprocs_input = QSpinBox()
        self.nprocs_input.setValue(1)
        self.nprocs_input.setMinimum(1)
        self.input_layout.addRow("Number of Processors:", self.nprocs_input)

        self.memory_input = QLineEdit("4000") # Memory in MB
        self.input_layout.addRow("Memory (MB):", self.memory_input)

        self.coordinates_input = QTextEdit("C 0.0 0.0 0.0\nH 0.0 0.0 1.09")
        self.input_layout.addRow("Coordinates (XYZ):", self.coordinates_input)

        self.layout.addLayout(self.input_layout)

        self.load_xyz_button = QPushButton("Load XYZ")
        self.load_xyz_button.clicked.connect(self._load_xyz)
        self.layout.addWidget(self.load_xyz_button)

        self._update_ui_for_method(self.method_combo.currentText())

    def _populate_basis_sets(self):
        basis_sets = {
            "Pople Style": [
                "STO-3G", "3-21G", "6-31G", "6-31G*", "6-31G**", "6-31+G*", 
                "6-31++G**", "6-311G", "6-311G*", "6-311G**", "6-311+G*", "6-311++G**"
            ],
            "Ahlrichs Style": ["SV", "SVP", "TZV", "TZVP", "TZVPP", "QZVP", "QZVPP"],
            "Karlsruhe def2": [
                "def2-SVP", "def2-SV(P)", "def2-TZVP", "def2-TZVPP", "def2-QZVP", "def2-QZVPP",
                "def2-SVPD", "def2-TZVPD", "def2-TZVPPD", "def2-QZVPD", "def2-QZVPPD"
            ],
            "Jensen PC": ["pc-1", "pc-2", "pc-3", "pc-4", "aug-pc-1", "aug-pc-2", "aug-pc-3", "aug-pc-4"],
            "Dunning CC": [
                "cc-pVDZ", "cc-pVTZ", "cc-pVQZ", "cc-pV5Z", "aug-cc-pVDZ", 
                "aug-cc-pVTZ", "aug-cc-pVQZ", "aug-cc-pV5Z"
            ],
            "ANO": ["ANO-SZ", "ANO-pVDZ", "ANO-pVTZ", "ANO-pVQZ", "ANO-pV5Z"]
        }

        for category, sets in basis_sets.items():
            self.basis_set_combo.addItem(f"--- {category} ---")
            self.basis_set_combo.addItems(sets)
        self.basis_set_combo.setCurrentText("def2-SVP")

    def _populate_dft_functionals(self):
        for category, functionals in self.dft_functionals.items():
            self.dft_functional_combo.addItem(f"--- {category} ---")
            self.dft_functional_combo.addItems(functionals)

    def _populate_solvents(self):
        cpcm_solvents = ['1,1,1-trichloroethane', '1,1,2-trichloroethane', '1,2,4-trimethylbenzene', '1,2-dibromoethane', '1,2-dichloroethane', '1,2-ethanediol', '1,4-dioxane', '1-bromo-2-methylpropane', '1-bromooctane', '1-bromopentane', '1-bromopropane', '1-butanol', '1-chlorohexane', '1-chloropentane', '1-chloropropane', '1-decanol', '1-fluorooctane', '1-heptanol', '1-hexanol', '1-hexene', '1-hexyne', '1-iodobutane', '1-iodohexadecane', '1-iodopentane', '1-iodopropane', '1-nitropropane', '1-nonanol', '1-octanol', '1-pentanol', '1-pentene', '1-propanol', '2,2,2-trifluoroethanol', '2,2,4-trimethylpentane', '2,4-dimethylpentane', '2,4-dimethylpyridine', '2,6-dimethylpyridine', '2-bromopropane', '2-butanol', '2-chlorobutane', '2-heptanone', '2-hexanone', '2-methoxyethanol', '2-methyl-1-propanol', '2-methyl-2-propanol', '2-methylpentane', '2-methylpyridine', '2-nitropropane', '2-octanone', '2-pentanone', '2-propanol', '2-propen-1-ol', 'e-2-pentene', '3-methylpyridine', '3-pentanone', '4-heptanone', '4-methyl-2-pentanone', '4-methylpyridine', '5-nonanone', 'aceticacid', 'acetone', 'acetonitrile', 'acetophenone', 'ammonia', 'aniline', 'anisole', 'benzaldehyde', 'benzene', 'benzonitrile', 'benzylalcohol', 'bromobenzene', 'bromoethane', 'bromoform', 'butanal', 'butanoicacid', 'butanone', 'butanonitrile', 'butylacetate', 'butylamine', 'n-butylbenzene', 'sec-butylbenzene', 't-butylbenzene', 'carbondisulfide', 'ccl4', 'chlorobenzene', 'chloroform', 'a-chlorotoluene', 'o-chlorotoluene', 'conductor', 'm-cresol', 'o-cresol', 'cyclohexane', 'cyclohexanone', 'cyclopentane', 'cyclopentanol', 'cyclopentanone', 'decalin', 'cis-decalin', 'n-decane', 'dibromomethane', 'dibutylether', 'o-dichlorobenzene', 'e-1,2-dichloroethene', 'z-1,2-dichloroethene', 'dichloromethane', 'diethylether', 'diethylsulfide', 'diethylamine', 'diiodomethane', 'diisopropylether', 'cis-1,2-dimethylcyclohexane', 'dimethyldisulfide', 'dimethylacetamide', 'dimethylformamide', 'dmso', 'diphenylether', 'dipropylamine', 'n-dodecane', 'ethanethiol', 'ethanol', 'ethylacetate', 'ethylmethanoate', 'ethoxybenzene', 'ethylbenzene', 'fluorobenzene', 'formamide', 'formicacid', 'furan', 'n-heptane', 'hexadecane', 'n-hexane', 'hexanoicacid', 'iodobenzene', 'iodoethane', 'iodomethane', 'isopropylbenzene', 'p-isopropyltoluene', 'mesitylene', 'methanol', 'methylbenzoate', 'methylbutanoate', 'methylethanoate', 'methylmethanoate', 'methylpropanoate', 'n-methylaniline', 'methylcyclohexane', 'n-methylformamide', 'nitrobenzene', 'nitroethane', 'nitromethane', 'o-nitrotoluene', 'n-nonane', 'n-octane', 'n-pentadecane', 'wetoctanol', 'pentanal', 'n-pentane', 'pentanoicacid', 'pentylethanoate', 'pentylamine', 'perfluorobenzene', 'phenol', 'propanal', 'propanoicacid', 'propanonitrile', 'propylethanoate', 'propylamine', 'pyridine', 'c2cl4', 'thf', 'sulfolane', 'tetralin', 'thiophene', 'thiophenol', 'toluene', 'trans-decalin', 'tributylphosphate', 'trichloroethene', 'triethylamine', 'n-undecane', 'water', 'xylene', 'm-xylene', 'o-xylene', 'p-xylene']
        smd_solvents = ['1,1,1-trichloroethane', '1,1,2-trichloroethane', '1,2,4-trimethylbenzene', '1,2-dibromoethane', '1,2-dichloroethane', '1,2-ethanediol', '1,4-dioxane', '1-bromo-2-methylpropane', '1-bromooctane', '1-bromopentane', '1-bromopropane', '1-butanol', '1-chlorohexane', '1-chloropentane', '1-chloropropane', '1-decanol', '1-fluorooctane', '1-heptanol', '1-hexanol', '1-hexene', '1-hexyne', '1-iodobutane', '1-iodohexadecane', '1-iodopentane', '1-iodopropane', '1-nitropropane', '1-nonanol', '1-octanol', '1-pentanol', '1-pentene', '1-propanol', '2,2,2-trifluoroethanol', '2,2,4-trimethylpentane', '2,4-dimethylpentane', '2,4-dimethylpyridine', '2,6-dimethylpyridine', '2-bromopropane', '2-butanol', '2-chlorobutane', '2-heptanone', '2-hexanone', '2-methoxyethanol', '2-methyl-1-propanol', '2-methyl-2-propanol', '2-methylpentane', '2-methylpyridine', '2-nitropropane', '2-octanone', '2-pentanone', '2-propanol', '2-propen-1-ol', 'e-2-pentene', '3-methylpyridine', '3-pentanone', '4-heptanone', '4-methyl-2-pentanone', '4-methylpyridine', '5-nonanone', 'aceticacid', 'acetone', 'acetonitrile', 'acetophenone', 'ammonia', 'aniline', 'anisole', 'benzaldehyde', 'benzene', 'benzonitrile', 'benzylalcohol', 'bromobenzene', 'bromoethane', 'bromoform', 'butanal', 'butanoicacid', 'butanone', 'butanonitrile', 'butylacetate', 'butylamine', 'n-butylbenzene', 'sec-butylbenzene', 't-butylbenzene', 'carbondisulfide', 'ccl4', 'chlorobenzene', 'chloroform', 'a-chlorotoluene', 'o-chlorotoluene', 'm-cresol', 'o-cresol', 'cyclohexane', 'cyclohexanone', 'cyclopentane', 'cyclopentanol', 'cyclopentanone', 'decalin', 'cis-decalin', 'n-decane', 'dibromomethane', 'dibutylether', 'o-dichlorobenzene', 'e-1,2-dichloroethene', 'z-1,2-dichloroethene', 'dichloromethane', 'diethylether', 'diethylsulfide', 'diethylamine', 'diiodomethane', 'diisopropylether', 'cis-1,2-dimethylcyclohexane', 'dimethyldisulfide', 'dimethylacetamide', 'dimethylformamide', 'dmso', 'diphenylether', 'dipropylamine', 'n-dodecane', 'ethanethiol', 'ethanol', 'ethylacetate', 'ethylmethanoate', 'ethoxybenzene', 'ethylbenzene', 'fluorobenzene', 'formamide', 'formicacid', 'furan', 'n-heptane', 'hexadecane', 'n-hexane', 'hexanoicacid', 'iodobenzene', 'iodoethane', 'iodomethane', 'isopropylbenzene', 'p-isopropyltoluene', 'mesitylene', 'methanol', 'methylbenzoate', 'methylbutanoate', 'methylethanoate', 'methylmethanoate', 'methylpropanoate', 'n-methylaniline', 'methylcyclohexane', 'n-methylformamide', 'nitrobenzene', 'nitroethane', 'nitromethane', 'o-nitrotoluene', 'n-nonane', 'n-octane', 'n-pentadecane', 'wetoctanol', 'pentanal', 'n-pentane', 'pentanoicacid', 'pentylethanoate', 'pentylamine', 'perfluorobenzene', 'phenol', 'propanal', 'propanoicacid', 'propanonitrile', 'propylethanoate', 'propylamine', 'pyridine', 'c2cl4', 'thf', 'sulfolane', 'tetralin', 'thiophene', 'thiophenol', 'toluene', 'trans-decalin', 'tributylphosphate', 'trichloroethene', 'triethylamine', 'n-undecane', 'water', 'xylene', 'm-xylene', 'o-xylene', 'p-xylene']

        self.solvents_by_model = {
            "ALPB": ["1,2,4-trimethylbenzene", "1,2-dichloroethane", "1,4-dioxane", "1-butanol", "1-chlorohexane", "1-decanol", "1-fluorooctane", "1-heptanol", "1-hexanol", "1-iodohexadecane", "1-nonanol", "1-octanol", "1-pentanol", "1-propanol", "2,2,4-trimethylpentane", "2,6-dimethylpyridine", "2-butanol", "2-methoxyethanol", "2-methyl-1-propanol", "2-methylpyridine", "2-propanol", "4-methyl-2-pentanone", "aceticacid", "acetone", "acetonitrile", "acetophenone", "aniline", "anisole", "benzaldehyde", "benzene", "benzonitrile", "benzylalcohol", "bromobenzene", "bromoethane", "bromoform", "butanone", "butylacetate", "n-butylbenzene", "sec-butylbenzene", "t-butylbenzene", "carbondisulfide", "ccl4", "chlorobenzene", "chloroform", "conductor", "m-cresol", "cyclohexane", "cyclohexanone", "decalin", "n-decane", "dibromomethane", "dibutylether", "o-dichlorobenzene", "dichloromethane", "diethylether", "diisopropylether", "dimethylacetamide", "dimethylformamide", "dmso", "diphenylether", "n-dodecane", "ethanol", "ethylacetate", "ethoxybenzene", "ethylbenzene", "fluorobenzene", "furan", "n-heptane", "hexadecane", "n-hexane", "iodobenzene", "isopropylbenzene", "p-isopropyltoluene", "mesitylene", "methanol", "n-methylformamide", "nitrobenzene", "nitroethane", "nitromethane", "o-nitrotoluene", "n-nonane", "n-octane", "n-pentadecane", "wetoctanol", "n-pentane", "perfluorobenzene", "phenol", "pyridine", "c2cl4", "thf", "sulfolane", "tetralin", "toluene", "tributylphosphate", "triethylamine", "n-undecane", "water", "xylene"],
            "DDCOSMO": ["1,4-dioxane", "1-octanol", "acetone", "acetonitrile", "aniline", "benzaldehyde", "benzene", "carbondisulfide", "chloroform", "dichloromethane", "diethylether", "dimethylformamide", "dmso", "ethanol", "ethylacetate", "hexadecane", "n-hexane", "methanol", "nitromethane", "wetoctanol", "phenol", "thf", "toluene", "water"],
            "CPCMX": ["1-octanol", "acetonitrile", "aniline", "benzene", "carbondisulfide", "chloroform", "dichloromethane", "diethylether", "dimethylformamide", "dmso", "ethanol", "ethylacetate", "hexadecane", "n-hexane", "methanol", "nitromethane", "thf", "toluene", "water"],
            "CPCM": cpcm_solvents,
            "CPCMC": cpcm_solvents,
            "SMD": smd_solvents
        }

    def _update_ui_for_method(self, method):
        is_dft = method == "DFT"
        is_semiempirical = method == "Semi-Empirical"
        is_xtb = method == "xTB"

        self.dft_functional_combo.setVisible(is_dft)
        self.input_layout.labelForField(self.dft_functional_combo).setVisible(is_dft)

        self.semiempirical_combo.setVisible(is_semiempirical)
        self.input_layout.labelForField(self.semiempirical_combo).setVisible(is_semiempirical)

        self.xtb_combo.setVisible(is_xtb)
        self.input_layout.labelForField(self.xtb_combo).setVisible(is_xtb)

        # Show solvation options for DFT, HF, and xTB
        show_solvation = is_dft or is_semiempirical or is_xtb
        self.solvation_model_combo.setVisible(show_solvation)
        self.input_layout.labelForField(self.solvation_model_combo).setVisible(show_solvation)

        current_models = []
        if is_xtb:
            current_models = self.solvation_models["xTB"]
        elif show_solvation:
            current_models = self.solvation_models["Other"]

        self.solvation_model_combo.clear()
        self.solvation_model_combo.addItems(current_models)

        self._update_solvent_dropdown(self.solvation_model_combo.currentText() if show_solvation else "None")

    def _update_solvent_dropdown(self, model):
        self.solvent_combo.clear()
        is_solvation_selected = model != "None"

        self.solvent_combo.setVisible(is_solvation_selected)
        self.input_layout.labelForField(self.solvent_combo).setVisible(is_solvation_selected)

        if is_solvation_selected:
            solvents = self.solvents_by_model.get(model, [])
            self.solvent_combo.addItems(solvents)
            if "water" in solvents:
                self.solvent_combo.setCurrentText("water")
        for category, functionals in self.dft_functionals.items():
            self.dft_functional_combo.addItem(f"--- {category} ---")
            self.dft_functional_combo.addItems(functionals)

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
        job_type = self.job_type_combo.currentText()
        method = self.method_combo.currentText()
        other_keywords = self.keywords_input.text()

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

        keyword_parts = [self.job_types.get(job_type, ""), method_keyword, basis_set_keyword, solvation_keyword, other_keywords]
        full_keywords = " ".join(part for part in keyword_parts if part).strip()

        self.generator.set_keywords(f"! {full_keywords}")

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

