#!/usr/bin/env python3

from edinet_data_fetcher import EdinetDataFetcher

fetcher = EdinetDataFetcher("2021-01-01", fetch_today=True)
fetcher.fetch_data()
# main()