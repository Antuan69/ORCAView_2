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
            block_str = f"%{name}\n    {content}"
            # The %maxcore block does not have an 'end' statement
            if name.strip().lower() != "maxcore":
                block_str += "\nend"
            block_lines.append(block_str)

        # Prepare the coordinate block
        coord_header = f" * xyz {self.charge} {self.multiplicity}"
        coord_lines = [f"{atom:2s} {x:12.8f} {y:12.8f} {z:12.8f}" for atom, x, y, z in self.coordinates]
        coord_block = [coord_header] + coord_lines + ["*"]

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
