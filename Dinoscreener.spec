# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['screensaver.py'],
    pathex=[],
    binaries=[],
    datas=[('ui-assets','ui-assets'), ('Bungee-Regular.ttf', '.'), ('app_icon.png', '.'), ('app_icon_taskbar.png', '.'), ('app_icon_taskbar.ico', '.'), ('hourly_chime.wav', '.')],
    hiddenimports=['PyQt6.QtSvg'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
# Use Qt's newer compatible runtime at the extraction root as well.
from pathlib import Path
import PyQt6
qt_bin = Path(PyQt6.__file__).parent / 'Qt6' / 'bin'
a.binaries = [(dest, str(qt_bin / Path(src).name), kind)
              if dest.lower() in ('vcruntime140.dll', 'vcruntime140_1.dll')
              else (dest, src, kind) for dest, src, kind in a.binaries]
a.binaries += [(p.name, str(p), 'BINARY') for p in qt_bin.glob('*.dll') if p.name.lower().startswith(('msvcp', 'vcruntime', 'concrt'))]
import os
a.binaries = [(dest, os.path.join(os.environ['SystemRoot'], 'System32', 'icuuc.dll'), kind) if dest.lower() == 'icuuc.dll' else (dest, src, kind) for dest, src, kind in a.binaries]
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Dinoscreener',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon_taskbar.ico',
)
