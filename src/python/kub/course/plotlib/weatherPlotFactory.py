from kub.course.plotlib.basePlotFactory import BasePlotFactory
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Union, Optional

class WeatherPlotFactory(BasePlotFactory):
    """
    Factory specialized for Weather Data Analysis.
    Input format: Pandas DataFrames with DateTimeIndex.
    """

    def _plot_pandas_curves(self, df: pd.DataFrame, columns_config: dict, title: str, y_label: str):
        """
        Internal helper to plot curves from a DataFrame based on a config dict.
        """
        fig = go.Figure()

        for col_name, style in columns_config.items():
            if col_name in df.columns:
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[col_name],
                    mode="lines",
                    name=style.get('name', col_name),
                    line=dict(color=style.get('color'), width=style.get('width', 2))
                ))

        # Smart Date Formatting for X-Axis
        fig.update_xaxes(
            dtick="M1",          # Tick every 1 Month
            tickformat="%b %Y",  # "Jan 2023"
            ticklabelmode="period"
        )

        self._apply_common_layout(fig, title, y_label, x_label="Date")
        fig.show()

    def plot_yearly_temperature(self, df: pd.DataFrame, mode: str = 'hourly'):
        """
        Plots Temperature.
        Mode 'hourly': Raw data.
        Mode 'daily': Aggregated Min/Mean/Max.
        """
        col_name = "temperature_2m"
        title = "Yearly Temperature Evolution"
        # Note: We assume weather data is already in °C, so we fetch label but skip conversion logic here
        # If needed, we could call self._convert_data logic, but usually pandas data is pre-processed.
        y_label = self.DATA_CONFIG["temperature"]["y_label"]

        if mode == 'hourly':
            config = {col_name: {'color': '#2ECC71', 'name': 'Temperature', 'width': 1}} # Green
            self._plot_pandas_curves(df, config, f"{title} (Hourly)", y_label)

        elif mode == 'daily':
            # Resample: Get Min, Max, Mean per day
            daily_df = df[col_name].resample('D').agg(['min', 'max', 'mean'])

            config = {
                'max':  {'color': '#E74C3C', 'name': 'Daily Max',  'width': 1}, # Red
                'mean': {'color': '#2ECC71', 'name': 'Daily Mean', 'width': 3}, # Green
                'min':  {'color': '#3498DB', 'name': 'Daily Min',  'width': 1}  # Blue
            }
            self._plot_pandas_curves(daily_df, config, f"{title} (Daily Stats)", y_label)

    def plot_yearly_solar_radiation(self, df: pd.DataFrame, mode: str = 'hourly'):
        """
        Plots Solar Radiation (Diffuse, Direct, Total).
        """
        # Calculate Total if missing
        if "total_radiation" not in df.columns:
            df = df.copy()
            df["total_radiation"] = df["diffuse_radiation"] + df["direct_radiation"]

        title = "Yearly Solar Radiation"
        y_label = self.DATA_CONFIG["solar_radiation"]["y_label"]

        if mode == 'hourly':
            config = {
                "diffuse_radiation": {'color': '#F1C40F', 'name': 'Diffuse', 'width': 1}, # Yellow
                "direct_radiation":  {'color': '#E67E22', 'name': 'Direct',  'width': 1}, # Orange
                "total_radiation":   {'color': '#C0392B', 'name': 'Total',   'width': 2}  # Red
            }
            self._plot_pandas_curves(df, config, f"{title} (Hourly)", y_label)

        elif mode == 'daily':
            # Stats on TOTAL radiation
            daily_df = df["total_radiation"].resample('D').agg(['min', 'max', 'mean'])

            config = {
                'max':  {'color': '#C0392B', 'name': 'Max Total',  'width': 1},
                'mean': {'color': '#E67E22', 'name': 'Mean Total', 'width': 3},
                'min':  {'color': '#F1C40F', 'name': 'Min Total',  'width': 1}
            }
            self._plot_pandas_curves(daily_df, config, f"{title} (Daily Total Stats)", y_label)