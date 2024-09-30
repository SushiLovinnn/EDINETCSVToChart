import json
import matplotlib.pyplot as plt
import matplotlib_fontja
import matplotlib.ticker as ticker



class Plot():

    def __init__(self, json_file_path: str) -> None:
        self.json_file_path = json_file_path
        
        
    def plot(self) -> None:
        """
        jsonファイルの読み込みからグラフの作成まで行う関数
        """


        # y軸の単位を十億円に変更するフォーマッター.
        def billions(y, pos):
            return f'{y * 1e-8:,.0f}億円'
        
        # JSONファイルを読み込む.
        with open(self.json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        # figとaxオブジェクトを作成.
        fig, ax = plt.subplots(figsize=(9, 7))
        # y軸にフォーマッターを適用.
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(billions))
        
        # グラフのタイトルを設定.
        ax.set_title(f"{data['CompanyName'][1]} 決算締日: {data['EndDate'][1]}", fontsize=16, loc='center')

        # 色の指定.
        colors = {
            'Assets': '#1f77b4',
            'NonCurrentAssets': '#468cb3',
            'CurrentAssets': '#aec7e8',
            'NetAssets': '#2ca02c',
            'Liabilities': '#d62728',
            'NonCurrentLiabilities': '#b41028',
            'CurrentLiabilities': '#ff9896',
            'Interest-bearingNonCurrentLiabilities': '#9467bd',
            'Interest-bearingCurrentLiabilities': '#c5b0d5',
            'Sales': '#ff7f0e', 
            'OperatingProfits': '#d874ea',
            'NetIncome': '#f63ad6'
            }
        
        is_missing_data = {}

        def missing_checker(data: list) -> bool:
            if data[1] == -1:
                print(f'{data[0]}がありません。')
                return True
            else:
                return False
        for key, value in data.items():
            is_missing_data[key] = missing_checker(value)
        
        # 貸借対照表(借方)の棒グラフ.
        if is_missing_data['Assets'] == False:
            bar_Assets = ax.bar(1, data['Assets'][1], width=1, color=colors['Assets'])[0]
            ax.text(bar_Assets.get_x() + bar_Assets.get_width() / 2, bar_Assets.get_height() / 2,
                data['Assets'][0], ha='center', va='center', color='white', fontsize=12)
        if is_missing_data['NonCurrentAssets'] == False:
            bar_NonCurrentAssets = ax.bar(1.25, data['NonCurrentAssets'][1], width=0.5, color=colors['NonCurrentAssets'])[0]
        if is_missing_data['CurrentAssets'] == False:
            bar_CurrentAssets = ax.bar(1.25, data['CurrentAssets'][1], bottom=data['NonCurrentAssets'][1], width=0.5, color=colors['CurrentAssets'])[0]


        # 貸借対照表(貸方)の棒グラフ.
        if is_missing_data['NetAssets'] == False:
            bar_NetAssets = ax.bar(2, data['NetAssets'][1], width=1, color=colors['NetAssets'])[0]
        if is_missing_data['Liabilities'] == False:
            bar_Liabilities = ax.bar(2, data['Liabilities'][1], bottom=data['NetAssets'][1], width=1, color=colors['Liabilities'])[0]
        if is_missing_data['NonCurrentLiabilities'] == False:
            bar_NonCurrentLiabilities = ax.bar(1.75, data['NonCurrentLiabilities'][1], bottom=data['NetAssets'][1], width=0.5, color=colors['NonCurrentLiabilities'])[0]
        if is_missing_data['CurrentLiabilities'] == False:
            bar_CurrentLiabilities = ax.bar(1.75, data['CurrentLiabilities'][1], bottom=data['NonCurrentLiabilities'][1]+data['NetAssets'][1], width=0.5, color=colors['CurrentLiabilities'])[0]


        # 有利子負債の棒グラフ.
        if is_missing_data['Interest-bearingNonCurrentLiabilities'] == False:
            bar_InterestbearingNonCurrentLiabilities = ax.bar(2.75, data['Interest-bearingNonCurrentLiabilities'][1], bottom=bar_CurrentLiabilities.get_y()-data['Interest-bearingNonCurrentLiabilities'][1], width=0.5, color=colors['Interest-bearingNonCurrentLiabilities'])[0]
        if is_missing_data['Interest-bearingCurrentLiabilities'] == False:
            bar_InterestbearingCurrentLiabilities = ax.bar(2.75, data['Interest-bearingCurrentLiabilities'][1], bottom=bar_CurrentLiabilities.get_y(), width=0.5, color=colors['Interest-bearingCurrentLiabilities'])[0]


        # 損益計算書の棒グラフ.
        if is_missing_data['Sales'] == False:
            bar_Sales = ax.bar(4, data['Sales'][1], width=1, color=colors['Sales'])[0]
        if is_missing_data['OperatingProfits'] == False:
            bar_OperatingProfits = ax.bar(3.75, data['OperatingProfits'][1], width=0.5, color=colors['OperatingProfits'])[0]
        if is_missing_data['NetIncome'] ==  False:
            bar_NetIncome = ax.bar(4.25, data['NetIncome'][1], width=0.5, color=colors['NetIncome'])[0]


        # 貸借対照表(借方)につけるテキスト.
        if is_missing_data['NonCurrentAssets'] == False:
            ax.text(bar_NonCurrentAssets.get_x() + bar_NonCurrentAssets.get_width() / 2, bar_NonCurrentAssets.get_height() / 2,
                data['NonCurrentAssets'][0], ha='center', va='center', color='black', fontsize=10)
        if is_missing_data['CurrentAssets'] == False:
            ax.text(bar_CurrentAssets.get_x() + bar_CurrentAssets.get_width() / 2,
                bar_CurrentAssets.get_y() + bar_CurrentAssets.get_height() / 2,
                data['CurrentAssets'][0], ha='center', va='center', color='black', fontsize=10)

        # 貸借対照表(貸方)につけるテキスト.
        if is_missing_data['NetAssets'] == False:
            ax.text(bar_NetAssets.get_x() + bar_NetAssets.get_width() / 2, bar_NetAssets.get_height() / 2,
                data['NetAssets'][0], ha='center', va='center', color='white', fontsize=12)
        if is_missing_data['Liabilities'] == False:
            ax.text(bar_Liabilities.get_x() + bar_Liabilities.get_width() / 2, 
                bar_Liabilities.get_y() + bar_Liabilities.get_height() / 2,
                data['Liabilities'][0], ha='center', va='center', color='white', fontsize=12)
        if is_missing_data['NonCurrentLiabilities'] == False:
            ax.text(bar_NonCurrentLiabilities.get_x() + bar_NonCurrentLiabilities.get_width() / 2,
                bar_NonCurrentLiabilities.get_y() + bar_NonCurrentLiabilities.get_height() / 2,
                data['NonCurrentLiabilities'][0], ha='center', va='center', color='black', fontsize=10)
        if is_missing_data['CurrentLiabilities'] == False:
            ax.text(bar_CurrentLiabilities.get_x() + bar_CurrentLiabilities.get_width() / 2,
                bar_CurrentLiabilities.get_y() + bar_CurrentLiabilities.get_height() / 2,
                data['CurrentLiabilities'][0], ha='center', va='center', color='black', fontsize=10)

        # 有利子負債につけるテキスト.
        if is_missing_data['Interest-bearingNonCurrentLiabilities'] == False:
            ax.text(bar_InterestbearingNonCurrentLiabilities.get_x() + bar_InterestbearingNonCurrentLiabilities.get_width() / 2,
                bar_InterestbearingNonCurrentLiabilities.get_y() + bar_InterestbearingNonCurrentLiabilities.get_height() / 2,
                data['Interest-bearingNonCurrentLiabilities'][0], ha='center', va='center', color='black', fontsize=10)
        if is_missing_data['Interest-bearingCurrentLiabilities'] == False:
            ax.text(bar_InterestbearingCurrentLiabilities.get_x() + bar_InterestbearingCurrentLiabilities.get_width() / 2,
                bar_InterestbearingCurrentLiabilities.get_y() + bar_InterestbearingCurrentLiabilities.get_height() / 2,
                data['Interest-bearingCurrentLiabilities'][0], ha='center', va='center', color='black', fontsize=10)

        # 損益計算書につけるテキスト.
        if is_missing_data['Sales'] == False:
            ax.text(bar_Sales.get_x() + bar_Sales.get_width() / 2, bar_Sales.get_height() / 2,
                data['Sales'][0], ha='center', va='center', color='white', fontsize=12)
        if is_missing_data['NetIncome'] == False:
            ax.text(bar_NetIncome.get_x() + 0.25, bar_NetIncome.get_height() / 2,
                data['NetIncome'][0], ha='center', va='center', color='black', fontsize=10)
        if is_missing_data['OperatingProfits'] == False:
            ax.text(bar_OperatingProfits.get_x(), bar_OperatingProfits.get_height() / 2,
                data['OperatingProfits'][0], ha='center', va='center', color='black', fontsize=10)
                
        # B/SからP/Lに線を引く.
        if (is_missing_data['Liabilities'] or is_missing_data['Sales']) == False:
            plt.plot([bar_Liabilities.get_x() + bar_Liabilities.get_width(), bar_Sales.get_x()],
                [bar_Liabilities.get_y() + bar_Liabilities.get_height(), bar_Sales.get_height()],
                color='#751d1f')

        # x軸の目盛りを消す.
        ax.get_xaxis().set_visible(False)

        # y軸のグリッドラインを追加
        ax.yaxis.grid(True, linestyle='--', color='gray', alpha=0.7)

        # グラフを表示.
        plt.show()
