from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QTextEdit, QHBoxLayout
from PyQt6.QtGui import QFont

class SubmissionTab(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        submission_layout = QFormLayout(self)

        # ORCA executable path
        path_layout = QHBoxLayout()
        self.orca_path_input = QLineEdit()
        self.orca_path_input.setText(settings.value("orca_path", ""))
        path_layout.addWidget(self.orca_path_input)
        self.orca_path_button = QPushButton("Browse...")
        path_layout.addWidget(self.orca_path_button)
        submission_layout.addRow("ORCA Executable Path:", path_layout)

        # Input File Path
        input_path_layout = QHBoxLayout()
        self.input_file_path_input = QLineEdit()
        self.input_file_path_input.setPlaceholderText("Path to save .inp file")
        input_path_layout.addWidget(self.input_file_path_input)
        self.input_file_browse_button = QPushButton("Browse...")
        input_path_layout.addWidget(self.input_file_browse_button)
        submission_layout.addRow("Input File:", input_path_layout)

        # Output File Path
        output_path_layout = QHBoxLayout()
        self.output_file_path_input = QLineEdit()
        self.output_file_path_input.setPlaceholderText("Path to save .out file")
        output_path_layout.addWidget(self.output_file_path_input)
        self.output_file_browse_button = QPushButton("Browse...")
        output_path_layout.addWidget(self.output_file_browse_button)
        submission_layout.addRow("Output File:", output_path_layout)

        # Add Prepared Input File Section
        prepared_input_layout = QHBoxLayout()
        self.prepared_input_path_input = QLineEdit()
        self.prepared_input_path_input.setPlaceholderText("Path to existing .inp file")
        prepared_input_layout.addWidget(self.prepared_input_path_input)
        self.prepared_input_browse_button = QPushButton("Browse...")
        prepared_input_layout.addWidget(self.prepared_input_browse_button)
        self.add_prepared_input_button = QPushButton("Add to Queue")
        prepared_input_layout.addWidget(self.add_prepared_input_button)
        submission_layout.addRow("Add Prepared Input File:", prepared_input_layout)

        self.generate_button = QPushButton("Generate Input")
        self.save_button = QPushButton("Save and Submit to ORCA")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier New", 10))

        submission_layout.addRow(self.generate_button)
        submission_layout.addRow(self.output_text)
        submission_layout.addRow(self.save_button)
