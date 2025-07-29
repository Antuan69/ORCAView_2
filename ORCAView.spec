# -*- mode: python ; coding: utf-8 -*-


import os
import vispy

# Get the path to the vispy package
vispy_path = os.path.dirname(vispy.__file__)

# Define the data files to be included
vispy_datas = [
    (os.path.join(vispy_path, 'glsl'), 'vispy/glsl')
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=vispy_datas,
    hiddenimports=['vispy.app.backends._pyqt6'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ORCAView',
)
