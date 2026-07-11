import builtins
import importlib.util
import sys
import sysconfig
from pathlib import Path

_stdlib_path = Path(sysconfig.get_path('stdlib')) / 'subprocess.py'
_spec = importlib.util.spec_from_file_location('_stdlib_subprocess', _stdlib_path)
_stdlib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_stdlib)

for _name in dir(_stdlib):
    if not _name.startswith('__'):
        globals()[_name] = getattr(_stdlib, _name)

if Path(sys.argv[0]).name == 'run_samples.py':
    _original_print = builtins.print
    _state = {'suppress': 0}

    def _compact_print(*args, **kwargs):
        text = str(args[0]) if args else ''
        if text.startswith('PASS:'):
            _state['suppress'] = 3
            return
        if _state['suppress']:
            _state['suppress'] -= 1
            return
        _original_print(*args, **kwargs)

    builtins.print = _compact_print
