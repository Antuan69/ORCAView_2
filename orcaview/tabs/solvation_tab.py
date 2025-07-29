from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox

from orcaview.config import SOLVENTS_BY_MODEL

class SolvationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QFormLayout(self)

        self.solvation_model_combo = QComboBox()
        self.solvent_combo = QComboBox()

        self.layout.addRow("Solvation Model:", self.solvation_model_combo)
        self.layout.addRow("Solvent:", self.solvent_combo)

        # Define which models are available for each method
        self.models_for_method = {
            "dft": ["None", "ALPB", "CPCM", "SMD"],
            "hf": ["None", "ALPB", "CPCM", "SMD"],
            "semiempirical": ["None", "ALPB", "CPCM", "SMD"],
            "xtb": ["None", "ALPB", "ddCOSMO", "CPCMX"],
            "other": ["None", "ALPB", "CPCM", "SMD"]
        }

        self.solvation_model_combo.currentTextChanged.connect(self.update_solvent_list)
        self.update_method("other") # Initialize with default

    def update_method(self, method_name):
        method_key = method_name.lower()
        # Fallback to 'other' if the specific method is not defined
        available_models = self.models_for_method.get(method_key, self.models_for_method["other"])

        current_model = self.solvation_model_combo.currentText()

        self.solvation_model_combo.blockSignals(True)
        self.solvation_model_combo.clear()
        self.solvation_model_combo.addItems(available_models)
        self.solvation_model_combo.blockSignals(False)

        # Restore selection if possible
        if current_model in available_models:
            self.solvation_model_combo.setCurrentText(current_model)
        else:
            self.solvation_model_combo.setCurrentIndex(0) # Default to 'None' or first available

        # Manually trigger update for solvent list
        self.update_solvent_list(self.solvation_model_combo.currentText())

    def update_solvent_list(self, model_name):
        self.solvent_combo.clear()
        if model_name and model_name != "None":
            solvents = SOLVENTS_BY_MODEL.get(model_name, [])
            self.solvent_combo.addItems(solvents)
            self.solvent_combo.setEnabled(True)
        else:
            self.solvent_combo.setEnabled(False)

    def get_selected_options(self):
        model = self.solvation_model_combo.currentText()
        solvent = self.solvent_combo.currentText()
        if model == "None":
            return {}
        return {"solvation_model": model, "solvent": solvent}
