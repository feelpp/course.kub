from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from kub.course.plotlib.basePlotFactory import BasePlotFactory


class WeatherPlotFactory(BasePlotFactory):
    """
    Factory specialized for Weather Data Analysis with interactive menus.
    """

    def _add_aggregated_traces(
        self,
        fig: go.Figure,
        df: pd.DataFrame,
        col_name: str,
        freq: str,
        label_suffix: str,
        colors: dict,
        visible: bool = False,
    ):
        """
        Private helper to add standard Min/Mean/Max traces (Temperature, Humidity).
        Returns the number of traces added.
        """
        # Resample
        agg = df[col_name].resample(freq).agg(["min", "max", "mean"])

        # Precise date format for hover
        date_fmt = "%d %b %Y" if freq == "D" else "%b %Y"

        # 1. Max (Dotted line)
        fig.add_trace(
            go.Scatter(
                x=agg.index,
                y=agg["max"],
                mode="lines",
                name=f"Max ({label_suffix})",
                line={"color": colors["max"]["color"], "width": 1, "dash": "dot"},
                visible=visible,
                hovertemplate=f"<b>Date</b>: %{{x|{date_fmt}}}<br><b>Max</b>: %{{y:.2f}}<extra></extra>",
            )
        )

        # 2. Mean (Solid thick line)
        fig.add_trace(
            go.Scatter(
                x=agg.index,
                y=agg["mean"],
                mode="lines",
                name=f"Mean ({label_suffix})",
                line={"color": colors["mean"]["color"], "width": 3},
                visible=visible,
                hovertemplate=f"<b>Date</b>: %{{x|{date_fmt}}}<br><b>Mean</b>: %{{y:.2f}}<extra></extra>",
            )
        )

        # 3. Min (Thin line)
        fig.add_trace(
            go.Scatter(
                x=agg.index,
                y=agg["min"],
                mode="lines",
                name=f"Min ({label_suffix})",
                line={"color": colors["min"]["color"], "width": 1},
                visible=visible,
                hovertemplate=f"<b>Date</b>: %{{x|{date_fmt}}}<br><b>Min</b>: %{{y:.2f}}<extra></extra>",
            )
        )

        return 3  # Added 3 traces

    def _create_update_menu(
        self, traces_indices: dict[str, list[int]], total_traces: int
    ) -> dict:
        """
        Creates the dropdown menu configuration based on trace indices.
        """
        buttons = []

        for label, indices in traces_indices.items():
            # Create a visibility mask [False, False, True, ...]
            visibility = [False] * total_traces
            for i in indices:
                visibility[i] = True

            buttons.append(
                {
                    "label": label,
                    "method": "update",
                    "args": [
                        {"visible": visibility},
                        {"title": f"View: {label}"},
                    ],  # Optional: update title
                }
            )

        return {
            "active": 0,  # The first button is active by default
            "buttons": buttons,
            "x": 1.1,  # Position on the right
            "y": 1,
            "xanchor": "left",
            "yanchor": "top",
        }

    # -------------------------------------------------------------------------
    # PLOTTING METHODS
    # -------------------------------------------------------------------------

    def plot_yearly_temperature(self, df: pd.DataFrame):
        col_name = "temperature_2m"
        title = "Yearly Temperature Evolution"
        y_label = self.DATA_CONFIG["temperature"]["y_label"]

        fig = go.Figure()
        trace_idx = 0
        indices = {}  # Stores indices for each view: {'Hourly': [0], 'Daily': [1,2,3]...}

        # --- 1. HOURLY TRACE (Default View) ---
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[col_name],
                mode="lines",
                name="Hourly",
                line={"color": "#2ECC71", "width": 1},
                visible=True,  # Visible at start
                hovertemplate="<b>Date</b>: %{x|%d %b %Y %H:%M}<br><b>Temp</b>: %{y:.2f}°C<extra></extra>",
            )
        )
        indices["Hourly"] = [trace_idx]
        trace_idx += 1

        # Colors for aggregations
        agg_colors = {
            "max": {"color": "#E74C3C"},
            "mean": {"color": "#2ECC71"},
            "min": {"color": "#3498DB"},
        }

        # --- 2. DAILY TRACES ---
        count = self._add_aggregated_traces(
            fig, df, col_name, "D", "Daily", agg_colors, visible=False
        )
        indices["Daily"] = list(range(trace_idx, trace_idx + count))
        trace_idx += count

        # --- 3. MONTHLY TRACES ---
        count = self._add_aggregated_traces(
            fig, df, col_name, "MS", "Monthly", agg_colors, visible=False
        )
        indices["Monthly"] = list(range(trace_idx, trace_idx + count))
        trace_idx += count

        # --- LAYOUT & MENUS ---
        fig.update_layout(updatemenus=[self._create_update_menu(indices, trace_idx)])

        # Smart Date Formatting on X Axis
        fig.update_xaxes(dtick="M1", tickformat="%b %Y", ticklabelmode="period")
        self._apply_common_layout(fig, title, y_label, x_label="Date")
        fig.show()

    def plot_yearly_humidity(self, df: pd.DataFrame):
        col_name = "relative_humidity_2m"
        title = "Yearly Relative Humidity"
        y_label = self.DATA_CONFIG["relative_humidity"]["y_label"]

        fig = go.Figure()
        trace_idx = 0
        indices = {}

        # --- 1. HOURLY ---
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[col_name],
                mode="lines",
                name="Hourly",
                line={"color": "#3498DB", "width": 1},
                visible=True,
                hovertemplate="<b>Date</b>: %{x|%d %b %Y %H:%M}<br><b>RH</b>: %{y:.1f}%<extra></extra>",
            )
        )
        indices["Hourly"] = [trace_idx]
        trace_idx += 1

        # Colors
        agg_colors = {
            "max": {"color": "#322AAA"},
            "mean": {"color": "#3498DB"},
            "min": {"color": "#84BCDA"},
        }

        # --- 2. DAILY ---
        count = self._add_aggregated_traces(
            fig, df, col_name, "D", "Daily", agg_colors, visible=False
        )
        indices["Daily"] = list(range(trace_idx, trace_idx + count))
        trace_idx += count

        # --- 3. MONTHLY ---
        count = self._add_aggregated_traces(
            fig, df, col_name, "MS", "Monthly", agg_colors, visible=False
        )
        indices["Monthly"] = list(range(trace_idx, trace_idx + count))
        trace_idx += count

        # --- LAYOUT ---
        fig.update_layout(updatemenus=[self._create_update_menu(indices, trace_idx)])
        fig.update_xaxes(dtick="M1", tickformat="%b %Y", ticklabelmode="period")
        self._apply_common_layout(fig, title, y_label, x_label="Date")
        fig.show()

    def plot_yearly_solar_radiation(self, df: pd.DataFrame):
        # Ensure Total Radiation exists
        if "total_radiation" not in df.columns:
            df = df.copy()
            df["total_radiation"] = df["diffuse_radiation"] + df["direct_radiation"]

        title = "Solar Radiation Analysis"
        y_label = self.DATA_CONFIG["solar_radiation"]["y_label"]

        fig = go.Figure()
        trace_idx = 0
        indices = {}

        # Config colors
        rad_config = {
            "diffuse_radiation": {"color": "#F1C40F", "name": "Diffuse"},
            "direct_radiation": {"color": "#E67E22", "name": "Direct"},
            "total_radiation": {"color": "#C0392B", "name": "Total"},
        }

        # --- 1. HOURLY VIEW (3 curves) ---
        start_idx = trace_idx
        for col, style in rad_config.items():
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[col],
                    mode="lines",
                    name=style["name"],
                    line={"color": style["color"], "width": 1},
                    visible=True,
                    hovertemplate=f"<b>Date</b>: %{{x|%d %b %Y %H:%M}}<br><b>{style['name']}</b>: %{{y:.1f}}<extra></extra>",
                )
            )
            trace_idx += 1
        indices["Hourly"] = list(range(start_idx, trace_idx))

        # --- HELPER FOR AGGREGATED SOLAR (Daily/Monthly) ---
        def add_solar_agg(freq_code, suffix):
            nonlocal trace_idx
            start_sub = trace_idx
            # Calculate Mean and Max for all 3 radiation types
            agg_df = (
                df[list(rad_config.keys())].resample(freq_code).agg(["mean", "max"])
            )

            date_fmt = "%d %b %Y" if freq_code == "D" else "%b %Y"

            for col, style in rad_config.items():
                # Mean
                fig.add_trace(
                    go.Scatter(
                        x=agg_df.index,
                        y=agg_df[col]["mean"],
                        mode="lines",
                        name=f"{style['name']} Mean ({suffix})",
                        line={"color": style["color"], "width": 3},
                        visible=False,
                        hovertemplate=f"<b>Date</b>: %{{x|{date_fmt}}}<br><b>Mean</b>: %{{y:.1f}}<extra></extra>",
                    )
                )
                trace_idx += 1
                # Max
                fig.add_trace(
                    go.Scatter(
                        x=agg_df.index,
                        y=agg_df[col]["max"],
                        mode="lines+markers",
                        name=f"{style['name']} Max ({suffix})",
                        line={"color": style["color"], "width": 1, "dash": "dot"},
                        marker={"size": 4},
                        visible=False,
                        hovertemplate=f"<b>Date</b>: %{{x|{date_fmt}}}<br><b>Max</b>: %{{y:.1f}}<extra></extra>",
                    )
                )
                trace_idx += 1
            return list(range(start_sub, trace_idx))

        # --- 2. DAILY VIEW ---
        indices["Daily"] = add_solar_agg("D", "Daily")

        # --- 3. MONTHLY VIEW ---
        indices["Monthly"] = add_solar_agg("MS", "Monthly")

        # --- LAYOUT ---
        fig.update_layout(updatemenus=[self._create_update_menu(indices, trace_idx)])
        fig.update_xaxes(dtick="M1", tickformat="%b %Y", ticklabelmode="period")
        self._apply_common_layout(fig, title, y_label, x_label="Date")
        fig.show()

    def _prepare_wind_data(self, df: pd.DataFrame, speed_col: str, dir_col: str):
        """
        Transforms raw data (Time Series) into frequency data for the Wind Rose.
        """
        # 1. Define speed bins
        # Ex: 0-5 km/h, 5-10, 10-20, 20-30, 30-50, >50
        speed_bins = [0, 5, 10, 20, 30, 50, 200]
        speed_labels = [
            "< 5 km/h",
            "5-10 km/h",
            "10-20 km/h",
            "20-30 km/h",
            "30-50 km/h",
            "> 50 km/h",
        ]
        # Associated colors (Blue -> Green -> Yellow -> Red)
        colors = ["#48bfe3", "#56cfe1", "#64dfdf", "#ffba08", "#e85d04", "#d00000"]

        df_rose = df.copy()

        # 2. Categorize speeds
        df_rose["speed_cat"] = pd.cut(
            df_rose[speed_col],
            bins=speed_bins,
            labels=speed_labels,
            include_lowest=True,
        )

        # 3. Categorize directions (Convert 0-360 to N, NNE, etc.)
        # Shift by 11.25° to center North on 0
        dirs = np.arange(0, 361, 22.5)
        dir_labels = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW",
            "N",
        ]

        # Trick to handle North which is both 0 and 360: use pd.cut
        df_rose["dir_cat"] = pd.cut(
            df_rose[dir_col], bins=dirs, labels=dir_labels[:-1], include_lowest=True
        )
        # Replace NaN (exact 360) with N
        df_rose["dir_cat"] = df_rose["dir_cat"].fillna("N")

        # 4. Create contingency table (How many hours per Direction AND per Speed?)
        wind_dist = pd.crosstab(df_rose["dir_cat"], df_rose["speed_cat"])

        # Convert to percentage
        total_count = len(df_rose)
        wind_dist_pct = (wind_dist / total_count) * 100

        return wind_dist_pct, speed_labels, colors

    def plot_wind_rose(self, df: pd.DataFrame):
        """
        Displays the Wind Rose (Frequency & Intensity) using Plotly Barpolar.
        """
        speed_col = "wind_speed_10m"
        dir_col = "wind_direction_10m"
        title = "Wind Rose Diagram (Frequency & Intensity)"

        # Prepare aggregated data
        df_pct, speed_labels, colors = self._prepare_wind_data(df, speed_col, dir_col)

        fig = go.Figure()

        # Stack bars: start with low speeds, then add higher speeds on top
        for i, label in enumerate(speed_labels):
            if label in df_pct.columns:
                fig.add_trace(
                    go.Barpolar(
                        r=df_pct[label],  # Radius (Frequency in %)
                        theta=df_pct.index,  # Angle (Direction N, NE...)
                        name=label,  # Legend (Speed)
                        marker_color=colors[i],
                        marker_line_color="black",
                        marker_line_width=0.5,
                        hoverinfo=["all"],
                    )
                )

        # Polar layout config
        fig.update_layout(
            title=title,
            font_size=12,
            legend_font_size=10,
            polar={
                "bgcolor": "rgb(245, 245, 245)",
                "radialaxis": {
                    "visible": True,
                    "range": [
                        0,
                        df_pct.sum(axis=1).max() + 1,
                    ],  # Adjust max scale to longest arm
                    "ticksuffix": "%",
                    "angle": 45,
                    "dtick": 5,  # Line every 5%
                },
                "angularaxis": {
                    "direction": "clockwise",  # Clockwise
                    "period": 6,
                },
            },
            # Force "stacked" mode
            barmode="stack",
        )

        # No common_layout call here because it is polar, not cartesian
        fig.show()

    def plot_cloud_layers(self, df: pd.DataFrame):
        """
        Visualizes the 3 cloud layers as an atmospheric cross-section.
        Uses filled areas with transparency for Hourly, Daily, and Monthly views.
        """
        # Check columns
        required = ["cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"]
        if not all(col in df.columns for col in required):
            return

        title = "Cloud Cover Analysis (Atmospheric Layers)"
        y_label = "% Coverage"

        fig = go.Figure()
        trace_idx = 0
        indices = {}

        # Define "Atmospheric" styles
        # Low = Bottom/Dark / High = Top/Light
        layers_config = {
            "cloud_cover_high": {
                "color": "#BDC3C7",
                "name": "High Clouds (>8km)",
            },  # Very light gray
            "cloud_cover_mid": {
                "color": "#7F8C8D",
                "name": "Mid Clouds (3-8km)",
            },  # Medium gray
            "cloud_cover_low": {
                "color": "#2C3E50",
                "name": "Low Clouds (0-3km)",
            },  # Dark gray / Dark blue
        }

        # Helper to add filled traces for any frequency (Hourly/Daily/Monthly)
        def add_cloud_traces(freq_code, label_suffix, visible_flag):
            nonlocal trace_idx
            start_sub = trace_idx

            # Resample logic (Mean for Daily/Monthly, Raw for Hourly)
            if freq_code == "hourly":
                data = df
                date_fmt = "%d %b %Y %H:%M"
            else:
                data = df[list(layers_config.keys())].resample(freq_code).mean()
                date_fmt = "%d %b %Y" if freq_code == "D" else "%b %Y"

            # Loop through layers
            for col, style in layers_config.items():
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data[col],
                        mode="lines",
                        name=f"{style['name']} ({label_suffix})",
                        line={
                            "color": style["color"],
                            "width": 0,
                        },  # No outline, just fill
                        fill="tozeroy",  # Fill area
                        opacity=0.5,  # Transparency
                        visible=visible_flag,
                        hovertemplate=f"<b>Date</b>: %{{x|{date_fmt}}}<br><b>{style['name']}</b>: %{{y:.0f}}%<extra></extra>",
                    )
                )
                trace_idx += 1
            return list(range(start_sub, trace_idx))

        # --- 1. HOURLY VIEW ---
        indices["Hourly"] = add_cloud_traces("hourly", "Hourly", True)

        # --- 2. DAILY VIEW (Filled) ---
        indices["Daily"] = add_cloud_traces("D", "Daily", False)

        # --- 3. MONTHLY VIEW (Filled) ---
        indices["Monthly"] = add_cloud_traces("MS", "Monthly", False)

        # Layout
        fig.update_layout(updatemenus=[self._create_update_menu(indices, trace_idx)])
        # Force Y-axis 0-100%
        fig.update_yaxes(range=[0, 100])
        self._apply_common_layout(fig, title, y_label)
        fig.show()

    def plot_pressure(self, df: pd.DataFrame):
        """
        Plots atmospheric pressure.
        Focuses on variations (Autoscale Y).
        Modes: Hourly (Filled), Daily (Stats), Monthly (Stats).
        """
        col_name = "surface_pressure"
        if col_name not in df.columns:
            return

        title = "Surface Pressure Evolution"
        y_label = "Pressure (hPa)"

        fig = go.Figure()
        trace_idx = 0
        indices = {}

        # --- 1. HOURLY ---
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[col_name],
                mode="lines",
                name="Pressure",
                line={"color": "#8E44AD", "width": 2},  # Purple
                fill="tozeroy",  # Fill downwards
                fillcolor="rgba(142, 68, 173, 0.1)",  # Very light transparent purple
                visible=True,
                hovertemplate="<b>Date</b>: %{x|%d %b %Y %H:%M}<br><b>Press</b>: %{y:.1f} hPa<extra></extra>",
            )
        )
        indices["Hourly"] = [trace_idx]
        trace_idx += 1

        # Colors for aggregations
        agg_colors = {
            "max": {"color": "#9B59B6"},
            "mean": {"color": "#8E44AD"},
            "min": {"color": "#6C3483"},
        }

        # --- 2. DAILY (Min/Max/Mean) ---
        count = self._add_aggregated_traces(
            fig, df, col_name, "D", "Daily", agg_colors, visible=False
        )
        indices["Daily"] = list(range(trace_idx, trace_idx + count))
        trace_idx += count

        # --- 3. MONTHLY (Min/Max/Mean) ---
        count = self._add_aggregated_traces(
            fig, df, col_name, "MS", "Monthly", agg_colors, visible=False
        )
        indices["Monthly"] = list(range(trace_idx, trace_idx + count))
        trace_idx += count

        # Layout
        fig.update_layout(updatemenus=[self._create_update_menu(indices, trace_idx)])

        # Note: Do NOT set fixed range for pressure (varies slightly around 1013).
        # Let Plotly autoscale to see variations.
        self._apply_common_layout(fig, title, y_label)
        fig.show()
