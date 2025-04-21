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

from .models import COPTIC_MONTHS
from .models import EGYPTIAN_SEASONS
from .models import EGYPTIAN_ZODIAC
from .models import EgyptianCalendarDetails
from .models import SOLAR_EVENTS


def get_egyptian_zodiac(day_of_year: int) -> str:
  """Determine the Egyptian zodiac sign based on the day of the year."""
  for sign in EGYPTIAN_ZODIAC:
    if sign['start'] <= day_of_year <= sign['end']:
      return sign['name']
  return 'Unknown'


def get_coptic_date(date: datetime, year: int) -> str:
  """Convert Gregorian date to Coptic date."""
  coptic_month = COPTIC_MONTHS[(date.month - 1) % 12]
  coptic_day = date.day
  return f'{coptic_month} {coptic_day}, {year}'


def get_solar_event(date: datetime) -> str | None:
  """Find the nearest solar event to the given date."""
  min_distance = float('inf')
  closest_event = None

  for event in SOLAR_EVENTS:
    distance = abs((date.month - event['month']) * 30 + (date.day - event['day']))
    if distance < min_distance:
      min_distance = distance
      closest_event = event['name']

  # Only return an event if it's within 7 days
  return closest_event if min_distance <= 7 else None


def egyptian_calendar_info(date: datetime) -> EgyptianCalendarDetails:
  if date.tzinfo is not None:
    jan1 = datetime(date.year, 1, 1, tzinfo=date.tzinfo)
  else:
    jan1 = datetime(date.year, 1, 1)

  day_of_year = (date - jan1).days + 1

  # Adjust for leap year if after February
  if (date.year % 4 == 0 and (date.year % 100 != 0 or date.year % 400 == 0)) and day_of_year > 59:
    day_of_year -= 1

  day_of_year = min(day_of_year, 365)
  egyptian_year = date.year + 4241
  year_progress = (day_of_year / 365) * 100

  current_egyptian_month = COPTIC_MONTHS[min(day_of_year // 30, 12)]
  current_egyptian_day = (day_of_year - 1) % 30 + 1
  is_epagomenal_day = day_of_year > 360
  season = EGYPTIAN_SEASONS[min(day_of_year // 120, 2)]

  # Calculate next Egyptian New Year (September 11)
  if date.month > 9 or (date.month == 9 and date.day >= 11):
    next_egyptian_new_year_date = datetime(date.year + 1, 9, 11)
  else:
    next_egyptian_new_year_date = datetime(date.year, 9, 11)

  if date.tzinfo is not None:
    next_egyptian_new_year_date = next_egyptian_new_year_date.replace(tzinfo=date.tzinfo)

  days_until_new_year = (next_egyptian_new_year_date - date).days

  # Get dynamic values
  egyptian_zodiac = get_egyptian_zodiac(day_of_year)
  coptic_date = get_coptic_date(date, egyptian_year)
  solar_event = get_solar_event(date)
  weekday = date.strftime('%A')

  return EgyptianCalendarDetails(
    current_egyptian_year=egyptian_year,
    day_of_year=day_of_year,
    total_days_in_year=365,
    year_progress=round(year_progress, 2),
    gregorian_date=date.date().isoformat(),
    current_egyptian_month=current_egyptian_month,
    current_egyptian_day=current_egyptian_day,
    is_epagomenal_day=is_epagomenal_day,
    season=season,
    next_egyptian_new_year=next_egyptian_new_year_date.date().isoformat(),
    days_until_new_year=days_until_new_year,
    egyptian_zodiac=egyptian_zodiac,
    coptic_date=coptic_date,
    # historical_events=[],
    weekday=weekday,
    solar_event=solar_event,
  )
