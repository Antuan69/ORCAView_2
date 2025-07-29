# ORCAView

A modern graphical user interface (GUI) for the [ORCA Quantum Chemistry Program](https://orcaforum.kofo.mpg.de/). ORCAView simplifies the process of creating, running, and analyzing ORCA calculations.

## Key Features

- **Intuitive Interface:** A user-friendly GUI built with PyQt6 for setting up a wide range of quantum chemistry calculations.
- **Integrated 2D/3D Molecule Editor:**
    - Draw molecules in 2D using the embedded [Ketcher](https://lifescience.opensource.epam.com/ketcher/index.html) editor.
    - Generate 3D structures from SMILES strings with RDKit-based optimization.
- **Advanced 3D Molecule Viewer:** A high-performance 3D viewer built with [Vispy](http://vispy.org/) for visualizing molecular structures with ball-and-stick models, lighting, and smooth controls.
- **Job Queue Management:**
    - Queue up multiple ORCA calculations to run sequentially.
    - Monitor job status (Queued, Running, Completed, Failed, Cancelled).
    - Cancel running jobs and manage the queue order.
    - View live output files for running calculations.
- **Flexible Input Generation:** Supports a wide variety of ORCA methods, basis sets, solvation models, and keywords.
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

A portable, folder-based distribution can be created using the included PyInstaller spec file.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the build script:**
    From the root of the project directory, run:
    ```bash
    pyinstaller build_portable.spec
    ```

3.  The complete, portable application will be located in the `dist/ORCAView` directory.

## July 2025 Update
- **Official ORCA 6.1 Solvent & Basis Set Support:** The solvent lists for CPCM and SMD, and the basis set dropdowns for DFT and HF, now use the official, comprehensive lists from the ORCA 6.1 manual for full compliance and user clarity.
- **Robust Windows Job Cancellation:** Cancelling a job now kills all ORCA-related processes (orca.exe, MPI, children) using native Windows process tree termination.
- **Batch Queue Stability:** The batch job queue is fully automatic—jobs start immediately after submission, and the UI remains responsive.
