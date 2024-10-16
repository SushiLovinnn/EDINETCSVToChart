from edinet_data_fetcher import EdinetDataFetcher

for month in range(1, 13):
    for day in range(1, 32):
        print(f"Fetching data for 2024-{month:02d}-{day:02d}")
        date = f"2024-{month:02d}-{day:02d}"
        fetcher = EdinetDataFetcher(date)
        fetcher.fetch_data()