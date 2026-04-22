from pathlib import Path
import subprocess
import typing
import re


def get_lua_executable(base_path: Path, exe_name: str = 'lua') -> typing.Optional[Path]:
    for file in base_path.iterdir():
        if not file.is_file():
            continue

        if re.match(rf'^{re.escape(exe_name)}(\d+)?\.exe$', file.name, re.IGNORECASE):
            return file
    return None


def run_process(cmd: typing.List[str]):
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f'Execution error: {e}')