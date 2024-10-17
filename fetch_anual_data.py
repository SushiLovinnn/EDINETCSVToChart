from edinet_data_fetcher import EdinetDataFetcher
from main import main
import time
from datetime import datetime
import requests

def is_valid_date(year, month, day):
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        return False

year = 2024
day_from = (3, 26)
day_to = (4, 10) #半開区間で指定. 3/22から3/31まで取得する場合は(3, 32)とする.
fetch_flag = False

for month in range(3, 4):
    for day in range(22, 32):
        if (month, day) == day_from:
            fetch_flag = True
        if (month, day) == day_to:
            fetch_flag = False
        if not is_valid_date(year, month, day) or not fetch_flag:
            continue

        time.sleep(1)  # リクエストの間隔は1秒.
        print("--------------------")
        print(f"Fetching data for 2024-{month:02d}-{day:02d}")
        date = f"2024-{month:02d}-{day:02d}"
        fetcher = EdinetDataFetcher(date)
        
        retries = 3
        connected_flag = False
        try:
            fetcher.fetch_data()
            connected_flag = True
        except requests.exceptions.ConnectionError as e:
            for attempt in range(retries):
                try:
                    fetcher.fetch_data()
                    connected_flag = True
                    break
                except requests.exceptions.ConnectionError as e:
                    if attempt < retries - 1:
                        print(f"Retrying... ({attempt + 1}/{retries})")
                        time.sleep(2)  # リトライの前に待機
                        continue
        if connected_flag == False:
            print(f"Failed to fetch data for {date} after {retries} attempts")
            raise requests.exceptions.ConnectionError
                        

main()