from edinet_data_fetcher import EdinetDataFetcher
from main import main
import time
from datetime import datetime

def is_valid_date(year, month, day):
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        return False

year = 2024

for month in range(3, 13):
    for day in range(1, 32):
        if not is_valid_date(year, month, day):
            continue
        time.sleep(0.5)
        print(f"Fetching data for 2024-{month:02d}-{day:02d}")
        date = f"2024-{month:02d}-{day:02d}"
        fetcher = EdinetDataFetcher(date)
        fetcher.fetch_data()

main()