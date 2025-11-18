import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from typing import Dict, Union, Optional

class BasePlotFactory:
    """
    Base class for all plotting factories.
    Holds shared configurations (unit conversions) and layout styles.
    """

    # Configuration for data types, units, and conversions
    DATA_CONFIG = {
        "temperature": {
            "y_label": "Temperature (°C)",
            "conversion": lambda K: K - 273.15,  # Kelvin -> Celsius
        },
        "heat_flux": {
            "y_label": "Heat Flux (W/m²)",
            "conversion": lambda x: x,          # Identity
        },
        "solar_radiation": {
            "y_label": "Irradiance (W/m²)",
            "conversion": lambda x: x,
        },
        "energy": {
            "y_label": "Energy (kWh)",
            "conversion": lambda J: J / 3.6e6,  # Joules -> kWh
        }
    }

    def _convert_data(self, data_type: str, data_dict: Dict[str, np.ndarray]):
        """
        Helper: Applies conversion logic based on data_type.
        Returns converted data and the appropriate Y-axis label.
        """
        config = self.DATA_CONFIG.get(data_type.lower())

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
            legend=dict(x=0, y=-0.2, orientation="h"),
            hovermode="x unified",
            template="plotly_white"
        )
        return fig