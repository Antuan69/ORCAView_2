# ORCAView

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
