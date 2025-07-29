# ORCAView

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
- **No PyVista Dependency:** The 3D viewer is now Vispy-only. PyVista is no longer required or supported.
- **requirements.txt is current** and matches all features.
- **All jobs are launched via batch files** for maximum compatibility with Windows and ORCA's official recommendations.

---

ORCAView is a powerful PyQt6 desktop application for molecular visualization, editing, and automated ORCA quantum chemistry job submission with advanced batch queue management.

## Features

- **Ketcher Integration**: Draw and edit molecules using the Ketcher web-based editor embedded in the app.
- **RDKit Backend**: SMILES parsing, 3D coordinate generation, and pre-optimization.
- **2D and 3D Visualization**: View molecules in 2D and interactive 3D.
- **Advanced 3D Rendering**: Vispy-based viewer with smooth tube/cylinder bonds and rounded, lit end-caps (no PyVista required).
- **Official Basis Set Dropdowns**: DFT and HF basis set selectors now present all official ORCA 6.1 basis sets, grouped by family (Karlsruhe def2, Ahlrichs, Pople, etc.) for clarity and accuracy.
- **Batch Job Queue System**: Queue multiple ORCA jobs for sequential execution. Jobs are launched via robust Windows batch files for maximum compatibility.
- **Queue UI Controls**: View queued, running, and completed jobs. Cancel or reorder jobs interactively from the GUI.
- **Full Logging and Diagnostics**: All job launches and errors are logged for easy troubleshooting.

## Dependencies

- PyQt6
- PyQt6-WebEngine
- Flask
- numpy < 2.0
- rdkit-pypi
- Pygments
- vispy

## Usage

