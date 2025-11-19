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
        Internal helper to plot standard curves.
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

        # Smart Date Formatting
        fig.update_xaxes(dtick="M1", tickformat="%b %Y", ticklabelmode="period")
        self._apply_common_layout(fig, title, y_label, x_label="Date")
        fig.show()

    def plot_yearly_temperature(self, df: pd.DataFrame, mode: str = 'hourly'):
        """
        Plots Temperature.
        Modes: 'hourly', 'daily', 'monthly'.
        """
        col_name = "temperature_2m"
        title = "Yearly Temperature Evolution"
        y_label = self.DATA_CONFIG["temperature"]["y_label"]

        # Config for aggregated views (Daily/Monthly share the same colors)
        agg_config = {
            'max':  {'color': '#E74C3C', 'name': 'Max',  'width': 1}, # Red
            'mean': {'color': '#2ECC71', 'name': 'Mean', 'width': 3}, # Green
            'min':  {'color': '#3498DB', 'name': 'Min',  'width': 1}  # Blue
        }

        if mode == 'hourly':
            config = {col_name: {'color': '#2ECC71', 'name': 'Hourly Temperature', 'width': 1}}
            self._plot_pandas_curves(df, config, f"{title} (Hourly)", y_label)

        elif mode == 'daily':
            # Resample by Day
            daily_df = df[col_name].resample('D').agg(['min', 'max', 'mean'])
            self._plot_pandas_curves(daily_df, agg_config, f"{title} (Daily Stats)", y_label)

        elif mode == 'monthly':
            # Resample by Month Start ('MS')
            monthly_df = df[col_name].resample('MS').agg(['min', 'max', 'mean'])
            self._plot_pandas_curves(monthly_df, agg_config, f"{title} (Monthly Stats)", y_label)

        else:
            print(f"Error: Unknown mode '{mode}'.")

    def plot_yearly_humidity(self, df: pd.DataFrame, mode: str = 'hourly'):
        """
        Plots Relative Humidity.
        Modes: 'hourly', 'daily', 'monthly'.
        """
        col_name = "relative_humidity_2m"
        title = "Yearly Relative Humidity Evolution"
        y_label = self.DATA_CONFIG["relative_humidity"]["y_label"]

        # Config for aggregated views (Daily/Monthly share the same colors)
        agg_config = {
            'max':  {'color': "#322AAA", 'name': 'Max',  'width': 1}, # Dark Blue
            'mean': {'color': '#3498DB', 'name': 'Mean', 'width': 3}, # Blue
            'min':  {'color': "#84BCDA", 'name': 'Min',  'width': 1}  # Light Blue
        }

        if mode == 'hourly':
            config = {col_name: {'color': '#3498DB', 'name': 'Hourly Relative Humidity', 'width': 1}}
            self._plot_pandas_curves(df, config, f"{title} (Hourly)", y_label)

        elif mode == 'daily':
            # Resample by Day
            daily_df = df[col_name].resample('D').agg(['min', 'max', 'mean'])
            self._plot_pandas_curves(daily_df, agg_config, f"{title} (Daily Stats)", y_label)

        elif mode == 'monthly':
            # Resample by Month Start ('MS')
            monthly_df = df[col_name].resample('MS').agg(['min', 'max', 'mean'])
            self._plot_pandas_curves(monthly_df, agg_config, f"{title} (Monthly Stats)", y_label)

        else:
            print(f"Error: Unknown mode '{mode}'.")

    def plot_yearly_solar_radiation(self, df: pd.DataFrame, mode: str = 'hourly'):
        """
        Plots Solar Radiation.
        Modes:
         - 'hourly': Raw curves.
         - 'daily' / 'monthly': 6 curves (Mean and Max for Total, Direct, Diffuse).
        """
        # 1. Ensure Total Radiation exists
        if "total_radiation" not in df.columns:
            df = df.copy()
            df["total_radiation"] = df["diffuse_radiation"] + df["direct_radiation"]

        title = "Solar Radiation Analysis"
        y_label = self.DATA_CONFIG["solar_radiation"]["y_label"]

        # --- HOURLY MODE ---
        if mode == 'hourly':
            config = {
                "diffuse_radiation": {'color': '#F1C40F', 'name': 'Diffuse', 'width': 1}, # Yellow
                "direct_radiation":  {'color': '#E67E22', 'name': 'Direct',  'width': 1}, # Orange
                "total_radiation":   {'color': '#C0392B', 'name': 'Total',   'width': 2}  # Red
            }
            self._plot_pandas_curves(df, config, f"{title} (Hourly)", y_label)
            return

        # --- AGGREGATED MODES (Daily / Monthly) ---

        # Determine frequency: 'D' for Daily, 'MS' for Month Start
        freq = 'D' if mode == 'daily' else 'MS'
        title_suffix = "Daily Stats" if mode == 'daily' else "Monthly Stats"

        # Resample and calculate Mean and Max for all 3 types
        agg_df = df[["total_radiation", "direct_radiation", "diffuse_radiation"]].resample(freq).agg(['mean', 'max'])

        fig = go.Figure()

        # Helper internal function to keep code DRY (Don't Repeat Yourself)
        def add_trace_pair(name_base, col_name, color):
            # 1. Mean Curve (Solid line)
            fig.add_trace(go.Scatter(
                x=agg_df.index,
                y=agg_df[col_name]['mean'],
                mode='lines',
                name=f'{name_base} (Mean)',
                line=dict(color=color, width=3)
            ))
            # 2. Max Curve (Dotted line + Markers)
            fig.add_trace(go.Scatter(
                x=agg_df.index,
                y=agg_df[col_name]['max'],
                mode='lines+markers',
                name=f'{name_base} (Max)',
                line=dict(color=color, width=1, dash='dot'),
                marker=dict(size=4)
            ))

        # Add the 3 pairs of curves
        # Total -> Red
        add_trace_pair("Total", "total_radiation", "#C0392B")
        # Direct -> Orange
        add_trace_pair("Direct", "direct_radiation", "#E67E22")
        # Diffuse -> Darker Yellow
        add_trace_pair("Diffuse", "diffuse_radiation", "#F39C12")

        # Apply layout
        fig.update_xaxes(dtick="M1", tickformat="%b %Y", ticklabelmode="period")
        self._apply_common_layout(fig, f"{title} ({title_suffix})", y_label, x_label="Date")
        fig.show()