from pathlib import Path
import argparse

from lua_manager.config import Config
from lua_manager.utils import run_process, get_lua_executable


def main():
    print("Executing Wua")
    parser = argparse.ArgumentParser(prog = "wlua")

    parser.add_argument("script", nargs = "?", help = "Lua script")
    parser.add_argument("-v", "--version-select", help = "Lua version")
    parser.add_argument("-r", "--refresh", action = "store_true")

    parser.add_argument("--version", action = "store_true")

    args = parser.parse_args()

    config = Config()

    if args.refresh:
        config.refresh()
        print("Refreshed Lua versions.")
        return

    version = args.version_select or config.default

    if version not in config.versions:
        print(f"Version {version} not found.")
        return

    base_path = Path(config.versions[version])
    wlua_exe = get_lua_executable(base_path, "wlua")

    if args.version:
        run_process([str(wlua_exe), "-v"])
        return

    if not args.script:
        print("No script provided.")
        return

    run_process([str(wlua_exe), args.script])


if __name__ == "__main__":
    main()