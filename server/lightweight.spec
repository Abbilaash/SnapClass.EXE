# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['desktop_app.py'],
    pathex=['.venv/Lib/site-packages'],
    binaries=[],
    datas=[
        # Only include essential files, NOT the heavy model folders
        ('templates', 'templates'),
        ('static', 'static'),
        
        # Python modules that need to be included
        ('app.py', '.'),
        ('trans.py', '.'),
        ('stt.py', '.'),
        ('pdf_reader.py', '.'),
        ('question_gen.py', '.'),
        ('slm_analyse.py', '.'),
        ('utils.py', '.'),
        ('setup.py', '.'),
        
        # Configuration files
        ('*.json', '.'),
        ('*.txt', '.'),
    ],
    hiddenimports=[
        # Flask and web framework
        'flask',
        'werkzeug',
        'jinja2',
        
        # AI/ML libraries (these will be loaded from external folders)
        'torch',
        'transformers',
        'librosa',
        'numpy',
        'PIL',
        'pdf2image',
        'pytesseract',
        
        # Custom modules
        'app',
        'trans',
        'stt',
        'pdf_reader',
        'question_gen',
        'slm_analyse',
        'utils',
        'setup',
        'llama3.chat',
        
        # Additional hidden imports (simplified - modules will be copied directly)
        'torch.nn',
        'torch.optim',
        'torch.utils.data',
        'librosa.core',
        'librosa.feature',
        'numpy.core',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'pdf2image.pdf2image',
        'pytesseract.pytesseract',
        
        # Flask extensions
        'flask.ext',
        'flask.cli',
        'flask.json',
        'flask.templating',
        'flask.static',
        
        # Additional dependencies
        'requests',
        'yaml',
        'json',
        'subprocess',
        'threading',
        'socket',
        'webbrowser',
        'customtkinter',
        'tkinter',
        'queue',
        'datetime',
        'os',
        'sys',
        'time',
        'signal',
        'argparse',
        'collections',
        'io',
        're',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Create the executable
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SnapClass',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
