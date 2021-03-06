# Copyright 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
XML interface specifications.
"""
from os import environ

import sys

import xml.etree.ElementTree as ET

from dbus_client_gen import managed_object_class
from dbus_client_gen import mo_query_builder
from dbus_client_gen import DbusClientGenerationError

from dbus_python_client_gen import make_class
from dbus_python_client_gen import DPClientGenerationError

from .._errors import StratisCliEnvironmentError
from .._errors import StratisCliGenerationError

from ._constants import BLOCKDEV_INTERFACE
from ._constants import FILESYSTEM_INTERFACE
from ._constants import POOL_INTERFACE


assert hasattr(sys.modules.get("stratis_cli"), "run"), (
    "This module is being loaded too eagerly. Make sure that loading it is "
    "deferred until after the stratis_cli module has been fully loaded."
)


SPECS = {
    "org.freedesktop.DBus.ObjectManager": """
<interface name="org.freedesktop.DBus.ObjectManager">
<method name="GetManagedObjects">
<arg name="objpath_interfaces_and_properties" type="a{oa{sa{sv}}}" direction="out"/>
</method>
</interface>
""",
    "org.storage.stratis1.Manager": """
<interface name="org.storage.stratis1.Manager">
<method name="ConfigureSimulator">
<arg name="denominator" type="u" direction="in"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<method name="CreatePool">
<arg name="name" type="s" direction="in"/>
<arg name="redundancy" type="(bq)" direction="in"/>
<arg name="devices" type="as" direction="in"/>
<arg name="result" type="(b(oao))" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<method name="DestroyPool">
<arg name="pool" type="o" direction="in"/>
<arg name="result" type="(bs)" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<property name="Version" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
</interface>
""",
    "org.storage.stratis1.pool": """
<interface name="org.storage.stratis1.pool">
<method name="AddCacheDevs">
<arg name="devices" type="as" direction="in"/>
<arg name="results" type="(bao)" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<method name="AddDataDevs">
<arg name="devices" type="as" direction="in"/>
<arg name="results" type="(bao)" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<method name="CreateFilesystems">
<arg name="specs" type="as" direction="in"/>
<arg name="results" type="(ba(os))" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<method name="DestroyFilesystems">
<arg name="filesystems" type="ao" direction="in"/>
<arg name="results" type="(bas)" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<method name="SetName">
<arg name="name" type="s" direction="in"/>
<arg name="result" type="(bs)" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<method name="SnapshotFilesystem">
<arg name="origin" type="o" direction="in"/>
<arg name="snapshot_name" type="s" direction="in"/>
<arg name="result" type="(bo)" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<property name="Name" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
</property>
<property name="TotalPhysicalSize" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
</property>
<property name="TotalPhysicalUsed" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
</property>
<property name="Uuid" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
<property name="State" type="q" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
</property>
<property name="ExtendState" type="q" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
</property>
<property name="SpaceState" type="q" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
</property>
</interface>
""",
    "org.storage.stratis1.filesystem": """
<interface name="org.storage.stratis1.filesystem">
<method name="SetName">
<arg name="name" type="s" direction="in"/>
<arg name="action" type="(bs)" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<property name="Created" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
<property name="Devnode" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
<property name="Name" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
</property>
<property name="Pool" type="o" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
<property name="Used" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
</property>
<property name="Uuid" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
</interface>
""",
    "org.storage.stratis1.blockdev": """
<interface name="org.storage.stratis1.blockdev">
<method name="SetUserInfo">
<arg name="id" type="s" direction="in"/>
<arg name="result" type="(bs)" direction="out"/>
<arg name="return_code" type="q" direction="out"/>
<arg name="return_string" type="s" direction="out"/>
</method>
<property name="Devnode" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
<property name="HardwareInfo" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
<property name="InitializationTime" type="t" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
<property name="Pool" type="o" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
<property name="State" type="q" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="true"/>
</property>
<property name="Tier" type="q" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
</property>
<property name="TotalPhysicalSize" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
</property>
<property name="UserInfo" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="false"/>
</property>
<property name="Uuid" type="s" access="read">
<annotation name="org.freedesktop.DBus.Property.EmitsChangedSignal" value="const"/>
</property>
</interface>
""",
}

_MANAGER_INTERFACE = "org.storage.stratis1.Manager"

DBUS_TIMEOUT_SECONDS = 120
MAXIMUM_DBUS_TIMEOUT_MS = 1073741823


def _get_timeout(value):
    """
    Turn an input str or int into a float timeout value.

    :param value: the input str or int
    :type value: str or int
    :raises StratisCliEnvironmentError:
    :returns: float
    """
    # Ensure the input str is not a float
    if isinstance(value, float):
        raise StratisCliEnvironmentError(
            "The timeout value provided is a float; it should be an integer."
        )

    try:
        timeout_int = int(value)

    except ValueError:
        raise StratisCliEnvironmentError(
            "The timeout value provided is not an integer."
        )

    # Ensure the integer is not too small
    if timeout_int < -1:
        raise StratisCliEnvironmentError(
            "The timeout value provided is smaller than the smallest acceptable value, -1."
        )

    # Ensure the integer is not too large
    if timeout_int > MAXIMUM_DBUS_TIMEOUT_MS:
        raise StratisCliEnvironmentError(
            "The timeout value provided exceeds the largest acceptable value, %s."
            % MAXIMUM_DBUS_TIMEOUT_MS
        )

    # Convert from milliseconds to seconds
    return timeout_int / 1000


try:

    timeout = _get_timeout(
        environ.get("STRATIS_DBUS_TIMEOUT", DBUS_TIMEOUT_SECONDS * 1000)
    )

    filesystem_spec = ET.fromstring(SPECS[FILESYSTEM_INTERFACE])
    Filesystem = make_class("Filesystem", filesystem_spec, timeout)
    MOFilesystem = managed_object_class("MOFilesystem", filesystem_spec)
    filesystems = mo_query_builder(filesystem_spec)

    pool_spec = ET.fromstring(SPECS[POOL_INTERFACE])
    Pool = make_class("Pool", pool_spec, timeout)
    MOPool = managed_object_class("MOPool", pool_spec)
    pools = mo_query_builder(pool_spec)

    blockdev_spec = ET.fromstring(SPECS[BLOCKDEV_INTERFACE])
    MODev = managed_object_class("MODev", blockdev_spec)
    devs = mo_query_builder(blockdev_spec)

    Manager = make_class("Manager", ET.fromstring(SPECS[_MANAGER_INTERFACE]), timeout)

    ObjectManager = make_class(
        "ObjectManager",
        ET.fromstring(SPECS["org.freedesktop.DBus.ObjectManager"]),
        timeout,
    )

# Do not expect to get coverage on Generation errors.
# These can only occurs if the XML data in _SPECS is ill-formed; we have
# complete control over that data and can expect it to be valid.
except DPClientGenerationError as err:  # pragma: no cover
    raise StratisCliGenerationError(
        "Failed to generate some class needed for invoking dbus-python methods"
    ) from err
except DbusClientGenerationError as err:  # pragma: no cover
    raise StratisCliGenerationError(
        "Failed to generate some class needed for examining D-Bus data"
    ) from err
