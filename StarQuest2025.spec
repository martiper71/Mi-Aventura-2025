# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Mi-Aventura-2025\\MiAventura2025.py'],
    pathex=[],
    binaries=[],
    datas=[('Mi-Aventura-2025\\imagenes', 'imagenes')],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='StarQuest2025',
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
    icon=['Mi-Aventura-2025\\icono\\icono.ico'],
)
