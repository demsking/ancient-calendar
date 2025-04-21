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
from datetime import datetime

import pytz
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query

from ..core.calendar import egyptian_calendar_info
from ..core.calendar import EgyptianCalendarDetails
from ..core.config import TIMEZONE


def create_calendar_endpoints(tag: str, api: FastAPI) -> None:
  @api.get('/current', tags=[tag])
  async def get_current_egyptian_date(
    timezone: str = Query(
      default=None,
      description='The timezone to use for calculating the Ancient Calendar details. Examples include UTC, Africa/Douala, Europe/Paris.',
      examples=['UTC', 'Africa/Douala', 'Europe/Paris'],
    ),
  ) -> EgyptianCalendarDetails:
    """
    Retrieve the Ancient Calendar details for the current date.

    This endpoint provides a snapshot of the Ancient Calendar based on the
    current date and time. It includes information such as the current day,
    month, and year in the Ancient Calendar, as well as the corresponding
    Gregorian date. Users can also learn about the current season, zodiac sign,
    and other calendar-related details.

    By specifying a timezone, users can ensure the calculations reflect their
    desired context.
    """
    tz = pytz.timezone(timezone or TIMEZONE)
    date_obj = datetime.now(tz)

    return egyptian_calendar_info(date_obj)

  @api.get(
    '/date',
    tags=[tag],
    responses={
      200: {
        'content': {
          'application/json': {},
        },
      },
      400: {
        'content': {
          'application/json': {},
        },
      },
    },
  )
  async def get_egyptian_date(
    date: str = Query(
      description='The specific Gregorian date (in YYYY-MM-DD format) to calculate the Ancient Calendar details for.',
      examples=['2025-04-21', '2025-09-11'],
    ),
  ) -> EgyptianCalendarDetails:
    """
    Retrieve the Ancient Calendar details for a specific Gregorian date.

    This endpoint provides a snapshot of the Ancient Calendar based on a
    user-specified Gregorian date. It includes information such as the day,
    month, and year in the Ancient Calendar, as well as the corresponding
    Gregorian date. Users can also learn about the season, zodiac sign, and
    other calendar-related details.

    The date must be provided in the format YYYY-MM-DD.
    """
    try:
      date_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError as error:
      raise HTTPException(status_code=400, detail='Invalid date format. Please use YYYY-MM-DD.') from error

    return egyptian_calendar_info(date_obj)
