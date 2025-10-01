# build_portable.spec - Complete dependencies for portable app
# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# --- Collect all necessary data files ---
datas = []

# Add application icon
datas.append(('Icon_logo.png', '.'))

# Ketcher files - include the entire ketcher directory
if os.path.exists('orcaview/ketcher'):
    datas.append(('orcaview/ketcher', 'orcaview/ketcher'))

# Vispy: Include all necessary shaders and data
datas += collect_data_files('vispy')

# PyQt6: Include all necessary plugins and data
datas += collect_data_files('PyQt6')

# PyQt6-WebEngine: Include web engine data
try:
    datas += collect_data_files('PyQt6.QtWebEngineCore')
    datas += collect_data_files('PyQt6.QtWebEngineWidgets')
except:
    pass

# RDKit: Include all data files
datas += collect_data_files('rdkit')

# Flask: Include templates and static files
datas += collect_data_files('flask')

# Hidden imports - comprehensive list
hiddenimports = [
    'PyQt6.sip',
    'PyQt6.QtTest',
    'PyQt6.QtWebEngineCore',
    'PyQt6.QtWebEngineWidgets',
    'PyQt6.QtWebChannel',
    'vispy.app.backends._pyqt6',
    'flask',
    'werkzeug',
    'jinja2',
    'markupsafe',
    'itsdangerous',
    'click',
    'blinker'
]

# Add all vispy submodules
hiddenimports += collect_submodules('vispy.visuals')
hiddenimports += collect_submodules('vispy.scene.visuals')
hiddenimports += collect_submodules('vispy.app.backends')

# Add RDKit submodules
hiddenimports += [
    'rdkit.Chem.Draw',
    'rdkit.Chem.Draw.MolDrawing',
    'rdkit.Chem.AllChem',
    'rdkit.Chem.rdDetermineBonds'
]

# Exclude only truly unnecessary modules
excludes = [
    'PySide6',
    'tkinter',
    'matplotlib',
    'IPython',
    'jupyter',
    'notebook'
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate and unnecessary files
a.datas = [x for x in a.datas if not any(exclude in x[0].lower() for exclude in [
    'test', 'example', 'demo', 'doc', 'readme', '.md', '.txt'
])]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ORCAView',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,  # Don't strip to preserve functionality
    upx=False,    # Disable UPX to avoid compatibility issues
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Icon_logo.png'  # Set application icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,   # Don't strip to preserve functionality
    upx=False,     # Disable UPX to avoid compatibility issues
    upx_exclude=[],
    name='ORCAView',
)