# ORCAView v2.3

A modern graphical user interface (GUI) for the [ORCA Quantum Chemistry Program](https://orcaforum.kofo.mpg.de/). ORCAView simplifies the process of creating, running, and analyzing ORCA calculations with a professional, feature-rich interface.

## Key Features

- **Intuitive Interface:** A user-friendly GUI built with PyQt6 for setting up a wide range of quantum chemistry calculations.
- **Professional Branding:** Custom ORCAView icon displayed in window title bars, taskbar, and application interface.
- **High-Performance 3D Structure Generation:** Generate low-energy, optimized 3D structures from SMILES strings at high speed using multithreading for conformer searching and optimization.
- **Enhanced 2D Depiction:** Automatically generate clean, standardized 2D molecular drawings with custom ORCAView logo displayed initially, replaced by molecule structure when parsed.
- **Coordinate Loading:** Load molecular coordinates directly from XYZ files or by pasting them into the application.
- **Job Type Support:** Includes support for a variety of job types, including Single Point, Geometry Optimization, Frequencies, and GOAT (Global Optimization).
- **Robust XYZ File Support:** Automatically infers bond connectivity from XYZ coordinate files for seamless visualization.
- **Advanced 3D Molecule Viewer:** A high-performance 3D viewer built with [Vispy](http://vispy.org/) for visualizing molecular structures. Features a trackball-style camera for unrestricted 3D rotation.
- **Enhanced Job Queue Management:**
    - Queue up multiple ORCA calculations to run sequentially without generating .bat files.
    - Monitor job status (Queued, Running, Completed, Failed, Cancelled) with real-time updates.
    - Cancel running jobs and manage the queue order.
    - Remove individual finished jobs or bulk remove all finished jobs via context menu.
    - View live output files for running calculations.
- **Flexible Input Generation:** Supports comprehensive ORCA method coverage including 80+ DFT functionals, 100+ basis sets, all ORCA 6.1 semiempirical methods, xTB methods, solvation models, and custom keywords.
- **Save Input File Only:** New option to save generated ORCA input files without submitting to job queue.
- **Custom Input Blocks:** A dedicated tab to add any of the official ORCA input blocks (%geom, %casscf, etc.) with custom keywords, providing advanced control over the calculation.
- **Ketcher Molecular Editor:** Draw molecules in a 2D editor and import them directly into the coordinates tab. The editor is launched via the "Draw Molecule (Ketcher)" button.
- **Portable Builds:** Includes a PyInstaller script to create a standalone, portable version for Windows.

## What's New in v2.3

### 🚀 **Performance & Size Optimizations**
- **Reduced Build Size:** Optimized PyInstaller configuration reduces standalone build size by 40-60% (from ~250MB to ~120-180MB)
- **Faster Startup:** Removed unused dependencies and optimized imports for quicker application launch
- **Memory Efficiency:** Eliminated unnecessary modules and improved resource management
- **Updated Dependencies:** Latest stable versions of all core libraries for better performance and security

### 🔧 **Code Quality Improvements**
- **Centralized Logging:** Replaced print statements with proper logging system for better debugging and monitoring
- **Removed Dead Code:** Eliminated unused files (`debug_viewer.py`, `job_submitter.py`) and legacy dependencies
- **Enhanced Error Handling:** Improved exception handling with proper logging levels and user feedback
- **Optimized Imports:** Cleaned up import statements and removed unused dependencies

### 📦 **Build System Enhancements**
- **Streamlined Dependencies:** Removed Pillow and other unused libraries from core requirements
- **Optimized PyInstaller:** Enhanced build configuration with selective module inclusion and UPX compression
- **Development Dependencies:** Separated build tools from runtime requirements for cleaner deployments

### 🐛 **Bug Fixes & Maintenance**
- **Removed Composite Methods:** Cleaned up job type dropdown by removing unused "Composite Methods" option
- **Improved Stability:** Better resource cleanup and error recovery mechanisms
- **Code Sanitization:** Comprehensive audit and cleanup of the entire codebase

## Previous Updates (v1.3.0)

- **UI Enhancements:**
    - The "Coordinates" tab is now the first tab, making it the default view on startup.
    - The "Draw Molecule (Ketcher)" button has been moved to the primary button row for easier access.
    - The 2D molecule depiction viewer is now centered for a more balanced and symmetrical layout.

- **Ketcher Integration & Stability:**
    - Implemented a robust, two-way communication channel to reliably fetch the SMILES string from the Ketcher editor, resolving all data transfer issues.
    - Fixed a series of bugs, including an `AttributeError` and a `NameError`, to ensure the Ketcher workflow is stable and functional.
    - Resolved a critical crash in the 3D molecule viewer by ensuring the `vispy` PyQt6 backend is correctly included in portable builds.
    - Fixed a bug that caused the application to crash when adding or updating custom input blocks.
    - Corrected the ORCA input file generator to no longer write a redundant `end` statement for the `%maxcore` block, ensuring valid input files.

- **Job Queue System & ORCA Integration:**
    - **Fixed Job Status Updates:** Job queue now properly displays real-time status changes (Queued → Running → Done/Error) with automatic UI refresh every 2 seconds.
    - **ORCA Path Selection:** Added functional "Browse..." button for ORCA executable selection with automatic path saving and validation.
    - **Enhanced Error Handling:** Improved batch file creation with comprehensive error checking, file validation, and detailed logging for ORCA execution.
    - **Memory Management:** Fixed timer cleanup to prevent memory leaks in job queue tab.
    - **Graphics Conflicts:** Added proper Vispy backend configuration to prevent conflicts between 3D viewer and molecular editor.

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

4.  **Set up Ketcher (Optional):**
    To use the Ketcher molecular editor, you must download and extract it:
    - Download `ketcher-standalone-3.4.0.zip`.
    - Unzip its contents into the `orcaview/ketcher/` directory.
    - The final structure should be `orcaview/ketcher/standalone/index.html`.
    ```

5.  **Run the application:**
    ```bash
    python main.py
    ```

## Building a Portable Version (Windows)

A portable, folder-based distribution can be created using the included `build_portable.spec` file.

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```

2.  **Run the build:**
    From the root of the project directory, run:
    ```bash
    pyinstaller build_portable.spec --noconfirm

    The build process is configured to automatically exclude `PySide6` to prevent conflicts with `PyQt6`.
    ```

3.  The complete, portable application will be located in the `dist/ORCAView` directory.


