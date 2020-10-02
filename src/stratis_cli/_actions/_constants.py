# Copyright 2016 Red Hat, Inc.
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
General constants.
"""
# isort: THIRDPARTY
from semantic_version import Version

SERVICE = "org.storage.stratis2"
TOP_OBJECT = "/org/storage/stratis2"

SECTOR_SIZE = 512

FETCH_PROPERTIES_INTERFACE = "org.storage.stratis2.FetchProperties.r2"
FILESYSTEM_INTERFACE = "org.storage.stratis2.filesystem"
POOL_INTERFACE = "org.storage.stratis2.pool.r3"
BLOCKDEV_INTERFACE = "org.storage.stratis2.blockdev.r2"
REPORT_INTERFACE = "org.storage.stratis2.Report.r1"

MAXIMUM_STRATISD_VERSION = "3.0.0"
MINIMUM_STRATISD_VERSION = "2.2.0"
assert Version(MINIMUM_STRATISD_VERSION) < Version(MAXIMUM_STRATISD_VERSION)
