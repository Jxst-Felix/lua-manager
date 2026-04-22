from pathlib import Path
import argparse

from lua_manager.config import Config
from lua_manager.utils import run_process, get_lua_executable


def main():
    parser = argparse.ArgumentParser(prog = "lua")

    parser.add_argument("script", nargs = "?", help = "Lua script")
    parser.add_argument("-v", "--version-select", help = "Lua version to use")
    parser.add_argument("-r", "--refresh", action = "store_true", help = "Refresh versions")

    parser.add_argument("--version", action = "store_true", help = "Show Lua version")

    args, unknown = parser.parse_known_args()
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
    lua_exe = get_lua_executable(base_path, "lua")

    if args.version:
        run_process([str(lua_exe), "-v"])
        return

    if args.script:
        run_process([str(lua_exe), args.script] + unknown)
    else:
        run_process([str(lua_exe)])


if __name__ == "__main__":
    main()