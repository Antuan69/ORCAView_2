class OrcaInputGenerator:
    """
    A class to generate ORCA input files.
    """
    def __init__(self):
        self.keywords = []
        self.blocks = {}
        self.charge = 0
        self.multiplicity = 1
        self.coordinates = []

    def set_keywords(self, keywords):
        """
        Set the keywords for the calculation.
        Example: ['B3LYP', 'def2-SVP', 'Opt']
        """
        self.keywords = keywords

    def add_block(self, block_name, block_content):
        """
        Add a block to the input file.
        Example: add_block('pal', 'nprocs 8')
        """
        self.blocks[block_name] = block_content

    def set_charge_and_multiplicity(self, charge, multiplicity):
        """
        Set the charge and multiplicity.
        """
        self.charge = charge
        self.multiplicity = multiplicity

    def set_coordinates(self, coordinates):
        """
        Set the atomic coordinates.
        Example: [['C', 0.0, 0.0, 0.0], ['H', 0.0, 0.0, 1.09]]
        """
        self.coordinates = coordinates

    def generate_input(self):
        """
        Generate the ORCA input file string.
        """
        input_lines = []

        # Add keywords
        if self.keywords:
            input_lines.append(f"! {' '.join(self.keywords)}")

        # Add blocks
        for block_name, block_content in self.blocks.items():
            input_lines.append(f"%{block_name}")
            input_lines.append(block_content)
            input_lines.append("end")

        # Add coordinates
        input_lines.append(f"* xyz {self.charge} {self.multiplicity}")
        for atom in self.coordinates:
            line = f"  {atom[0]:<2} {atom[1]:>12.6f} {atom[2]:>12.6f} {atom[3]:>12.6f}"
            input_lines.append(line)
        input_lines.append("*")

        return "\n".join(input_lines)
