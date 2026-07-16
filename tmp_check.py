import pathlib
import py_compile

root = pathlib.Path(r'c:/Users/Kenwo/OneDrive/Documents/cd password-manager')
files = sorted([p for p in (root / 'src').rglob('*.py')])
print('compiling', len(files), 'files')
for path in files:
    print('checking', path)
    py_compile.compile(str(path), doraise=True)
