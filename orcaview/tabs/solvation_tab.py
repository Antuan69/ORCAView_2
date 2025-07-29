from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox

class SolvationTab(QWidget):
    def __init__(self, solvation_models, solvents_by_model, parent=None):
        super().__init__(parent)
        self.solvation_layout = QFormLayout(self)
        self.solvation_model_combo = QComboBox()
        self.solvent_combo = QComboBox()
        self.solvation_layout.addRow("Solvation Model:", self.solvation_model_combo)
        self.solvation_layout.addRow("Solvent:", self.solvent_combo)
        self.update_models(solvation_models, solvents_by_model)

    def update_models(self, solvation_models, solvents_by_model):
        self.solvation_models = solvation_models
        self.solvents_by_model = solvents_by_model
        self.solvation_model_combo.clear()
        # Populate solvation models (flatten all model names)
        models_flat = []
        for group in solvation_models.values():
            models_flat.extend(group)
        self.solvation_model_combo.addItems(models_flat)
        # Disconnect previous connections to avoid multiple triggers
        try:
            self.solvation_model_combo.currentTextChanged.disconnect()
        except Exception:
            pass
        self.solvation_model_combo.currentTextChanged.connect(self._update_solvent_combo)
        # Populate solvents for the currently selected model
        current_model = self.solvation_model_combo.currentText() if self.solvation_model_combo.count() > 0 else None
        if current_model:
            self._update_solvent_combo(current_model)

    def _update_solvent_combo(self, model):
        self.solvent_combo.clear()
        # Try to find solvents for this model
        solvents = self.solvents_by_model.get(model, [])
        # If not found, try lowercase (for xTB models)
        if not solvents:
            solvents = self.solvents_by_model.get(model.upper(), [])
        if not solvents:
            solvents = self.solvents_by_model.get(model.lower(), [])
        if not solvents:
            solvents = ["None"]
        self.solvent_combo.addItems(solvents)
