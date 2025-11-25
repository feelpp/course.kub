"""Unit tests for FMU simulation wrapper."""
from __future__ import annotations

import pytest
from pathlib import Path
from kub.course.simlib import FMUSimulation, FMUState


class TestFMUSimulation:
    """Test cases for FMUSimulation class."""

    @pytest.fixture
    def fmu_path(self):
        """Provide path to test FMU."""
        # This should point to an actual FMU file in tests
        return Path("database/day1/FMUs/Exercises_Conduction_SteStaWalResCon_01.fmu")

    def test_initialization(self, fmu_path):
        """Test FMU initialization."""
        if not fmu_path.exists():
            pytest.skip("FMU file not found")

        sim = FMUSimulation(str(fmu_path))
        assert sim.state == FMUState.INSTANTIATED
        assert sim.fmu is not None
        assert sim.model_description is not None

    def test_state_transitions(self, fmu_path):
        """Test FMU state machine transitions."""
        if not fmu_path.exists():
            pytest.skip("FMU file not found")

        sim = FMUSimulation(str(fmu_path))

        # Initial state
        assert sim.state == FMUState.INSTANTIATED

        # Initialize
        sim.initialize()
        assert sim.state == FMUState.INITIALIZATION_MODE

        # Exit initialization
        sim.exitInitialization()
        assert sim.state == FMUState.INITIALIZED

        # Terminate
        sim.terminate()
        assert sim.state == FMUState.TERMINATED

    def test_invalid_state_transition(self, fmu_path):
        """Test that invalid state transitions raise errors."""
        if not fmu_path.exists():
            pytest.skip("FMU file not found")

        sim = FMUSimulation(str(fmu_path))

        # Try to exit initialization without entering it
        with pytest.raises(RuntimeError):
            sim.exitInitialization()

    def test_parameter_setting(self, fmu_path):
        """Test setting FMU parameters."""
        if not fmu_path.exists():
            pytest.skip("FMU file not found")

        sim = FMUSimulation(str(fmu_path))
        sim.initialize()

        # Set parameters during initialization
        params = {"Wall_Resistor.R": 1.5, "Wall_Conductor.G": 0.75}
        sim.initParameters(params)

        sim.exitInitialization()
        sim.terminate()

    def test_simulation_run(self, fmu_path):
        """Test running a complete simulation."""
        if not fmu_path.exists():
            pytest.skip("FMU file not found")

        sim = FMUSimulation(str(fmu_path))
        sim.initialize(startTime=0.0, stopTime=100.0, timeStep=1.0)
        sim.initParameters({"Wall_Resistor.R": 1.5, "Wall_Conductor.G": 0.75})
        sim.exitInitialization()

        outputs = ["Wall_Resistor.port_b.T", "Wall_Conductor.port_b.Q_flow"]
        data = sim.run(outputs)

        # Check returned data structure
        assert "time" in data
        assert all(output in data for output in outputs)
        assert len(data["time"]) > 0

        sim.terminate()
