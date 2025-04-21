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
import asyncio
import json
import logging
import os

import uvicorn.config

from server.core.api import BASE_PATH
from server.core.config import HOST
from server.core.config import LOG_FILE
from server.core.config import PORT
from server.core.config import ROOT_PATH
from server.core.config import WORKERS
from server.core.logger import LOG_LEVEL_STR
from server.core.logger import logger
from server.core.package import APP_NAME
from server.core.package import APP_VERSION


def get_log_config():
  current_dir = os.path.dirname(os.path.abspath(__file__))
  config_filename = os.path.join(current_dir, 'log-config.json')

  with open(config_filename, encoding='utf-8') as file:
    return json.load(file)


async def main():
  verbose = logger.isEnabledFor(logging.DEBUG)
  log_config = get_log_config() if not verbose else uvicorn.config.LOGGING_CONFIG

  logger.info(f'Starting {APP_NAME}/{APP_VERSION}')
  logger.info(f'Server Host: {HOST}')
  logger.info(f'Server Port: {PORT}')
  logger.info(f'Server Workers: {WORKERS}')
  logger.info(f'Server Root Path: {ROOT_PATH}')
  logger.info(f'API Root Path: {ROOT_PATH}')
  logger.info(f'API Base Path: {BASE_PATH}')
  logger.info(f'Log Level: {LOG_LEVEL_STR}')
  logger.info(f'Log File Path: {LOG_FILE or None}')

  uvicorn.run(
    app='server:api',
    host=HOST,
    port=PORT,
    workers=WORKERS,
    server_header=False,
    use_colors=True,
    proxy_headers=True,
    log_level='info',
    log_config=log_config,
  )


if __name__ == '__main__':
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    pass
