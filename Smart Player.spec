# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['videoplayer\\main.py'],
    pathex=['videoplayer'],
    binaries=[],
    datas=[('videoplayer/assets/charsmartrewindicon.ico', '.'), ('videoplayer/assets/charsmartfowardicon.ico', '.'), ('videoplayer/assets/scenesmartforwardicon.ico', '.'), ('videoplayer/assets/scenesmartrewindicon.ico', '.'), ('videoplayer/assets/returntotimestampicon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Smart Player',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
