# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['auswertung.py'],
             pathex=[],
             binaries=[],
             datas=[('./ui/logo.ico', '.'),('./ui/title.png', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
splash=Splash('gesamt.png',
				binaries=a.binaries,
				datas=a.datas,
				text_pos=(10, 50),
				text_size=12,
				text_color='white')
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
		  splash,
		  splash.binaries,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='auswertung',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='./ui/logo.ico' )
