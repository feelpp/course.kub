from kub.course.plotlib.basePlotFactory import BasePlotFactory
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, Union, Optional

class SimulationPlotFactory(BasePlotFactory):
    """
    Factory specialized for Building Simulation outputs.
    Input format: Dictionaries of Numpy Arrays.
    """

    def plot_subplots(self, time: np.ndarray, data_type: str, data_dict: Dict[str, np.ndarray], title: str):
        """
        Creates a figure with 1 row and N columns (one subplot per curve).
        """
        # 1. Convert Data
        y_data, y_label = self._convert_data(data_type, data_dict)

        # 2. Setup Subplots
        cols = len(y_data)
        fig = make_subplots(rows=1, cols=cols, shared_xaxes=True,
                            subplot_titles=list(y_data.keys()))

        # 3. Add Traces
        for i, (label, y) in enumerate(y_data.items(), start=1):
            fig.add_trace(go.Scatter(x=time, y=y, mode="lines", name=label),
                          row=1, col=i)
            fig.update_yaxes(title_text=y_label, row=1, col=i)
            fig.update_xaxes(title_text="Time (s)", row=1, col=i)

        # 4. Final Layout
        fig.update_layout(width=600 * cols, title_text=title)
        fig.show()

    def plot_multi_curves(self, time: np.ndarray, data_type: str, data_dict: Dict[str, np.ndarray], title: str):
        """
        Plots all curves on a single chart.
        """
        # 1. Convert Data
        y_data, y_label = self._convert_data(data_type, data_dict)

        # 2. Setup Figure
        fig = go.Figure()
        for label, y in y_data.items():
            fig.add_trace(go.Scatter(x=time, y=y, mode="lines", name=label))

        # 3. Final Layout
        self._apply_common_layout(fig, title, y_label, x_label="Time (s)")
        fig.show()