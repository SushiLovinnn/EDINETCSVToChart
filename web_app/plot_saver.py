import os
import matplotlib.pyplot as plt

class PlotSaver:
    def __init__(self, session_dir, show_chart=True):
        self.session_dir = session_dir
        self.show_chart = show_chart

    def save_plots(self, plots):
        plot_paths = []
        for i, plot in enumerate(plots):
            plot_path = os.path.join(self.session_dir, f'plot_{i}.png')
            plot.save_fig=True
            plot.save_path=plot_path
            fig = plot.plot()
            plot_paths.append(plot_path)
            print(f"Plot saved to {plot_path}")

        return plot_paths

    def show_plots(self, plot_paths):
        if self.show_chart:
            for plot_path in plot_paths:
                img = plt.imread(plot_path)
                plt.imshow(img)
                plt.show()

    def delete_plots(self, plot_paths):
        for plot_path in plot_paths:
            if os.path.exists(plot_path):
                os.remove(plot_path)
                print(f"Plot removed from {plot_path}")
        # セッションディレクトリを削除
        if os.path.exists(self.session_dir):
            os.rmdir(self.session_dir)
            print(f"Directory removed: {self.session_dir}")