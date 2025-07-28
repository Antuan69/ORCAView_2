import pyvista as pv
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

# --- Atom Styling ---
atom_colors = {
    'H': '#FFFFFF', 'C': '#222222', 'N': '#0000FF', 'O': '#FF0000',
    'F': '#00FF00', 'Cl': '#00FF00', 'Br': '#A52A2A', 'I': '#9400D3',
    'S': '#FFFF00', 'P': '#FFA500', 'B': '#FA8072', 'Si': '#DAA520',
    'DEFAULT': '#808080' # Grey for others
}

atom_radii = {
    'H': 0.37, 'C': 0.77, 'N': 0.75, 'O': 0.73,
    'F': 0.71, 'Cl': 0.99, 'Br': 1.14, 'I': 1.33,
    'S': 1.02, 'P': 1.06, 'B': 0.82, 'Si': 1.11,
    'DEFAULT': 0.6
}

def render_molecule_standalone(molecule):
    """Renders a molecule in a standalone PyVista window."""
    plotter = pv.Plotter(lighting='none')
    plotter.set_background('grey')

    # Add a custom light
    light = pv.Light(position=(10, 10, 10), intensity=1.5)
    plotter.add_light(light)

    conformer = molecule.GetConformer()

    # Render atoms
    for atom in molecule.GetAtoms():
        idx = atom.GetIdx()
        pos = conformer.GetAtomPosition(idx)
        symbol = atom.GetSymbol()
        color = atom_colors.get(symbol, atom_colors['DEFAULT'])
        radius = atom_radii.get(symbol, atom_radii['DEFAULT'])

        sphere = pv.Sphere(center=(pos.x, pos.y, pos.z), radius=radius)
        sphere.compute_normals(inplace=True, cell_normals=False, point_normals=True)
        plotter.add_mesh(
            sphere, color=color, smooth_shading=True, pbr=True, metallic=0.4, roughness=0.5
        )

    # Render bonds
    for bond in molecule.GetBonds():
        start_atom_idx = bond.GetBeginAtomIdx()
        end_atom_idx = bond.GetEndAtomIdx()
        pos1 = conformer.GetAtomPosition(start_atom_idx)
        pos2 = conformer.GetAtomPosition(end_atom_idx)
        start_pos = [pos1.x, pos1.y, pos1.z]
        end_pos = [pos2.x, pos2.y, pos2.z]

        stick = pv.Cylinder(
            center=(np.array(start_pos) + np.array(end_pos)) / 2,
            direction=np.array(end_pos) - np.array(start_pos),
            radius=0.08,
            height=np.linalg.norm(np.array(end_pos) - np.array(start_pos)),
        )
        stick.compute_normals(inplace=True, cell_normals=False, point_normals=True)
        plotter.add_mesh(stick, color='grey', smooth_shading=True, pbr=True, metallic=0.2, roughness=0.5)

    print("Showing standalone plot...")
    plotter.show()

if __name__ == '__main__':
    # Create a simple molecule (methane)
    smiles = 'C'
    mol = Chem.MolFromSmiles(smiles)
    mol_with_h = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol_with_h, AllChem.ETKDG())
    
    render_molecule_standalone(mol_with_h)
