"""Unit tests for material database."""

from __future__ import annotations

import pytest

from ktirio.ub.course.simlib.materials import (
    insulation_materials,
    structural_materials,
)


class TestMaterialDatabase:
    """Test cases for material property databases."""

    def test_structural_materials_exist(self):
        """Test that structural materials are defined."""
        assert len(structural_materials) > 0

        # Check some common materials
        assert "reinforced_concrete" in structural_materials
        assert "solid_brick" in structural_materials
        assert "oak_wood" in structural_materials

    def test_insulation_materials_exist(self):
        """Test that insulation materials are defined."""
        assert len(insulation_materials) > 0

        # Check some common materials
        assert "glass_wool" in insulation_materials
        assert "rock_wool" in insulation_materials
        assert "polyurethane_PU" in insulation_materials

    def test_material_properties_complete(self):
        """Test that all materials have required properties."""
        required_keys = {"lambda", "rho", "Cp", "desc"}

        for material in structural_materials.values():
            assert required_keys.issubset(material.keys())

        for material in insulation_materials.values():
            assert required_keys.issubset(material.keys())

    def test_thermal_conductivity_ranges(self):
        """Test that thermal conductivity values are physically reasonable."""
        # Structural materials: typically 0.1 to 5 W/(m·K)
        for name, material in structural_materials.items():
            lambda_val = material["lambda"]
            assert 0.01 < lambda_val < 10, (
                f"{name} has unrealistic lambda: {lambda_val}"
            )

        # Insulation materials: typically 0.01 to 0.1 W/(m·K)
        for name, material in insulation_materials.items():
            lambda_val = material["lambda"]
            assert 0.01 < lambda_val < 0.2, (
                f"{name} has unrealistic lambda: {lambda_val}"
            )

    def test_density_ranges(self):
        """Test that density values are physically reasonable."""
        for materials_dict in [structural_materials, insulation_materials]:
            for name, material in materials_dict.items():
                rho = material["rho"]
                assert 1 < rho < 5000, f"{name} has unrealistic density: {rho}"

    def test_specific_heat_ranges(self):
        """Test that specific heat values are physically reasonable."""
        for materials_dict in [structural_materials, insulation_materials]:
            for name, material in materials_dict.items():
                cp = material["Cp"]
                assert 500 < cp < 3000, f"{name} has unrealistic Cp: {cp}"

    def test_material_descriptions(self):
        """Test that all materials have non-empty descriptions."""
        for materials_dict in [structural_materials, insulation_materials]:
            for name, material in materials_dict.items():
                desc = material["desc"]
                assert isinstance(desc, str)
                assert len(desc) > 0, f"{name} has empty description"

    @pytest.mark.parametrize(
        "material_name",
        [
            "reinforced_concrete",
            "glass_wool",
            "oak_wood",
        ],
    )
    def test_specific_materials(self, material_name):
        """Test specific material properties."""
        if material_name in structural_materials:
            material = structural_materials[material_name]
        else:
            material = insulation_materials[material_name]

        assert material["lambda"] > 0
        assert material["rho"] > 0
        assert material["Cp"] > 0
