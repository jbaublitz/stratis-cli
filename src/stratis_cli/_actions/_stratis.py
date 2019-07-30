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
Miscellaneous actions about stratis.
"""

from .._stratisd_constants import RedundancyCodes

from ._connection import get_object
from ._constants import TOP_OBJECT
from ._data import Manager


class StratisActions():
    """
    Stratis actions.
    """

    @staticmethod
    def list_stratisd_redundancy(_namespace):
        """
        List the stratisd redundancy designations.
        """
        for code in RedundancyCodes:
            print("%s: %d" % (code.name, code.value))

    @staticmethod
    def list_stratisd_version(_namespace):
        """
        List the stratisd version.
        """
        print("%s" % Manager.Properties.Version.Get(get_object(TOP_OBJECT)))
