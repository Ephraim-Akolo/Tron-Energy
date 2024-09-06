import importlib

def get_version():
    try:
        version_module = importlib.import_module('.version', package='tron_energy')
        return version_module.version
    except ImportError:
        return "0.0.0"

__version__ = get_version()


from .tron_energy import TronEnergy
from .async_tron_energy import AsyncTronEnergy

    
__all__ = ['TronEnergy', 'AsyncTronEnergy']