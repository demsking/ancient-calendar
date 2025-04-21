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
import os

from fastapi import FastAPI

from .core.api import BASE_PATH
from .core.package import APP_VERSION
from .endpoints.calendar import create_calendar_endpoints
from .endpoints.docs import create_docs_endpoints
from .endpoints.version import create_version_endpoints


SERVICE_TITLE = 'Ancient Calendar Documentation'

_current_dir = os.path.dirname(os.path.abspath(__file__))
_readme_path = os.path.realpath(
  os.path.join(_current_dir, '..', 'DOCUMENTATION.md'),
)

with open(_readme_path, encoding='utf-8') as file:
  SERVICE_DESCRIPTION = file.read()

calendar_tag = {
  'name': 'Calendar Endpoints',
  'description': (
    'Endpoints for exploring the ancient Egyptian civil calendar, including '
    'details about the current year, day, zodiac, and seasonal progress.'
  ),
}

version_tag = {
  'name': 'Server Endpoints',
  'description': (
    "Endpoints for retrieving server-related metadata, such as the server's "
    'name and version. These endpoints help clients identify the server they '
    'are interacting with and ensure compatibility with the API.'
  ),
}


api = FastAPI(
  docs_url=None,
  redoc_url=None,
  title=SERVICE_TITLE,
  version=APP_VERSION,
  description=SERVICE_DESCRIPTION,
  root_path=BASE_PATH,
  servers=[
    {'url': BASE_PATH},
  ],
  license_info={
    'name': 'Apache 2.0',
    'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
  },
  openapi_tags=[
    calendar_tag,
    version_tag,
  ],
)

create_calendar_endpoints(tag=calendar_tag['name'], api=api)
create_version_endpoints(version_tag['name'], api)
create_docs_endpoints(api)
