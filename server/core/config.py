# Copyright 2025 Sébastien Demanou. All Rights Reserved.
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
# ==============================================================================
import multiprocessing

from oremi_core.vars import getenv

HOST = getenv('HOST', default='127.0.0.1')
"""
Host address to listen on.
"""

PORT = getenv('PORT', default=4241, expected_type=int)
"""
Port number to listen on.
"""

ROOT_PATH = getenv('ROOT_PATH', default='/')
"""The root path for the API, which defines the base URL path for all routes."""

LOG_FILE = getenv('LOG_FILE', default='')
"""Path to the log file where application logs will be stored. If left empty, logs may be directed
to the console by default."""

LOG_LEVEL = getenv('LOG_LEVEL', default='INFO')
"""The log level used to control the verbosity of application logs. Options include 'DEBUG', 'INFO',
'WARNING', 'ERROR', and 'CRITICAL'."""

WORKERS = getenv('WORKERS', default=multiprocessing.cpu_count(), expected_type=int)
"""The number of worker processes to run for handling incoming API requests. By default, it uses
the number of CPU cores available on the system."""

TIMEZONE = getenv('TIMEZONE', default='UTC')
"""
Timezone used for datetime operations, e.g., 'Africa/Cairo' or 'UTC'.
"""
