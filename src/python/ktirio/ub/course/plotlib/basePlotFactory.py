from __future__ import annotations

from typing import ClassVar

import numpy as np


class BasePlotFactory:
    """
    Base class for all plotting factories.
    Holds shared configurations (unit conversions) and layout styles.
    """

    # Configuration for data types, units, and conversions
    DATA_CONFIG: ClassVar[dict] = {
        "temperature": {
            "y_label": "Temperature (°C)",
            "conversion": lambda K: K - 273.15,  # Kelvin -> Celsius
        },
        "surface_heat_flux": {
            "y_label": "Heat Flux (W/m²)",
            "conversion": lambda x: x,
        },
        "heat_flux": {
            "y_label": "Heat Flux (W)",
            "conversion": lambda x: x,
        },
        "solar_radiation": {
            "y_label": "Irradiance (W/m²)",
            "conversion": lambda x: x,
        },
        "energy": {
            "y_label": "Energy (kWh)",
            "conversion": lambda x: x,
        },
        "relative_humidity": {
            "y_label": "Relative Humidity (%)",
            "conversion": lambda x: x,
        },
    }

    def _convert_data(self, data_type: str, data_dict: dict[str, np.ndarray | list]):
        """
        Helper: Applies conversion logic based on data_type.
        Returns converted data and the appropriate Y-axis label.
        """
        config = self.DATA_CONFIG.get(data_type.lower())

        # Ensure all data are numpy arrays
        converted_data = {
            label: np.array(data) if not isinstance(data, np.ndarray) else data
            for label, data in data_dict.items()
        }

        if config and "conversion" in config:
            converter = config["conversion"]
            converted_data = {
                label: converter(array) for label, array in data_dict.items()
            }
            return converted_data, config["y_label"]

        # Fallback
        return data_dict, "Value"

    def _apply_common_layout(self, fig, title, y_label, x_label="Time"):
        """
        Helper: Applies a consistent style to all figures.
        """
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            legend={"x": 0, "y": -0.2, "orientation": "h"},
            hovermode="x unified",
            template="plotly_white",
            plot_bgcolor="white",
        )

        # Grid (Y-axis)
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor="#A9A9A9",
            zeroline=True,
            zerolinecolor="#7E7E7E",
            zerolinewidth=1,
        )

        # Grid (X-axis)
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#A9A9A9")

        return fig
