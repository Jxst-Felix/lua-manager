from pathlib import Path
import argparse

from lua_manager.config import Config


def main():
    parser = argparse.ArgumentParser(prog = "lua-config")

    parser.add_argument("-r", "--refresh", action = "store_true")
    parser.add_argument("--show", choices = ["lua_base", "lua_rock", "default", "versions"])
    parser.add_argument("--set_default")
    parser.add_argument("--set_base")
    parser.add_argument("--set_rock")

    args = parser.parse_args()

    config = Config()

    if args.refresh:
        config.refresh()
        print("Refreshed Lua versions.")

    if args.show:
        value = config.settings.get(args.show, None)
        if value:
            print(f"Value of {args.show}: {value}")
        else:
            print(f"{args.show} is not part of the config")

    if args.set_default:
        config.default = args.set_default
        print(f"Default set to {args.set_default}")

    if args.set_base:
        config.lua_base = Path(args.set_base)
        print(f"Base path set to {args.set_base}")

    if args.set_rock:
        config.lua_rock = args.set_rock
        print(f"LuaRocks version set to {args.set_rock}")

    config.save()


if __name__ == "__main__":
    main()