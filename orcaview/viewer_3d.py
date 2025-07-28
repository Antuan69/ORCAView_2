import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from rdkit import Chem
import numpy as np
from vispy import scene
from vispy import scene
from vispy.geometry import generation
from vispy.scene import visuals
from vispy.visuals.filters import ShadingFilter

from vispy.visuals.transforms import MatrixTransform

# Atom styling dictionaries (can be expanded)
atom_colors = {
    'H': (1.0, 1.0, 1.0, 1.0),   # White
    'C': (0.2, 0.2, 0.2, 1.0),   # Black
    'N': (0.0, 0.0, 1.0, 1.0),   # Blue
    'O': (1.0, 0.0, 0.0, 1.0),   # Red
    'F': (0.0, 1.0, 0.0, 1.0),   # Green
    'Cl': (0.0, 1.0, 0.0, 1.0),  # Green
    'Br': (0.6, 0.16, 0.16, 1.0), # Brown
    'I': (0.58, 0.0, 0.82, 1.0), # Indigo
    'S': (1.0, 1.0, 0.0, 1.0),   # Yellow
    'P': (1.0, 0.65, 0.0, 1.0),  # Orange
    'DEFAULT': (0.5, 0.5, 0.5, 1.0) # Grey
}

atom_radii = {
    'H': 0.37, 'C': 0.77, 'N': 0.75, 'O': 0.73,
    'F': 0.71, 'Cl': 0.99, 'Br': 1.14, 'I': 1.33,
    'S': 1.02, 'P': 1.06, 'DEFAULT': 0.6
}


class MoleculeViewer3D(QWidget):
    def __init__(self, molecule, parent=None):
        super().__init__(parent)
        self.setWindowTitle("3D Molecule Viewer (Vispy)")
        self.setLayout(QVBoxLayout())
        self.setMinimumSize(600, 400)

        self.canvas = scene.SceneCanvas(keys='interactive', bgcolor='grey')
        self.layout().addWidget(self.canvas.native)

        self.view = self.canvas.central_widget.add_view()
        self.molecule = molecule
        conformer = self.molecule.GetConformer()
        atom_positions = np.array([conformer.GetAtomPosition(i) for i in range(self.molecule.GetNumAtoms())])
        centroid = atom_positions.mean(axis=0)
        max_extent = np.linalg.norm(atom_positions - centroid, axis=1).max()

        self.view.camera = scene.TurntableCamera(fov=45, azimuth=45, elevation=30, up='z')
        self.view.camera.center = centroid
        self.view.camera.distance = max_extent * 3 if max_extent > 0 else 10

        self._render_molecule()

    def _render_molecule(self):
        conformer = self.molecule.GetConformer()
        
        atom_positions = np.array([conformer.GetAtomPosition(i) for i in range(self.molecule.GetNumAtoms())])

        # Render small spheres at atom centers for rounded bond ends
        bond_radius = 0.12
        for i, pos in enumerate(atom_positions):
            atom = self.molecule.GetAtomWithIdx(i)
            color = atom_colors.get(atom.GetSymbol(), atom_colors['DEFAULT'])
            from vispy.geometry import create_sphere
            mesh_data = create_sphere(rows=16, cols=16, radius=bond_radius)
            sphere = visuals.Mesh(vertices=mesh_data.get_vertices(),
                                  faces=mesh_data.get_faces(),
                                  color=color,
                                  parent=self.view.scene)
            shading_filter = ShadingFilter(shading='smooth', light_dir=(0.5, 0.5, -1))
            sphere.attach(shading_filter)
            sphere.transform = MatrixTransform()
            sphere.transform.translate(pos)

        # Render bonds as cylinders
        for bond in self.molecule.GetBonds():
            start_idx = bond.GetBeginAtomIdx()
            end_idx = bond.GetEndAtomIdx()
            start_pos = atom_positions[start_idx]
            end_pos = atom_positions[end_idx]

            start_atom = self.molecule.GetAtomWithIdx(start_idx)
            end_atom = self.molecule.GetAtomWithIdx(end_idx)

            # Draw cylinder from atom center to atom center (no shortening)
            bond_vector = end_pos - start_pos
            bond_length = np.linalg.norm(bond_vector)
            start_color = atom_colors.get(start_atom.GetSymbol(), atom_colors['DEFAULT'])
            end_color = atom_colors.get(end_atom.GetSymbol(), atom_colors['DEFAULT'])
            self._create_colored_bond_cylinder(start_pos, end_pos, start_color, end_color)

    def _create_colored_bond_cylinder(self, start_pos, end_pos, start_color, end_color):
        bond_vector = end_pos - start_pos
        bond_length = np.linalg.norm(bond_vector)

        # Generate a high-res cylinder for seamless appearance
        mesh_data = generation.create_cylinder(rows=40, radius=(0.12, 0.12), length=bond_length, cols=30)

        # Assign vertex colors based on z-position (seamless coloring)
        vertices = mesh_data.get_vertices()
        vertex_colors = np.ones((len(vertices), 4))
        half_length = bond_length / 2
        epsilon = 1e-6
        for i, vertex in enumerate(vertices):
            # z=0 is the base (start), z=bond_length is the tip (end)
            if vertex[2] <= half_length:
                vertex_colors[i] = start_color
            else:
                vertex_colors[i] = end_color

        bond_mesh = visuals.Mesh(
            vertices=vertices,
            faces=mesh_data.get_faces(),
            vertex_colors=vertex_colors,
            parent=self.view.scene
        )

        shading_filter = ShadingFilter(shading='smooth', light_dir=(0.5, 0.5, -1))
        bond_mesh.attach(shading_filter)

        # --- Calculate and apply the transformation ---
        default_axis = np.array([0, 0, 1])
        bond_axis = bond_vector / bond_length
        rotation_axis = np.cross(default_axis, bond_axis)
        dot_product = np.clip(np.dot(default_axis, bond_axis), -1.0, 1.0)
        rotation_angle_rad = np.arccos(dot_product)
        rotation_angle_deg = np.rad2deg(rotation_angle_rad)

        transform = MatrixTransform()
        if np.linalg.norm(rotation_axis) > 1e-6:
            rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
            transform.rotate(rotation_angle_deg, rotation_axis)
        elif np.allclose(default_axis, -bond_axis):
            transform.rotate(180, [1, 0, 0])

        transform.translate(start_pos)
        bond_mesh.transform = transform


