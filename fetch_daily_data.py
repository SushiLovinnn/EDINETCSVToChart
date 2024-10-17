#! pass to your python interpreter

from edinet_data_fetcher import EdinetDataFetcher
from main import main

fetcher = EdinetDataFetcher("2021-01-01", fetch_today=True)
fetcher.fetch_data()
# main()