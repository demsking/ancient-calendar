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
from typing import Literal

from pydantic import BaseModel
from pydantic import Field

CalendarSeason = Literal['Akhet', 'Peret', 'Shemu']
EGYPTIAN_SEASONS: list[CalendarSeason] = ['Akhet', 'Peret', 'Shemu']

CalendarMonth = Literal[
  'Thoth',
  'Phaophi',
  'Hathor',
  'Koiak',
  'Tybi',
  'Mechir',
  'Phamenoth',
  'Pharmuthi',
  'Pachons',
  'Payni',
  'Epip',
  'Mesori',
  'Epagomenal',
]

COPTIC_MONTHS: list[CalendarMonth] = [
  'Thoth',
  'Phaophi',
  'Hathor',
  'Koiak',
  'Tybi',
  'Mechir',
  'Phamenoth',
  'Pharmuthi',
  'Pachons',
  'Payni',
  'Epip',
  'Mesori',
  'Epagomenal',
]

# Egyptian zodiac signs with their date ranges (day of year)
EGYPTIAN_ZODIAC = [
  {'name': 'Nile', 'start': 1, 'end': 30},
  {'name': 'Amun-Ra', 'start': 31, 'end': 60},
  {'name': 'Mut', 'start': 61, 'end': 90},
  {'name': 'Geb', 'start': 91, 'end': 120},
  {'name': 'Osiris', 'start': 121, 'end': 150},
  {'name': 'Isis', 'start': 151, 'end': 180},
  {'name': 'Thoth', 'start': 181, 'end': 210},
  {'name': 'Horus', 'start': 211, 'end': 240},
  {'name': 'Anubis', 'start': 241, 'end': 270},
  {'name': 'Seth', 'start': 271, 'end': 300},
  {'name': 'Bastet', 'start': 301, 'end': 330},
  {'name': 'Sekhmet', 'start': 331, 'end': 365},
]

# Solar events with their approximate dates (month, day)
SOLAR_EVENTS = [
  {'name': 'Spring Equinox', 'month': 3, 'day': 20},
  {'name': 'Summer Solstice', 'month': 6, 'day': 21},
  {'name': 'Autumn Equinox', 'month': 9, 'day': 22},
  {'name': 'Winter Solstice', 'month': 12, 'day': 21},
]


class EgyptianCalendarDetails(BaseModel):
  """Details of the Egyptian civil calendar for a given Gregorian date."""

  current_egyptian_day: int = Field(
    ..., description='The current day of the Egyptian month (1-30).', examples=[15], ge=1, le=30
  )
  current_egyptian_month: CalendarMonth = Field(
    ..., description='The current month in the Egyptian civil calendar.', examples=[COPTIC_MONTHS[3]]
  )
  current_egyptian_year: int = Field(
    ..., description='The year in the Egyptian civil calendar (starting from 4241 BCE).', examples=[6266]
  )
  day_of_year: int = Field(..., description='The current day of the Egyptian year (1-365).', examples=[112], ge=1, le=365)
  total_days_in_year: int = Field(
    default=365, description='Total days in the Egyptian year (always 365, no leap years).', examples=[365]
  )
  year_progress: float = Field(..., description='Percentage of the year elapsed (0-100).', examples=[30.68], ge=0, le=100)

  is_epagomenal_day: bool = Field(
    ..., description='Indicates whether the current day is one of the 5 epagomenal days.', examples=[False]
  )
  season: CalendarSeason = Field(
    ...,
    description='The current Egyptian season: Akhet (Inundation), Peret (Emergence), or Shemu (Harvest).',
    examples=[EGYPTIAN_SEASONS[0]],
  )
  next_egyptian_new_year: str = Field(
    ..., description='The date of the next Egyptian New Year in ISO format.', examples=['2025-09-11']
  )
  days_until_new_year: int = Field(
    ..., description='Number of days remaining until the next Egyptian New Year.', examples=[142], ge=0, le=365
  )
  egyptian_zodiac: str = Field(
    ..., description='The Egyptian zodiac sign associated with the current date.', examples=['Amun-Ra']
  )
  coptic_date: str = Field(..., description='The corresponding date in the Coptic calendar.', examples=['Parmouti 14, 6266'])
  # historical_events: list[str] = Field(
  #   default_factory=list, description='List of historical or cultural events associated with the date.'
  # )
  weekday: str = Field(..., description='The weekday name of the corresponding Gregorian date.', examples=['Tuesday'])
  solar_event: str | None = Field(
    None, description='The solar event closest to the current date (e.g., Equinox, Solstice).', examples=['Spring Equinox']
  )
  gregorian_date: str = Field(
    ..., description='The corresponding Gregorian date in ISO format (YYYY-MM-DD).', examples=['2025-04-22']
  )
