from ._connection import get_object
from ._constants import TOP_OBJECT
from ._data import MAXIMUM_STRATISD_VERSION, MINIMUM_STRATISD_VERSION, Manager
from .._errors import StratisCliStratisdVersionError


def check_stratisd_version():
    """
    Check that the version of stratisd is compatible with the required versions.
    FIX ME
    """
    version = Manager.Properties.Version.Get(get_object(TOP_OBJECT))
    version = tuple([int(x) for x in version.split(".")])
    if version < MINIMUM_STRATISD_VERSION or version > MAXIMUM_STRATISD_VERSION:
        raise StratisCliStratisdVersionError(
            version, MINIMUM_STRATISD_VERSION, MAXIMUM_STRATISD_VERSION
        )
