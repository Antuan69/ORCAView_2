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

A modern GUI for the ORCA quantum chemistry package, designed to simplify the process of creating, submitting, and monitoring ORCA calculations.

## Features

- **Intuitive GUI**: A user-friendly interface built with PyQt6 for setting up calculations.
- **Integrated 3D Molecule Viewer**: Visualize molecules in 3D with a powerful viewer built on Vispy.
- **Advanced Job Queue**: Manage multiple calculations with a built-in job queue that supports submission, cancellation, and live output monitoring.
- **Structured Input Generation**: Automatically generates ORCA input files based on user selections, reducing syntax errors.
- **Portable Build**: Packaged with PyInstaller for easy distribution and use on Windows without requiring a Python installation.

## Usage

1.  Launch `ORCAView.exe`.
2.  Configure your calculation using the tabs for Method, Solvation, etc.
3.  Click 'Save and Submit' to add the job to the queue and start the calculation.
4.  Monitor job progress in the 'Job Queue' tab.


---

### July 2025 Update
- **Official ORCA 6.1 Basis Sets:** The DFT and HF basis set dropdowns now use grouped, deduplicated lists directly from the ORCA 6.1 manual (Karlsruhe def2, Ahlrichs, Pople, etc.) for full compliance and user clarity.
- **Robust Windows Job Cancellation:** Cancelling a job now kills all ORCA-related processes (orca.exe, MPI, children) using native Windows process tree termination.
- **Batch Queue Stability:** The batch job queue is fully automatic—jobs start immediately after submission, and the UI remains responsive.
