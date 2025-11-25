from kub.course.plotlib.basePlotFactory import BasePlotFactory
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, Tuple

class SimulationPlotFactory(BasePlotFactory):
    """
    Factory specialized for Building Simulation outputs.
    Input format: Dictionaries of Numpy Arrays.
    """

    def _convert_time_unit(self, time_arr: np.ndarray) -> Tuple[np.ndarray, str]:
        """
        Internal helper to convert time into Hours or Days if the simulation is long enough.

        Returns:
            (new_time_array, time_label)
        """
        if time_arr.size == 0:
            return time_arr, "Time (s)"

        max_time = np.max(time_arr)

        if max_time >= 172800:
            return time_arr / 86400.0, "Time (days)"
        elif max_time > 3600:
            return time_arr / 3600.0, "Time (h)"
        else:
            return time_arr, "Time (s)"

    def plot_subplots(self, time: np.ndarray, data_type: str, data_dict: Dict[str, np.ndarray], title: str, show: bool = True):
        """
        Creates a figure with 1 row and N columns (one subplot per curve).
        
        Args:
            time: Time array
            data_type: Type of data (temperature, heat_flux, etc.)
            data_dict: Dictionary of data arrays
            title: Plot title
            show: Whether to display the plot (default True)
        
        Returns:
            Plotly figure object
        """
        # Convert Data
        y_data, y_label = self._convert_data(data_type, data_dict)

        # Convert Time
        x_vals, x_label = self._convert_time_unit(time)

        # Setup Subplots
        cols = len(y_data)
        fig = make_subplots(rows=1, cols=cols, shared_xaxes=True,
                            subplot_titles=list(y_data.keys()))

        # Add Traces
        for i, (label, y) in enumerate(y_data.items(), start=1):
            fig.add_trace(go.Scatter(x=x_vals, y=y, mode="lines", name=label),
                          row=1, col=i)
            fig.update_yaxes(title_text=y_label, row=1, col=i)
            fig.update_xaxes(title_text=x_label, row=1, col=i)

        # Final Layout
        fig.update_layout(width=600 * cols, title_text=title)
        if show:
            fig.show()
        return fig

    def plot_multi_curves(self, time: np.ndarray, data_type: str, data_dict: Dict[str, np.ndarray], title: str, show: bool = True):
        """
        Plots all curves on a single chart.
        
        Args:
            time: Time array
            data_type: Type of data (temperature, heat_flux, etc.)
            data_dict: Dictionary of data arrays
            title: Plot title
            show: Whether to display the plot (default True)
        
        Returns:
            Plotly figure object
        """
        # Convert Data
        y_data, y_label = self._convert_data(data_type, data_dict)

        # Convert Time
        x_vals, x_label = self._convert_time_unit(time)

        # Setup Figure
        fig = go.Figure()
        for label, y in y_data.items():
            fig.add_trace(go.Scatter(x=x_vals, y=y, mode="lines", name=label))

        # Final Layout
        self._apply_common_layout(fig, title, y_label, x_label=x_label)
        if show:
            fig.show()
        return fig