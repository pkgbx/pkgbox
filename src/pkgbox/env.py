import os
import shutil
from typing import Dict, Optional


def getvar(name: str, defaults: Optional[str] = None) -> Optional[str]:
    """
    Return a environemnt variable value, if found.

    Return `None` in case an `defaults` value is not provided.
    """
    return os.environ.get(name, defaults)


def get_pkgbox_dirs() -> Dict[str, str]:
    """
    Detect the correct directory paths to use
    in a dictionary.

    The function works based on a set o priorities:

    - Use the value of `PKGBOX_HOME` env var if set;
    - Use the following XDG directories if set:
      - $XDG_DATA_HOME/pkgbox
      - $XDG_CONFIG_HOME/pkgbox
    - Use the following scheme if a $HOME env var is set:
      - $HOME/.local/share/pkgbox
      - $HOME/.config/pkgbox
    - Use `/opt/pkgbox` in case everything else fails
    """
    paths = {
        'config_dir': '',
        'data_dir': ''
    }

    if (e := getvar('PKGBOX_HOME')):
        paths['config_dir'] = f'{e}/config'
        paths['data_dir'] = f'{e}/data'
        return paths

    # XDG env vars
    if (e := getvar('XDG_CONFIG_HOME')):
        paths['config_dir'] = f'{e}/pkgbox'
    if (e := getvar('XDG_DATA_HOME')):
        paths['data_dir'] = f'{e}/pkgbox'

    # home env vars in case xdg fails
    if (e := getvar('HOME')):
        if not paths['config_dir']:
            paths['config_dir'] = f'{e}/.config/pkgbox'
        if not paths['data_dir']:
            paths['data_dir'] = f'{e}/.local/share/pkgbox'

    # defaults to /opt/pkgbox if nothing works
    if not paths['config_dir']:
        paths['config_dir'] = '/opt/pkgbox/config'
    if not paths['data_dir']:
        paths['data_dir'] = '/opt/pkgbox/data'

    return paths


def ensure_pkgbox_dirs(paths: Dict[str, str]) -> None:
    """
    Ensure all defined paths exists.
    """
    keys = ('config_dir', 'data_dir')
    for key in keys:
        try:
            os.makedirs(paths[key], exist_ok=True)
        except KeyError:
            raise errors.PBError('Missing "{keys}" from paths dict')
        except OSError as e:
            raise errors.PBError('OS error: {e.strerror}', e.errno)

def bootstrap(paths: Dict[str, str]) -> None:
    """
    Setup basic env files into pkgbox dirs.
    """

    # base crun config.json file
    assets_dir = f'{os.path.dirname(os.path.realpath(__file__))}/../assets'
    crun_config_path = f'{assets_dir}/crun/config.json'
    cfg_dir = paths['config_dir']

    try:
        os.makedirs(f'{cfg_dir}/crun', exist_ok=True)
    except OSError as e:
        raise errors.PBError('OS error: {e.strerror}', e.errno)
    
    shutil.copyfile(crun_config_path, f'{paths["config_dir"]}/crun/config.json')