### Application
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python main.py
   ```
3. Use the Ketcher editor to draw a molecule and generate a 3D structure.
4. Submit ORCA jobs via the GUI. Jobs are queued and processed one-by-one.
5. Monitor job progress, cancel, or reorder jobs in the "Job Queue" tab.

### ORCA Job Submission (Windows)
- Jobs are submitted by generating a temporary batch file that launches ORCA with the correct environment and working directory.
- All paths use Windows backslashes for compatibility.
- Input files are generated with correct ORCA block formatting (no 'end' for %maxcore; all other blocks properly closed).

### Troubleshooting
- If a job fails:
  - Check the job's output and error logs in the GUI or in the output files.
  - Common errors include input geometry mismatches (see below).
  - Try running the generated batch file manually to isolate environment issues.
- If the UI does not update after a job finishes, switch tabs or submit a new job to refresh.

### Advanced Usage & Known Issues
- **Input Geometry Mismatch**: If you see errors like `Input geometry does not match current geometry`, ensure you are not referencing restart files or old `.gbw` files. Delete old scratch/restart files before rerunning.
- **Queue Robustness**: The batch queue system is thread-safe and will not deadlock the UI. All job processing is handled in a background thread.
- **No PyVista**: The 3D viewer is now fully Vispy-based. PyVista is no longer required or supported.

## Contribution & Development
- All source code is in the `orcaview` directory.
- Requirements are listed in `requirements.txt`.
- For bug reports or feature requests, open an issue or pull request on GitHub.

---

ORCAView is a modern, user-friendly interface for quantum chemistry workflows, making it easy to go from drawn molecule to completed ORCA calculation, with full batch automation and diagnostics.

## Features

- **SMILES to 3D Structure:** Instantly generate a 3D molecular structure from a SMILES string using RDKit.
- **2D Depiction:** View a 2D image of the generated molecule.
- **Customizable Input:** Easily set keywords, calculation methods (DFT, HF, xTB, etc.), basis sets, charge, multiplicity, and solvation models.
- **File Management:** Use the file browser to specify exact save locations for your input (`.inp`) and output (`.out`) files.
- **Direct Submission:** Launch ORCA calculations directly from the GUI with a single click.
- **Syntax Highlighting:** The generated input file text is highlighted for better readability.

## Setup and Installation

1.  **Prerequisites:**
    -   Python 3.x
    -   ORCA quantum chemistry software installed and accessible on your system.

2.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ORCAView
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  Launch the application:
    ```bash
    python main.py
    ```

2.  **Provide ORCA Path:** Use the "Browse..." button to select the path to your ORCA executable (e.g., `C:/orca/orca.exe`).

3.  **Generate a Structure:**
    -   Enter a SMILES string (e.g., `CCO` for ethanol) into the SMILES input field.
    -   Click "Generate Structure from SMILES".

4.  **Customize Calculation:**
    -   Adjust keywords, job type, method, charge, etc. as needed.
    -   Click "Generate Input" to see the complete ORCA input file.

5.  **Save and Submit:**
    -   Use the "Browse..." buttons to choose save locations for your input and output files.
    -   Click "Save and Submit to ORCA" to start the calculation.

ORCAView is a graphical user interface (GUI) built with Python and PyQt6 to help computational chemists build and manage input files for the ORCA quantum chemistry package.

## Features

- **Intuitive Tabbed Interface**: The UI is organized into three main tabs for a clear workflow:
  - **Job Type**: Select the overall type of calculation (e.g., Single Point, Geometry Optimization, Frequency Analysis).
  - **Method**: Choose the computational method (DFT, HF, Semi-Empirical, xTB) and specify method-specific options like DFT functionals and basis sets.
  - **Solvation**: Apply solvation models (CPCM, SMD) and select from a list of available solvents.
- **Dynamic UI**: The interface intelligently updates to show only the relevant options for the selected method and solvation model.
- **Advanced Options**: Easily specify charge, multiplicity, number of processors, and memory allocation.
- **Coordinate Editor**: A simple text box for pasting or typing molecular coordinates in XYZ format.
- **Syntax Highlighting**: The generated ORCA input is displayed with syntax highlighting for improved readability.
- **File Management**: Save the generated input file or (in a future update) submit it directly to a job queue.
- **Settings**: Configure the path to the ORCA executable.

## How to Run

1.  **Install Dependencies**: Make sure you have Python installed. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Launch the Application**:
    ```bash
    python main.py
    ```

A graphical user interface for building and submitting ORCA quantum chemistry calculations.

## Features

*   **Easy-to-use Interface**: A user-friendly GUI built with PyQt6 to simplify the creation of ORCA input files.
*   **Job Type Selection**: Dropdown menu to select the type of calculation (e.g., Optimization, Transition State Search, Single Point).
*   **Method Selection**: Support for a wide range of computational methods, including:
    *   DFT (Density Functional Theory)
    *   Hartree-Fock (HF)
    *   Semi-Empirical methods
    *   xTB (Extended Tight-Binding)
*   **Basis Set and Functional Selection**: Dropdowns populated with basis sets and DFT functionals from the ORCA 6.1 manual.
*   **Advanced Solvation Modeling**:
    *   Support for multiple solvation models: C-PCM, CPCMC, and SMD for DFT/HF methods.
    *   Specialized solvation models for xTB: ALPB, DDCOSMO, CPCMX.
    *   Dynamic solvent dropdowns populated with extensive lists of solvents for each model.
*   **Molecule Loading**: Load molecular geometries from `.xyz` files.
*   **Input File Generation**: Automatically generates ORCA input files based on user selections.
*   **Syntax Highlighting**: The generated input file is displayed with syntax highlighting for better readability.
*   **Cross-Platform**: Runs on any platform that supports Python and PyQt6.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd ORCAView
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the application:
    ```bash
    python main.py
    ```
2.  Use the GUI to select your desired calculation parameters.
3.  Load a molecule from an `.xyz` file.
4.  The ORCA input will be generated in the text box.
5.  Save the generated input to a file.

ORCAView is a user-friendly graphical interface designed to simplify the process of creating input files for the ORCA quantum chemistry package and managing computational jobs.

## Features

- **Intuitive Input Builder**: A straightforward interface for constructing complex ORCA input files.
- **Method Selection**: Choose from a wide range of computational methods, including:
    - DFT (with a comprehensive list of functionals)
    - Hartree-Fock (HF)
    - Semi-Empirical methods
    - GFN-xTB methods
- **Basis Set Library**: A categorized selection of popular basis sets (Pople, Ahlrichs, Karlsruhe, Jensen, Dunning, ANO).
- **Job Type Control**: Easily specify the calculation type (e.g., Single Point, Geometry Optimization, Frequencies).
- **xTB Solvation**: Apply implicit solvation models (ALPB, DDCOSMO, CPCMX) for xTB calculations with a dynamic list of available solvents.
- **Resource Management**: Configure the number of processors and memory allocation for your job.
- **Molecule Loading**: Load molecular coordinates directly from `.xyz` files.
- **Syntax Highlighting**: The generated input file is displayed with syntax highlighting for better readability.
- **Job Submission**: Save the input file and submit the ORCA job directly from the application.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd ORCAView
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python main.py
    ```
