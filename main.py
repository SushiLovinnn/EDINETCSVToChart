import pandas as pd
import json


# CSVファイルを読み込む
print("CSV file path:")
file_path = input()

try:
    df = pd.read_csv(file_path, encoding='utf-16le', delimiter='\t')
except Exception as e:
    print(f"読み込みエラー: {e}")
    exit()

# ID_expression_dict の定義
ID_expression_dict = {
    ('jpcrp_cor:CompanyNameCoverPage', 'FilingDateInstant'): ['会社名', -1, '単位'],
    ('jpcrp030000-asr_E02144-000:OperatingRevenuesIFRSKeyFinancialData', 'CurrentYearDuration'): ['売上高(IFRS)', -1, '単位'],
    ('jpigp_cor:OperatingProfitLossIFRS', 'CurrentYearDuration'): ['営業利益(IFRS)', -1, '単位'],
    ('jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults', 'CurrentYearDuration'): ['当期純利益(IFRS)', -1, '単位'],
    ('jpigp_cor:AssetsIFRS', 'CurrentYearInstant'): ['資産(IFRS)', -1, '単位'],
    ('jpigp_cor:LiabilitiesIFRS', 'CurrentYearInstant'): ['負債(IFRS)', -1, '単位'],
    ('jpigp_cor:CurrentAssetsIFRS', 'CurrentYearInstant'): ['流動資産(IFRS)', -1, '単位'],
    ('jpigp_cor:NonCurrentAssetsIFRS', 'CurrentYearInstant'): ['固定資産(IFRS)', -1, '単位'],
    ('jpdei_cor:CurrentPeriodEndDateDEI', 'FilingDateInstant'): ['当会計期間終了日', -1, '単位'],
    ('jpigp_cor:EquityIFRS', 'CurrentYearInstant'): ['資本(IFRS)', -1, '単位'],
    ('jpigp_cor:TotalCurrentLiabilitiesIFRS', 'CurrentYearInstant'): ['流動負債(IFRS)', -1, '単位'],
    ('jpigp_cor:NonCurrentLabilitiesIFRS', 'CurrentYearInstant'): ['固定負債(IFRS)', -1, '単位'],
    ('jpigp_cor:InterestBearingLiabilitiesCLIFRS', 'CurrentYearInstant'): ['有利子流動負債(IFRS)', -1, '単位'],
    ('jpigp_cor:InterestBearingLiabilitiesNCLIFRS', 'CurrentYearInstant'): ['有利子固定負債(IFRS)', -1, '単位']
}

# 行データを処理する関数を定義
def update_id_expression_dict(row):
    key = (row['要素ID'], row['コンテキストID'])
    if key in ID_expression_dict:
        try:
            ID_expression_dict[key][1] = int(row['値'])
        except ValueError:
            ID_expression_dict[key][1] = row['値']
        ID_expression_dict[key][2] = row['単位']

# `apply`で全行を処理
df.apply(update_id_expression_dict, axis=1)

# 値を表示
for content_name, value, unit in ID_expression_dict.values():
    if isinstance(value, int):
        formatted_value = f'{value:,}'
    else:
        formatted_value = value
    print(f'{content_name}: {formatted_value}{unit}' if isinstance(value, int) else f'{content_name}: {formatted_value}')

# データを作成してJSONに保存
data = {
    'CompanyName': ID_expression_dict[('jpcrp_cor:CompanyNameCoverPage', 'FilingDateInstant')],
    'Sales': ID_expression_dict[('jpcrp030000-asr_E02144-000:OperatingRevenuesIFRSKeyFinancialData', 'CurrentYearDuration')],
    'OperatingProfits': ID_expression_dict[('jpigp_cor:OperatingProfitLossIFRS', 'CurrentYearDuration')],
    'NetIncome': ID_expression_dict[('jpcrp_cor:ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults', 'CurrentYearDuration')],
    'Assets': ID_expression_dict[('jpigp_cor:AssetsIFRS', 'CurrentYearInstant')],
    'Liabilities': ID_expression_dict[('jpigp_cor:LiabilitiesIFRS', 'CurrentYearInstant')],
    'CurrentAssets': ID_expression_dict[('jpigp_cor:CurrentAssetsIFRS', 'CurrentYearInstant')],
    'NonCurrentAssets': ID_expression_dict[('jpigp_cor:NonCurrentAssetsIFRS', 'CurrentYearInstant')],
    'EndDate': ID_expression_dict[('jpdei_cor:CurrentPeriodEndDateDEI', 'FilingDateInstant')],
    'NetAssets': ID_expression_dict[('jpigp_cor:EquityIFRS', 'CurrentYearInstant')],
    'CurrentLiabilities': ID_expression_dict[('jpigp_cor:TotalCurrentLiabilitiesIFRS', 'CurrentYearInstant')],
    'NonCurrentLiabilities': ID_expression_dict[('jpigp_cor:NonCurrentLabilitiesIFRS', 'CurrentYearInstant')],
    'Interest-bearingCurrentLiabilities': ID_expression_dict[('jpigp_cor:InterestBearingLiabilitiesCLIFRS', 'CurrentYearInstant')],
    'Interest-bearingNonCurrentLiabilities': ID_expression_dict[('jpigp_cor:InterestBearingLiabilitiesNCLIFRS', 'CurrentYearInstant')]

}

json_file_path = f'json_file/{data["CompanyName"][1]}{data["EndDate"][1]}.json'
try:
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"JSONファイルを保存しました: {json_file_path}")
except Exception as e:
    print(f"JSONファイル保存エラー: {e}")
    exit()

from plot import Plot


chart = Plot(json_file_path)
chart.plot()