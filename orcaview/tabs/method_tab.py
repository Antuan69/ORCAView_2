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
        self.dft_functional_combo.clear()
        for group, items in dft_functionals.items():
            self.dft_functional_combo.addItem(f"-- {group} --")
            idx = self.dft_functional_combo.count() - 1
            self.dft_functional_combo.model().item(idx).setEnabled(False)
            self.dft_functional_combo.addItems(items)

        self.dft_basis_set_combo = QComboBox()
        # Use basis sets from config.py
        for group, items in basis_sets.items():
            self.dft_basis_set_combo.addItem(f"-- {group} --")
            idx = self.dft_basis_set_combo.count() - 1
            self.dft_basis_set_combo.model().item(idx).setEnabled(False)
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
        for group, items in basis_sets.items():
            self.hf_basis_set_combo.addItem(f"-- {group} --")
            idx = self.hf_basis_set_combo.count() - 1
            self.hf_basis_set_combo.model().item(idx).setEnabled(False)
            self.hf_basis_set_combo.addItems(items)

        self.hf_layout.addRow("HF Method:", self.hf_method_combo)
        self.hf_layout.addRow("Basis Set:", self.hf_basis_set_combo)
        self.method_stack.addWidget(self.hf_pane)

        # Semi-Empirical pane
        self.semi_pane = QWidget()
        semi_layout = QFormLayout(self.semi_pane)
        self.semiempirical_combo = QComboBox()
        # Populate with semiempirical methods from config.py
        for method, keyword in semiempirical_methods.items():
            self.semiempirical_combo.addItem(method)
        semi_layout.addRow("Semi-Empirical Method:", self.semiempirical_combo)
        self.method_stack.addWidget(self.semi_pane)

        # xTB pane
        self.xtb_pane = QWidget()
        xtb_layout = QFormLayout(self.xtb_pane)
        self.xtb_combo = QComboBox()
        # Populate with xTB methods from config.py
        for method, keyword in xtb_methods.items():
            self.xtb_combo.addItem(method)
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
        elif method == "Semiempirical":
            self.method_stack.setCurrentWidget(self.semi_pane)
        elif method == "xTB":
            self.method_stack.setCurrentWidget(self.xtb_pane)
        else:
            self.method_stack.setCurrentWidget(self.no_options_pane)
