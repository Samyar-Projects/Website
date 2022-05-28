#  Gigawhat Website Google Analytics Data API util.
#  Copyright 2022 Gigawhat Programming Team
#  Written by Samyar Sadat Akhavi, 2020 - 2022.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Google Analytics util.

Gets analytics information from the Google Analytics Data API.
"""


# ------- Libraries and utils -------
from config import AppConfig
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest, RunReportResponse


# ---- Global variables ----
PROPERTY_ID = AppConfig.ANALYTICS_PROPERTY_ID


# -=-=-= Functions =-=-=-

# ---- Get basic analytics data from the API ----
def get_basic_data(start_date: str, end_date: str, metric: str):
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property = f"properties/{PROPERTY_ID}",
        metrics = [Metric(name=metric)],
        date_ranges = [DateRange(start_date=start_date, end_date=end_date)],
    )
    
    return client.run_report(request)


# ---- Parse usable data from raw basic API response ----
def parse_basic_response(response: RunReportResponse):
    if response.rows:
        return response.rows[0].metric_values[0].value
    
    return "0"


class Analytics():
    # ---- Total page views ----
    def total_pageviews():
        response = get_basic_data("2022-05-01", "today", "screenPageviews")
        value = parse_basic_response(response)
        
        return str(value)


    # ---- Total page views (Past 30 days) ----
    def pageviews_this_month():
        response = get_basic_data("30daysAgo", "today", "screenPageviews")
        value = parse_basic_response(response)
        
        return str(value)
    

    # ---- Total page views (Today) ----
    def pageviews_today():
        response = get_basic_data("today", "today", "screenPageviews")
        value = parse_basic_response(response)
        
        return str(value)


    # ---- Total unique user count ----
    def total_users():
        response = get_basic_data("2022-05-01", "today", "totalUsers")
        value = parse_basic_response(response)
        
        return str(value)


    # ---- Number of new users (Today) ----
    def new_users_today():
        response = get_basic_data("today", "today", "newUsers")
        value = parse_basic_response(response)
        
        return str(value)


    # ---- Number of active users (Today) ----
    def active_users_today():
        response = get_basic_data("today", "today", "activeUsers")
        value = parse_basic_response(response)
        
        return str(value)
    
    
    # ---- Custom basic API query ----
    def custom_basic_query(start_date: str, end_date: str, metric: str):
        response = get_basic_data(start_date, end_date, metric)
        value = parse_basic_response(response)
        return value
    
    
    # ---- Fully custom API query ----
    def custom_query(request: RunReportRequest):
        client = BetaAnalyticsDataClient()
        return client.run_report(request)