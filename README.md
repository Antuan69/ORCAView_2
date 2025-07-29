# ORCAView

A modern graphical user interface (GUI) for the [ORCA Quantum Chemistry Program](https://orcaforum.kofo.mpg.de/). ORCAView simplifies the process of creating, running, and analyzing ORCA calculations.

## Key Features

- **Intuitive Interface:** A user-friendly GUI built with PyQt6 for setting up a wide range of quantum chemistry calculations.
- **Structure Generation:** Generate 3D structures directly from SMILES strings using the integrated RDKit.
- **Advanced 3D Molecule Viewer:** A high-performance 3D viewer built with [Vispy](http://vispy.org/) for visualizing molecular structures with ball-and-stick models, lighting, and smooth controls.
- **Job Queue Management:**
    - Queue up multiple ORCA calculations to run sequentially.
    - Monitor job status (Queued, Running, Completed, Failed, Cancelled).
    - Cancel running jobs and manage the queue order.
    - View live output files for running calculations.
- **Flexible Input Generation:** Supports a wide variety of ORCA methods, basis sets, solvation models, and keywords.
- **Custom Input Blocks:** A dedicated tab to add any of the official ORCA input blocks (%geom, %casscf, etc.) with custom keywords, providing advanced control over the calculation.
- **Portable Builds:** Includes a PyInstaller script to create a standalone, portable version for Windows.

## Installation and Usage

To run ORCAView from source, follow these steps:

1.  **Prerequisites:**
    -   An installation of the [ORCA Quantum Chemistry Program](https://orcaforum.kofo.mpg.de/).
    -   Python 3.9+

2.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ORCAView
    ```

3.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

## Building a Portable Version (Windows)

A portable, folder-based distribution can be created using PyInstaller. Due to dependencies on Vispy, the `.spec` file requires modification.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Generate the initial `.spec` file:**
    ```bash
    pyinstaller --name ORCAView --windowed main.py
    ```

3.  **Modify `ORCAView.spec`:**
    Make the following two changes to the generated `ORCAView.spec` file to ensure Vispy's resources are correctly packaged:
    - Add `(os.path.join(os.path.dirname(vispy.__file__), 'glsl'), 'vispy/glsl')` to the `datas` list.
    - Add `'vispy.app.backends._pyqt6'` to the `hiddenimports` list.

4.  **Run the build:**
    From the root of the project directory, run:
    ```bash
    pyinstaller ORCAView.spec --noconfirm
    ```

5.  The complete, portable application will be located in the `dist/ORCAView` directory.


