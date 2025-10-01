from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox, QStackedWidget, QTextEdit, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from ..method_info import DFT_FUNCTIONAL_INFO, BASIS_SET_INFO, SEMIEMPIRICAL_INFO, XTB_INFO, METHOD_RECOMMENDATIONS

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
        dft_main_layout = QVBoxLayout(self.dft_pane)
        
        # DFT controls
        dft_controls = QWidget()
        self.dft_layout = QFormLayout(dft_controls)
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
        
        dft_main_layout.addWidget(dft_controls)
        
        # DFT Information viewer - positioned right after controls
        self.dft_info_widget = self._create_info_viewer()
        dft_main_layout.addWidget(self.dft_info_widget)
        
        # Add stretch to push info viewer up
        dft_main_layout.addStretch()
        
        # Connect DFT combo boxes to info updates
        self.dft_functional_combo.currentTextChanged.connect(self._update_dft_info)
        self.dft_basis_set_combo.currentTextChanged.connect(self._update_dft_info)
        
        self.method_stack.addWidget(self.dft_pane)

        # HF pane
        self.hf_pane = QWidget()
        hf_main_layout = QVBoxLayout(self.hf_pane)
        
        # HF controls
        hf_controls = QWidget()
        self.hf_layout = QFormLayout(hf_controls)
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
        
        hf_main_layout.addWidget(hf_controls)
        
        # HF Information viewer - positioned right after controls
        self.hf_info_widget = self._create_info_viewer()
        hf_main_layout.addWidget(self.hf_info_widget)
        
        # Add stretch to push info viewer up
        hf_main_layout.addStretch()
        
        # Connect HF combo box to info updates
        self.hf_basis_set_combo.currentTextChanged.connect(self._update_hf_info)
        
        self.method_stack.addWidget(self.hf_pane)

        # Semi-Empirical pane
        self.semi_pane = QWidget()
        semi_main_layout = QVBoxLayout(self.semi_pane)
        
        # Semi-empirical controls
        semi_controls = QWidget()
        semi_layout = QFormLayout(semi_controls)
        self.semiempirical_combo = QComboBox()
        # Populate with semiempirical methods from config.py
        for method, keyword in semiempirical_methods.items():
            self.semiempirical_combo.addItem(method)
        semi_layout.addRow("Semi-Empirical Method:", self.semiempirical_combo)
        
        semi_main_layout.addWidget(semi_controls)
        
        # Semi-empirical Information viewer - positioned right after controls
        self.semi_info_widget = self._create_info_viewer()
        semi_main_layout.addWidget(self.semi_info_widget)
        
        # Add stretch to push info viewer up
        semi_main_layout.addStretch()
        
        # Connect semi-empirical combo box to info updates
        self.semiempirical_combo.currentTextChanged.connect(self._update_semi_info)
        
        self.method_stack.addWidget(self.semi_pane)

        # xTB pane
        self.xtb_pane = QWidget()
        xtb_main_layout = QVBoxLayout(self.xtb_pane)
        
        # xTB controls
        xtb_controls = QWidget()
        xtb_layout = QFormLayout(xtb_controls)
        self.xtb_combo = QComboBox()
        # Populate with xTB methods from config.py
        for method, keyword in xtb_methods.items():
            self.xtb_combo.addItem(method)
        xtb_layout.addRow("xTB Method:", self.xtb_combo)
        
        xtb_main_layout.addWidget(xtb_controls)
        
        # xTB Information viewer - positioned right after controls
        self.xtb_info_widget = self._create_info_viewer()
        xtb_main_layout.addWidget(self.xtb_info_widget)
        
        # Add stretch to push info viewer up
        xtb_main_layout.addStretch()
        
        # Connect xTB combo box to info updates
        self.xtb_combo.currentTextChanged.connect(self._update_xtb_info)
        
        self.method_stack.addWidget(self.xtb_pane)

        # Empty pane
        self.no_options_pane = QWidget()
        self.method_stack.addWidget(self.no_options_pane)

        # Connect method selection to pane switching
        self.method_combo.currentTextChanged.connect(self._on_method_changed)

    def _create_info_viewer(self):
        """Create an information viewer widget with dark theme styling."""
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 8, 0, 0)  # Small top margin for spacing
        
        # Title label
        title_label = QLabel("Method Information")
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                font-size: 11px; 
                color: #ffffff;
                background-color: transparent;
                padding: 4px 8px;
            }
        """)
        info_layout.addWidget(title_label)
        
        # Text area for information
        info_text = QTextEdit()
        info_text.setMaximumHeight(100)
        info_text.setReadOnly(True)
        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 8px;
                font-size: 10px;
                line-height: 1.3;
                color: #e0e0e0;
                selection-background-color: #0078d4;
            }
            QScrollBar:vertical {
                background-color: #2b2b2b;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #555555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666666;
            }
        """)
        info_text.setPlainText("Select a method to see detailed information about its properties, applicability, and recommendations.")
        info_layout.addWidget(info_text)
        
        # Store reference to text widget
        info_widget.text_widget = info_text
        
        return info_widget

    def _update_dft_info(self):
        """Update information display for DFT method."""
        functional = self.dft_functional_combo.currentText()
        basis_set = self.dft_basis_set_combo.currentText()
        
        info_text = ""
        
        # Skip group separators
        if functional.startswith("--") or basis_set.startswith("--"):
            return
            
        # Add functional information
        if functional in DFT_FUNCTIONAL_INFO:
            info_text += f"**{functional} Functional:**\n{DFT_FUNCTIONAL_INFO[functional]}\n\n"
        
        # Add basis set information
        if basis_set in BASIS_SET_INFO:
            info_text += f"**{basis_set} Basis Set:**\n{BASIS_SET_INFO[basis_set]}\n\n"
        
        # Add general recommendations
        info_text += "**General Recommendations:**\n"
        for application, recommendation in METHOD_RECOMMENDATIONS.items():
            if any(method in recommendation.lower() for method in [functional.lower(), basis_set.lower()]):
                info_text += f"• {application}: {recommendation}\n"
        
        if not info_text.strip():
            info_text = f"Information for {functional} functional and {basis_set} basis set is not available in the database."
        
        self.dft_info_widget.text_widget.setPlainText(info_text)

    def _update_hf_info(self):
        """Update information display for HF method."""
        basis_set = self.hf_basis_set_combo.currentText()
        
        if basis_set.startswith("--"):
            return
            
        info_text = ""
        
        # Add basis set information
        if basis_set in BASIS_SET_INFO:
            info_text += f"**{basis_set} Basis Set:**\n{BASIS_SET_INFO[basis_set]}\n\n"
        
        # Add HF-specific information
        info_text += "**Hartree-Fock Method:**\nHartree-Fock (HF) is a mean-field approximation that neglects electron correlation. "
        info_text += "It provides a good starting point for post-HF methods like MP2, CCSD(T). "
        info_text += "Generally less accurate than DFT for most chemical applications but computationally cheaper.\n\n"
        
        info_text += "**Recommendations:**\n• Use as reference for post-HF methods\n• Good for systems where correlation is less important\n• Consider DFT for better accuracy at similar cost"
        
        self.hf_info_widget.text_widget.setPlainText(info_text)

    def _update_semi_info(self):
        """Update information display for semiempirical method."""
        method = self.semiempirical_combo.currentText()
        
        info_text = ""
        
        if method in SEMIEMPIRICAL_INFO:
            info_text += f"**{method} Method:**\n{SEMIEMPIRICAL_INFO[method]}\n\n"
        
        info_text += "**Semiempirical Methods:**\nSemiempirical methods use experimental data to parameterize simplified quantum mechanical models. "
        info_text += "They are much faster than ab initio methods but less accurate and transferable.\n\n"
        
        info_text += "**Best for:**\n• Large organic molecules\n• Conformational searches\n• Preliminary screening\n• Systems with thousands of atoms"
        
        self.semi_info_widget.text_widget.setPlainText(info_text)

    def _update_xtb_info(self):
        """Update information display for xTB method."""
        method = self.xtb_combo.currentText()
        
        info_text = ""
        
        if method in XTB_INFO:
            info_text += f"**{method} Method:**\n{XTB_INFO[method]}\n\n"
        
        info_text += "**Extended Tight-Binding (xTB):**\nModern semiempirical methods with improved accuracy over traditional approaches. "
        info_text += "Include dispersion, halogen bonding, and other non-covalent interactions.\n\n"
        
        info_text += "**Best for:**\n• Very large systems (>1000 atoms)\n• Conformational sampling\n• Screening calculations\n• Systems with non-covalent interactions"
        
        self.xtb_info_widget.text_widget.setPlainText(info_text)

    def _on_method_changed(self, method):
        if method == "DFT":
            self.method_stack.setCurrentWidget(self.dft_pane)
            self._update_dft_info()  # Update info when switching to DFT
        elif method == "HF":
            self.method_stack.setCurrentWidget(self.hf_pane)
            self._update_hf_info()  # Update info when switching to HF
        elif method == "Semiempirical":
            self.method_stack.setCurrentWidget(self.semi_pane)
            self._update_semi_info()  # Update info when switching to Semi
        elif method == "xTB":
            self.method_stack.setCurrentWidget(self.xtb_pane)
            self._update_xtb_info()  # Update info when switching to xTB
        else:
            self.method_stack.setCurrentWidget(self.no_options_pane)
