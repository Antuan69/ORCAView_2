from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox, QStackedWidget

class MethodTab(QWidget):
    def __init__(self, methods, dft_functionals, basis_sets, semiempirical_methods, xtb_methods, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)
        self.method_combo = QComboBox()
        self.method_combo.addItems(methods)
        layout.addRow("Method:", self.method_combo)

        self.method_stack = QStackedWidget()
        layout.addRow(self.method_stack)

        # DFT pane
        self.dft_pane = QWidget()
        self.dft_layout = QFormLayout(self.dft_pane)
        self.dft_functional_combo = QComboBox()
        # Populate with all official ORCA 6.1 DFT functionals (deduplicated)
        # Grouped by type for dropdown
        dft_functionals_grouped = {
            "Local Functionals": [
                "HFS", "LDA", "LSD", "VWN", "VWN5", "VWN3", "PWLDA"
            ],
            "GGA / meta-GGA Functionals": [
                "BP86", "BLYP", "OLYP", "GLYP", "XLYP", "PW91", "MPWPW", "MPWLYP", "PBE", "RPBE", "REVPBE", "RPW86PBE", "PWP", "B97-3C",
                "B97M-V", "B97M-D3BJ", "B97M-D4", "SCANFUNC", "RSCAN", "R2SCAN", "M06L", "TPSS", "REVTPSS", "R2SCAN-3C"
            ],
            "Hybrid Functionals": [
                "B1LYP", "B3LYP", "B3LYP/G", "O3LYP", "X3LYP", "B1P86", "B3P86", "B3PW91", "PW1PW", "MPW1PW", "MPW1LYP", "PBE0", "REVPBE0", "REVPBE38", "BHANDHLYP", "M06", "M062X", "PW6B95", "TPSSH", "TPSS0", "R2SCANH", "R2SCAN0", "R2SCAN50", "PBEH-3C", "B3LYP-3C"
            ],
            "Double-Hybrid Functionals": [
                "DSD-BLYP D3BJ", "DSD-BLYP/2013", "DSD-BLYP/2013 D3BJ", "DSD-PBEP86 D3BJ", "DSD-PBEP86/2013", "DSD-PBEP86/2013 D3BJ", "DSD-PBEB95", "DSD-PBEB95 D3BJ", "B2PLYP", "MPW2PLYP", "B2GP-PLYP", "B2K-PLYP", "B2T-PLYP", "B2NC-PLYP", "PWPB95", "PBE-QIDH", "PBE0-DH", "REVDSD-PBEP86/2021", "REVDSD-PBEP86-D4/2021", "REVDOD-PBEP86/2021", "REVDOD-PBEP86-D4/2021"
            ]
        }
        self.dft_functional_combo.clear()
        for group, items in dft_functionals_grouped.items():
            self.dft_functional_combo.addItem(f"-- {group} --")
            idx = self.dft_functional_combo.count() - 1
            self.dft_functional_combo.model().item(idx).setEnabled(False)
            self.dft_functional_combo.addItems(items)

        self.dft_basis_set_combo = QComboBox()
        # Official ORCA 6.1 basis sets
        official_basis_sets = {
            "Karlsruhe def2": [
                "def2-SVP", "def2-SV(P)", "def2-TZVP", "def2-TZVP(-f)", "def2-TZVPP", "def2-QZVP", "def2-QZVPP",
                "def2-SVPD", "def2-TZVPD", "def2-TZVPPD", "def2-QZVPD", "def2-QZVPPD",
                "ma-def2-SVP", "ma-def2-SV(P)", "ma-def2-mSVP", "ma-def2-TZVP", "ma-def2-TZVP(-f)", "ma-def2-TZVPP", "ma-def2-QZVPP"
            ],
            "Ahlrichs": [
                "SV", "SV(P)", "SVP", "TZV", "TZV(P)", "TZVP", "TZVPP", "QZVP", "QZVPP",
                "def-SV(P)", "def-SVP", "def-TZVP", "def-TZVPP", "ma-def-TZVP",
                "old-SV", "old-SV(P)", "old-SVP", "old-TZV", "old-TZV(P)", "old-TZVP", "old-TZVPP"
            ],
            "Pople": [
                "STO-3G", "3-21G", "3-21GSP", "4-22GSP", "6-31G", "6-31G*", "m6-31G", "m6-31G*", "6-31G**", "6-31G(d)", "6-31G(d,p)", "6-31G(2d)", "6-31G(2d,p)", "6-31G(2d,2p)", "6-31G(2df)", "6-31G(2df,2p)", "6-31G(2df,2pd)", "6-31+G*", "6-31+G**", "6-31+G(d)", "6-31+G(d,p)", "6-31+G(2d)", "6-31+G(2d,p)", "6-31+G(2d,2p)", "6-31+G(2df)", "6-31+G(2df,2p)", "6-31+G(2df,2pd)", "6-31++G**", "6-31++G(d,p)", "6-31++G(2d,p)", "6-31++G(2d,2p)", "6-31++G(2df,2p)", "6-31++G(2df,2pd)", "6-311G", "6-311G*", "6-311G**", "6-311G(d)", "6-311G(d,p)", "6-311G(2d)", "6-311G(2d,p)", "6-311G(2d,2p)", "6-311G(2df)", "6-311G(2df,2p)", "6-311G(2df,2pd)", "6-311G(3df)", "6-311G(3df,3pd)", "6-311+G*", "6-311+G**", "6-311+G(d)", "6-311+G(d,p)", "6-311+G(2d)", "6-311+G(2d,p)", "6-311+G(2d,2p)", "6-311+G(2df)", "6-311+G(2df,2p)", "6-311+G(2df,2pd)", "6-311+G(3df)", "6-311+G(3df,2p)", "6-311+G(3df,3pd)", "6-311++G**", "6-311++G(d,p)", "6-311++G(2d,p)", "6-311++G(2d,2p)", "6-311++G(2df,2p)", "6-311++G(2df,2pd)", "6-311++G(3df,3pd)"
            ]
        }
        for group, items in official_basis_sets.items():
            self.dft_basis_set_combo.addItem(f"-- {group} --")
            self.dft_basis_set_combo.addItems(items)

        self.dft_layout.addRow("DFT Functional:", self.dft_functional_combo)
        # DFT dispersion corrections dropdown
        self.dispersion_combo = QComboBox()
        dispersion_methods = [
            "None",  # No correction
            "D2",    # Grimme D2
            "D3",    # Grimme D3
            "D3BJ",  # Grimme D3(BJ)
            "D3ZERO",# Grimme D3(0)
            "D4",    # Grimme D4
            "VV10",  # Non-local VV10
            "NOVDW"   # Explicitly disable dispersion corrections
        ]
        self.dispersion_combo.addItems(dispersion_methods)
        self.dft_layout.addRow("Dispersion Correction:", self.dispersion_combo)
        self.dft_layout.addRow("Basis Set:", self.dft_basis_set_combo)
        self.method_stack.addWidget(self.dft_pane)

        # HF pane
        self.hf_pane = QWidget()
        self.hf_layout = QFormLayout(self.hf_pane)
        self.hf_method_combo = QComboBox()
        hf_methods = [
            "RHF",  # Restricted Hartree-Fock
            "UHF",  # Unrestricted Hartree-Fock
            "ROHF", # Restricted Open-shell Hartree-Fock
            "CASSCF", # Complete Active Space SCF
            "ROKS"   # Restricted Open-shell Kohn-Sham (for DFT, but appears in HF context)
        ]
        self.hf_method_combo.addItems(hf_methods)
        self.hf_basis_set_combo = QComboBox()
        for group, items in official_basis_sets.items():
            self.hf_basis_set_combo.addItem(f"-- {group} --")
            self.hf_basis_set_combo.addItems(items)

        self.hf_layout.addRow("HF Method:", self.hf_method_combo)
        self.hf_layout.addRow("Basis Set:", self.hf_basis_set_combo)
        self.method_stack.addWidget(self.hf_pane)

        # Semi-Empirical pane
        self.semi_pane = QWidget()
        semi_layout = QFormLayout(self.semi_pane)
        self.semiempirical_combo = QComboBox()
        # Populate with deduplicated Table 3.22 semiempirical method keywords
        semiempirical_keywords = [
            "AM1", "PM3", "MNDO", "CNDO", "INDO", "ZINDO", "NDDO"
        ]
        self.semiempirical_combo.addItems(semiempirical_keywords)
        semi_layout.addRow("Semi-Empirical Method:", self.semiempirical_combo)
        self.method_stack.addWidget(self.semi_pane)

        # xTB pane
        self.xtb_pane = QWidget()
        xtb_layout = QFormLayout(self.xtb_pane)
        self.xtb_combo = QComboBox()
        # Populate with deduplicated Table 3.25 xTB method keywords
        xtb_keywords = [
            "GFN0-xTB", "GFN1-xTB", "GFN2-xTB", "GFN-FF"
        ]
        self.xtb_combo.addItems(xtb_keywords)
        xtb_layout.addRow("xTB Method:", self.xtb_combo)
        self.method_stack.addWidget(self.xtb_pane)

        # Empty pane
        self.no_options_pane = QWidget()
        self.method_stack.addWidget(self.no_options_pane)

        # Connect method selection to pane switching
        self.method_combo.currentTextChanged.connect(self._on_method_changed)

    def _on_method_changed(self, method):
        if method == "DFT":
            self.method_stack.setCurrentWidget(self.dft_pane)
        elif method == "HF":
            self.method_stack.setCurrentWidget(self.hf_pane)
        elif method == "Semi-Empirical":
            self.method_stack.setCurrentWidget(self.semi_pane)
        elif method == "xTB":
            self.method_stack.setCurrentWidget(self.xtb_pane)
        else:
            self.method_stack.setCurrentWidget(self.no_options_pane)
