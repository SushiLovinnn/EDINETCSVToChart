import json
import matplotlib.pyplot as plt
import matplotlib_fontja
import matplotlib.ticker as ticker



class Plot():
    """
    test
    """

    def __init__(self, json_file_path: str) -> None:
        self.json_file_path = json_file_path
        
        
    def plot(self) -> None:
        """
        jsonファイルの読み込みからグラフの作成まで行う関数
        """


        # y軸の単位を十億円に変更するフォーマッター.
        def billions(y, pos):
            return f'{y * 1e-9:,.0f}億円'
        
        # JSONファイルを読み込む.
        with open(self.json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        # FigureとAxesオブジェクトを作成.
        fig, ax = plt.subplots(figsize=(9, 7))
        # y軸にフォーマッターを適用.
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(billions))
        
        # グラフのタイトルを設定.
        ax.set_title(f'{data['CompanyName'][1]} 決算締日: {data['EndDate'][1]}', fontsize=16, loc='center')

        # 色の指定.
        colors: dict = {
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

        # 貸借対照表(借方)の棒グラフ.
        bar_Assets = ax.bar(1, data['Assets'][1], width=1, color=colors['Assets'])[0]
        bar_NonCurrentAssets = ax.bar(1.25, data['NonCurrentAssets'][1], width=0.5, color=colors['NonCurrentAssets'])[0]
        bar_CurrentAssets = ax.bar(1.25, data['CurrentAssets'][1], bottom=data['NonCurrentAssets'][1], width=0.5, color=colors['CurrentAssets'])[0]

        # 貸借対照表(貸方)の棒グラフ.
        bar_NetAssets = ax.bar(2, data['NetAssets'][1], width=1, color=colors['NetAssets'])[0]
        bar_Liabilities = ax.bar(2, data['Liabilities'][1], bottom=data['NetAssets'][1], width=1, color=colors['Liabilities'])[0]
        bar_NonCurrentLiabilities = ax.bar(1.75, data['NonCurrentLiabilities'][1], bottom=data['NetAssets'][1], width=0.5, color=colors['NonCurrentLiabilities'])[0]
        bar_CurrentLiabilities = ax.bar(1.75, data['CurrentLiabilities'][1], bottom=data['NonCurrentLiabilities'][1]+data['NetAssets'][1], width=0.5, color=colors['CurrentLiabilities'])[0]

        # 有利子負債の棒グラフ.
        bar_InterestbearingNonCurrentLiabilities = ax.bar(2.75, data['Interest-bearingNonCurrentLiabilities'][1], bottom=bar_CurrentLiabilities.get_y()-data['Interest-bearingNonCurrentLiabilities'][1], width=0.5, color=colors['Interest-bearingNonCurrentLiabilities'])[0]
        bar_InterestbearingCurrentLiabilities = ax.bar(2.75, data['Interest-bearingCurrentLiabilities'][1], bottom=bar_CurrentLiabilities.get_y(), width=0.5, color=colors['Interest-bearingCurrentLiabilities'])[0]

        # 損益計算書の棒グラフ.
        bar_Sales = ax.bar(4, data['Sales'][1], width=1, color=colors['Sales'])[0]
        bar_OperatingProfits = ax.bar(3.75, data['OperatingProfits'][1], width=0.5, color=colors['OperatingProfits'])[0]
        bar_NetIncome = ax.bar(4.25, data['NetIncome'][1], width=0.5, color=colors['NetIncome'])[0]

        # 貸借対照表(借方)につけるテキスト.
        ax.text(bar_Assets.get_x() + bar_Assets.get_width() / 2, bar_Assets.get_height() / 2,
                data['Assets'][0], ha='center', va='center', color='white', fontsize=12)

        ax.text(bar_NonCurrentAssets.get_x() + bar_NonCurrentAssets.get_width() / 2, bar_NonCurrentAssets.get_height() / 2,
                data['NonCurrentAssets'][0], ha='center', va='center', color='black', fontsize=10)

        ax.text(bar_CurrentAssets.get_x() + bar_CurrentAssets.get_width() / 2,
                bar_CurrentAssets.get_y() + bar_CurrentAssets.get_height() / 2,
                data['CurrentAssets'][0], ha='center', va='center', color='black', fontsize=10)

        # 貸借対照表(貸方)につけるテキスト.
        ax.text(bar_NetAssets.get_x() + bar_NetAssets.get_width() / 2, bar_NetAssets.get_height() / 2,
                data['NetAssets'][0], ha='center', va='center', color='white', fontsize=12)

        ax.text(bar_Liabilities.get_x() + bar_Liabilities.get_width() / 2, 
                bar_Liabilities.get_y() + bar_Liabilities.get_height() / 2,
                data['Liabilities'][0], ha='center', va='center', color='white', fontsize=12)

        ax.text(bar_NonCurrentLiabilities.get_x() + bar_NonCurrentLiabilities.get_width() / 2,
                bar_NonCurrentLiabilities.get_y() + bar_NonCurrentLiabilities.get_height() / 2,
                data['NonCurrentLiabilities'][0], ha='center', va='center', color='black', fontsize=10)

        ax.text(bar_CurrentLiabilities.get_x() + bar_CurrentLiabilities.get_width() / 2,
                bar_CurrentLiabilities.get_y() + bar_CurrentLiabilities.get_height() / 2,
                data['CurrentLiabilities'][0], ha='center', va='center', color='black', fontsize=10)

        # 有利子負債につけるテキスト.
        ax.text(bar_InterestbearingNonCurrentLiabilities.get_x() + bar_InterestbearingNonCurrentLiabilities.get_width() / 2,
                bar_InterestbearingNonCurrentLiabilities.get_y() + bar_InterestbearingNonCurrentLiabilities.get_height() / 2,
                data['Interest-bearingNonCurrentLiabilities'][0], ha='center', va='center', color='black', fontsize=10)

        ax.text(bar_InterestbearingCurrentLiabilities.get_x() + bar_InterestbearingCurrentLiabilities.get_width() / 2,
                bar_InterestbearingCurrentLiabilities.get_y() + bar_InterestbearingCurrentLiabilities.get_height() / 2,
                data['Interest-bearingCurrentLiabilities'][0], ha='center', va='center', color='black', fontsize=10)

        # 損益計算書につけるテキスト.
        ax.text(bar_Sales.get_x() + bar_Sales.get_width() / 2, bar_Sales.get_height() / 2,
                data['Sales'][0], ha='center', va='center', color='white', fontsize=12)

        ax.text(bar_NetIncome.get_x() + 0.25, bar_NetIncome.get_height() / 2,
                data['NetIncome'][0], ha='center', va='center', color='black', fontsize=10)

        ax.text(bar_OperatingProfits.get_x(), bar_OperatingProfits.get_height() / 2,
                data['OperatingProfits'][0], ha='center', va='center', color='black', fontsize=10)
                
        # B/SからP/Lに線を引く.
        plt.plot([bar_Liabilities.get_x() + bar_Liabilities.get_width(), bar_Sales.get_x()],
                [bar_Liabilities.get_y() + bar_Liabilities.get_height(), bar_Sales.get_height()],
                color='#751d1f')

        # x軸の目盛りを消す.
        ax.get_xaxis().set_visible(False)

        # y軸のグリッドラインを追加
        ax.yaxis.grid(True, linestyle='--', color='gray', alpha=0.7)
        # データの出力.
        for key, val in data.items():
            print(f'{val[0]}: {val[1]} key: {key}')

        # グラフを表示.
        plt.show()
