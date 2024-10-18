import os
import matplotlib.pyplot as plt
from flask import session
import uuid

class PlotSaver:
    def __init__(self, show_chart=True):
        self.show_chart = show_chart

    def save_plots(self, plots):
        session_id = session.get('session_id', str(uuid.uuid4()))
        session['session_id'] = session_id

        plot_paths = []
        for i, plot in enumerate(plots):
            plot_path = os.path.join('static', 'plots', f'{session_id}_plot_{i}.png')
            plot.savefig(plot_path)
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