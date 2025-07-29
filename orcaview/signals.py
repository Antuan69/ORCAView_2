from PyQt6.QtCore import QObject, pyqtSignal

class AppSignals(QObject):
    # Example signals for inter-tab communication
    job_type_changed = pyqtSignal(str)
    method_changed = pyqtSignal(str)
    solvation_model_changed = pyqtSignal(str)
    coordinates_generated = pyqtSignal(str)
    input_generated = pyqtSignal(str)
    job_submitted = pyqtSignal(str, str)
    view_3d_requested = pyqtSignal(object)
