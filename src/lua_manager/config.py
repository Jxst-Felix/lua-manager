from pathlib import Path
import subprocess
import typing
import copy
import yaml
import re

BASE_DIR = Path(__file__).parent # set basedir here so I can import config.yml
DEFAULT_CONFIG = { # in case config.yml is not found in the same dir as this py file
    'lua_base': str(BASE_DIR), # lua_base as to where all the Lua versions take root
    'default': '5.5.0', # default version
    'lua_rock': '5.5.0', # version that lua rock handles
    'versions': { # a list of lua versions found (version and its base_dir)
        '5.5.0': '', 
        '5.4.8': '',
    }
}

class Config:
    def __init__(self):
        self._config_file: Path = BASE_DIR / 'config.yml'
        config_dict = self.load()

        self.lua_base: Path = Path(config_dict.get('lua_base', DEFAULT_CONFIG['lua_base']))
        self.lua_rock: str = config_dict.get('lua_rock', DEFAULT_CONFIG['lua_rock'])
        self.default: str = config_dict.get('default', DEFAULT_CONFIG['default'])
        self.versions: typing.Dict[str, typing.Any] = config_dict.get('versions', DEFAULT_CONFIG['versions'])

    @property
    def default_path(self) -> typing.Optional[Path]:
        path_str = self.versions.get(self.default, '')
        if not path_str:
            return None
        
        path = Path(path_str)
        if not (path.exists() and path.is_dir()):
            return None
        return path

    @property
    def settings(self) -> typing.Dict[str, typing.Any]:
        return {
            'lua_base': str(self.lua_base), 'lua_rock': self.lua_rock, 
            'default': self.default, 'versions': self.versions,
        }

    @property
    def _config_exists(self) -> bool:
        return self._config_file.exists() and self._config_file.is_file()
    
    @property
    def versions_available(self) -> typing.List[str]:
        return [
            key for key, value in self.versions.items() 
            if Path(value).exists() and Path(value).is_dir()
        ]

    def load(self) -> typing.Dict[str, typing.Any]:
        default = copy.deepcopy(DEFAULT_CONFIG)
        if not self._config_exists:
            return default

        with open(self._config_file, 'r') as f:
            return yaml.safe_load(f) or default
        
    def save(self):
        if not self._config_exists:
            self._config_file.parent.mkdir(parents = True, exist_ok = True)

        with open(self._config_file, 'w') as f:
            yaml.safe_dump(self.settings, f)

    def _get_version(self, path: Path) -> str:
        if not (path.exists() and path.is_file()):
            return ''
        
        try:
            result = subprocess.check_output([str(path), '-v'], text = True)
            tokens = result.split()
            return tokens[1]
        
        except Exception as e:
            print(e)
            return ''

    def _get_recurse(self, path: Path):
        for file in path.iterdir():
            if file.is_file() and re.match(r'lua\d+\.exe$', file.name, re.IGNORECASE):
                version = self._get_version(file)
                if version:
                    self.versions[version] = str(file.parent)

            elif file.is_dir() and not file.is_symlink():
                self._get_recurse(file)

    def refresh(self):
        path = self.lua_base
        self.versions = {}
        if not (path.exists() and path.is_dir()):
            self.lua_base = DEFAULT_CONFIG['lua_base']
            self.versions = DEFAULT_CONFIG['versions']
        self._get_recurse(path)
        self.save()