import sys
from PyQt6.QtWidgets import QDialog, QVBoxLayout
from PyQt6.QtCore import Qt
import pyvista as pv
from pyvistaqt import QtInteractor
import numpy as np

# A simple dictionary for atomic radii and colors (can be expanded)
ATOM_STYLES = {
    'H': {'radius': 0.35, 'color': 'white'},
    'C': {'radius': 0.7, 'color': 'black'},
    'N': {'radius': 0.65, 'color': 'blue'},
    'O': {'radius': 0.6, 'color': 'red'},
    'F': {'radius': 0.5, 'color': 'lightgreen'},
    'S': {'radius': 1.0, 'color': 'yellow'},
    'Cl': {'radius': 1.0, 'color': 'green'},
    # Add more elements as needed
}
DEFAULT_STYLE = {'radius': 0.8, 'color': 'gray'}

class MoleculeViewer3D(QDialog):
    def __init__(self, coordinates, parent=None):
        super().__init__(parent)
        self.setWindowTitle("3D Molecule Viewer")
        self.setLayout(QVBoxLayout())
        self.setMinimumSize(600, 400)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.plotter = QtInteractor(self)
        self.layout().addWidget(self.plotter.interactor)

        self.plotter.set_background('grey')

        self.coordinates = coordinates
        self._render_molecule()

    def _render_molecule(self):
        self.plotter.clear()

        if not self.coordinates:
            return

        for atom, x, y, z in self.coordinates:
            style = ATOM_STYLES.get(atom.upper(), DEFAULT_STYLE)
            sphere = pv.Sphere(radius=style['radius'], center=(x, y, z))
            self.plotter.add_mesh(sphere, color=style['color'])

        self.plotter.camera_position = 'xy'
        self.plotter.reset_camera()
