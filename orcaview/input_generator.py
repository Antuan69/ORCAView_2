class OrcaInputGenerator:
    def __init__(self):
        self.keywords = []
        self.charge = 0
        self.multiplicity = 1
        self.coordinates = []
        self.blocks = {}

    def set_keywords(self, keywords):
        """Sets the main keywords for the simple input line."""
        self.keywords = keywords

    def set_charge_and_multiplicity(self, charge, multiplicity):
        """Sets the charge and spin multiplicity."""
        self.charge = charge
        self.multiplicity = multiplicity

    def set_coordinates(self, coordinates):
        """Sets the atomic coordinates."""
        self.coordinates = coordinates

    def add_block(self, block_name, content):
        """Adds a block like %pal or %maxcore."""
        self.blocks[block_name.lower()] = content

    def generate_input(self):
        """Generates the full ORCA input file content as a string."""
        # Start with the simple keyword line
        keyword_line = f"! {' '.join(self.keywords)}"

        # Add any blocks
        block_lines = []
        for name, content in self.blocks.items():
            block_lines.append(f"%{name}\n    {content}\nend")

        # Prepare the coordinate block
        coord_header = f" * xyz {self.charge} {self.multiplicity}"
        coord_lines = [f"{atom:2s} {x:12.8f} {y:12.8f} {z:12.8f}" for atom, x, y, z in self.coordinates]
        coord_block = [coord_header] + coord_lines + ["*"]

        # Assemble the final input
        # Assemble the final input
        final_input_parts = [keyword_line]
        if block_lines:
            final_input_parts.append("\n".join(block_lines))

        # Add the coordinate block, ensuring it's separated by a blank line
        final_input_parts.append("\n".join(coord_block))

        # Join the main sections first, then join with the coordinate block
        # This provides explicit control and guarantees the blank line.
        main_section = "\n\n".join(final_input_parts[:-1])
        coord_section = final_input_parts[-1]
        return f"{main_section}\n\n{coord_section}"

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
            input_lines.append("")  # Add empty line before each block
            input_lines.append(f"%{block_name}")
            input_lines.append(block_content)
            if block_name.strip().lower() != "maxcore":
                input_lines.append("end")


        # Always ensure a blank line before the coordinate block
        if input_lines and input_lines[-1].strip() != '':
            input_lines.append("")
        input_lines.append(f"* xyz {self.charge} {self.multiplicity}")
        for atom in self.coordinates:
            line = f"  {atom[0]:<2} {atom[1]:>12.6f} {atom[2]:>12.6f} {atom[3]:>12.6f}"
            input_lines.append(line)
        input_lines.append("*")

        # Join and strip any trailing blank lines
        result = "\n".join(input_lines).rstrip() + "\n"
        return result
