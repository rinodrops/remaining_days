#!/usr/bin/env python3

# =============================================================================
# Notify remaining days until the new years day
#
# Download and place the Japanese national holidays CSV file
# https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
# =============================================================================

from mastodon import Mastodon
from datetime import date, datetime
import os
import dotenv
import pandas as pd

# Load environment variables
# -----------------------------------------------------------------------------
dotenv.load_dotenv()

# Calculate remaining days and percentage until New Year's Day
# -----------------------------------------------------------------------------
today = date.today()
new_year = date(today.year + 1, 1, 1)
remaining_days_new_year = (new_year - today).days
total_days = (new_year - date(today.year, 1, 1)).days
remaining_percentage =  remaining_days_new_year / total_days * 100

# Load and process the Japanese national holidays CSV file
# -----------------------------------------------------------------------------
holidays_df = pd.read_csv('syukujitsu.csv', encoding='shift_jis')
holidays_df.iloc[:, 0] = pd.to_datetime(holidays_df.iloc[:, 0], format='%Y/%m/%d')
upcoming_holidays = holidays_df[holidays_df.iloc[:, 0] >= pd.Timestamp(today)].head(5)

# Prepare a message for the upcoming holidays
holiday_messages = []
for idx, holiday in upcoming_holidays.iterrows():
    remaining_days = (holiday.iloc[0] - pd.Timestamp(today)).days
    holiday_message = f"{holiday.iloc[0].strftime('%Y年%m月%d日')}: {holiday.iloc[1]} (残り{remaining_days}日)"
    holiday_messages.append(holiday_message)

upcoming_holiday_message = '\n'.join(holiday_messages)

# Format the message
# -----------------------------------------------------------------------------
message = f"{today.year}年{today.month}月{today.day}日になりました。\n今年は残り{remaining_days_new_year}日です。あと{remaining_percentage:.1f}%です。\n\n次の祝日:\n{upcoming_holiday_message}"

# Mastodon API credentials
mastodon = Mastodon(
    access_token = os.getenv("MASTODON_ACCESS_TOKEN"),
    api_base_url = os.getenv("MASTODON_API_BASE_URL")
)

# Post the message
mastodon.status_post(message)