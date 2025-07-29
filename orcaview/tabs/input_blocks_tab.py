from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QPushButton, QListWidget, QLabel

class InputBlocksTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.input_blocks = {}

        # List of ORCA input blocks from the documentation
        self.block_keywords = sorted([
            "autoci", "basis", "casresp", "casscf", "chelpg", "cim", "cis", "tddft",
            "compound", "conical", "coords", "cosmors", "cpcm", "docker", "eda",
            "elprop", "eprnmr", "esd", "frag", "freq", "geom", "goat", "ice",
            "iceci", "cipsi", "irc", "lft", "loc", "mcrpa", "md", "mdci", "mecp",
            "method", "mm", "mp2", "mrcc", "mrci", "mtr", "nbo", "ndoparas", "neb",
            "numgrad", "output", "pal", "paras", "plots", "qmmm", "rel", "rocis",
            "rr", "scf", "shark", "solvator", "symmetry", "sym", "vpt2", "xtb"
        ])

        layout = QVBoxLayout(self)

        # Block selection
        selection_layout = QHBoxLayout()
        self.block_combo = QComboBox()
        self.block_combo.addItems(self.block_keywords)
        selection_layout.addWidget(QLabel("Block:"))
        selection_layout.addWidget(self.block_combo)

        # Content editor
        self.block_content_edit = QTextEdit()
        self.block_content_edit.setPlaceholderText("Enter keywords for the selected block here...")

        # Action buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add/Update Block")
        self.add_button.clicked.connect(self.add_or_update_block)
        self.remove_button = QPushButton("Remove Selected Block")
        self.remove_button.clicked.connect(self.remove_block)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        # List of added blocks
        self.added_blocks_list = QListWidget()
        self.added_blocks_list.itemClicked.connect(self.on_block_selected)

        layout.addLayout(selection_layout)
        layout.addWidget(self.block_content_edit)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("Defined Blocks:"))
        layout.addWidget(self.added_blocks_list)

    def add_or_update_block(self):
        block_name = self.block_combo.currentText()
        block_content = self.block_content_edit.toPlainText().strip()

        if not block_content:
            # If content is empty, remove the block if it exists
            if block_name in self.input_blocks:
                self.remove_block(block_name)
            return

        self.input_blocks[block_name] = block_content
        self.update_added_blocks_list()
        self.block_content_edit.clear()

    def remove_block(self):
        selected_items = self.added_blocks_list.selectedItems()
        if not selected_items: 
            return
        
        block_name_to_remove = selected_items[0].text().split(' ')[0]
        
        if block_name_to_remove in self.input_blocks:
            del self.input_blocks[block_name_to_remove]
            self.update_added_blocks_list()
            self.block_content_edit.clear()

    def on_block_selected(self, item):
        block_name = item.text().split(' ')[0]
        self.block_combo.setCurrentText(block_name)
        self.block_content_edit.setPlainText(self.input_blocks.get(block_name, ''))

    def update_added_blocks_list(self):
        self.added_blocks_list.clear()
        for block_name in sorted(self.input_blocks.keys()):
            self.added_blocks_list.addItem(f"{block_name} (...)")

    def get_input_blocks_string(self):
        full_string = ""
        for block, content in self.input_blocks.items():
            full_string += f"%{block}\n{content}\nend\n"
        return full_string
