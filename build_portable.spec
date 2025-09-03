# build_portable.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# --- Collect all necessary data files and hidden imports ---
# This ensures all plugins, shaders, fonts, and DLLs are included.
datas = []
# Vispy: Include GLSL shaders, fonts, and any other data.
datas += collect_data_files('vispy', include_py_files=True)

# PyQt6: Ensure all Qt plugins (especially platform plugins) are found.
datas += collect_data_files('PyQt6', include_py_files=True)

# RDKit: RDKit needs its data files to function correctly.
datas += collect_data_files('rdkit', include_py_files=True)

# Hidden imports for libraries that PyInstaller might miss.
hiddenimports = [
    'PyQt6.sip',
    'vispy.app.backends._pyqt6',
    'rdkit.Chem.Draw.MolDrawing',
] 
hiddenimports += collect_submodules('vispy.visuals')
hiddenimports += collect_submodules('vispy.scene.visuals')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide6'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ORCAView',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Set to True for debugging, False for release
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ORCAView',
)