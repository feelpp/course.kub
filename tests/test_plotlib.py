"""Unit tests for plotting factories."""
from __future__ import annotations

import pytest
import numpy as np
from kub.course.plotlib import SimulationPlotFactory


class TestSimulationPlotFactory:
    """Test cases for SimulationPlotFactory."""

    @pytest.fixture
    def factory(self):
        """Provide a plot factory instance."""
        return SimulationPlotFactory()

    @pytest.fixture
    def sample_data(self):
        """Provide sample time series data."""
        time = np.linspace(0, 3600, 100)
        temperature = 273.15 + 20 + 5 * np.sin(time / 600)
        heat_flux = 100 * np.cos(time / 600)

        return {
            "time": time,
            "temperature": temperature,
            "heat_flux": heat_flux,
        }

    def test_factory_initialization(self, factory):
        """Test factory can be instantiated."""
        assert factory is not None
        assert hasattr(factory, "DATA_CONFIG")

    def test_data_config_exists(self, factory):
        """Test that data configuration is defined."""
        assert "temperature" in factory.DATA_CONFIG
        assert "heat_flux" in factory.DATA_CONFIG
        assert "solar_radiation" in factory.DATA_CONFIG

    def test_temperature_conversion(self, factory):
        """Test temperature conversion from Kelvin to Celsius."""
        config = factory.DATA_CONFIG["temperature"]

        # Test conversion function
        kelvin_temp = 273.15
        celsius_temp = config["conversion"](kelvin_temp)
        assert abs(celsius_temp - 0.0) < 0.01

    def test_convert_data_method(self, factory, sample_data):
        """Test data conversion helper method."""
        data_dict = {"Temperature": sample_data["temperature"]}

        converted, y_label = factory._convert_data("temperature", data_dict)

        assert "Temperature" in converted
        assert y_label == "Temperature (°C)"
        # Check temperature was converted from Kelvin
        assert np.max(converted["Temperature"]) < 30  # Should be in Celsius range

    def test_plot_creation(self, factory, sample_data):
        """Test that plot can be created without errors."""
        # Create plot without showing it (show=False for testing)
        fig = factory.plot_subplots(
            time=sample_data["time"],
            data_type="temperature",
            data_dict={"Temperature": sample_data["temperature"]},
            title="Test Plot",
            show=False,  # Don't display in headless test environment
        )
        assert fig is not None
        assert hasattr(fig, 'data')
        assert len(fig.data) > 0

    @pytest.mark.parametrize("data_type,expected_label", [
        ("temperature", "Temperature (°C)"),
        ("heat_flux", "Heat Flux (W)"),
        ("solar_radiation", "Irradiance (W/m²)"),
    ])
    def test_data_type_labels(self, factory, data_type, expected_label):
        """Test that different data types have correct labels."""
        config = factory.DATA_CONFIG.get(data_type)
        assert config is not None
        assert config["y_label"] == expected_label
