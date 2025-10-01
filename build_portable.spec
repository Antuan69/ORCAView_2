# build_portable.spec - Optimized for smaller size
# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# --- Collect only essential data files ---
datas = []
# Vispy: Only essential shaders and data
datas += collect_data_files('vispy', includes=['**/*.vert', '**/*.frag', '**/*.glsl'])

# PyQt6: Only platform plugins
datas += collect_data_files('PyQt6', includes=['Qt6/plugins/platforms/*'])

# RDKit: Only essential data files
datas += collect_data_files('rdkit', includes=['**/*.txt', '**/*.mol'])

# Hidden imports - minimized list
hiddenimports = [
    'PyQt6.sip',
    'vispy.app.backends._pyqt6',
    'vispy.visuals.line',
    'vispy.visuals.markers',
    'vispy.visuals.mesh',
    'vispy.scene.visuals.line',
    'vispy.scene.visuals.markers', 
    'vispy.scene.visuals.mesh'
]

# Exclude unnecessary modules to reduce size
excludes = [
    'PySide6',
    'tkinter',
    'matplotlib',
    'IPython',
    'jupyter',
    'notebook',
    'scipy',
    'pandas',
    'PIL.ImageQt',
    'PyQt6.QtMultimedia',
    'PyQt6.QtMultimediaWidgets',
    'PyQt6.QtBluetooth',
    'PyQt6.QtNfc',
    'PyQt6.QtPositioning',
    'PyQt6.QtSensors',
    'PyQt6.QtSerialPort',
    'PyQt6.QtSql',
    'PyQt6.QtTest',
    'PyQt6.QtXml'
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
    strip=True,  # Strip debug symbols
    upx=True,    # Compress with UPX
    console=False,
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
    strip=True,   # Strip debug symbols from binaries
    upx=True,     # Compress binaries with UPX
    upx_exclude=[
        'vcruntime140.dll',
        'msvcp140.dll',
        'api-ms-win-*.dll'
    ],
    name='ORCAView',
)