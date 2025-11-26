"""
Database of thermal properties of materials.

Standard units used:
- lambda (thermal conductivity): W/(m·K)
- rho (density): kg/m³
- Cp (specific heat): J/(kg·K)
"""

# structural materials
from __future__ import annotations

structural_materials = {
    "reinforced_concrete": {
        "lambda": 2.3,
        "rho": 2400.0,
        "Cp": 1000.0,
        "desc": "Standard reinforced concrete. Highly conductive but high thermal inertia.",
    },
    "aerated_concrete": {
        "lambda": 0.15,
        "rho": 500.0,
        "Cp": 1000.0,
        "desc": "Cellular material (AAC/Siporex). A compromise between structure and insulation.",
    },
    "solid_brick": {
        "lambda": 0.8,
        "rho": 1900.0,
        "Cp": 850.0,
        "desc": "Traditional solid red brick. High thermal inertia.",
    },
    "hollow_brick": {
        "lambda": 0.35,
        "rho": 1000.0,
        "Cp": 900.0,
        "desc": "Standard honeycomb/perforated brick. Lighter than solid brick.",
    },
    "hollow_concrete_block": {
        "lambda": 1.1,
        "rho": 1300.0,
        "Cp": 1000.0,
        "desc": "Classic cinder block (CMU). Poor insulation.",
    },
    "granite_stone": {
        "lambda": 3.0,
        "rho": 2600.0,
        "Cp": 800.0,
        "desc": "Hard stone, feels cold to the touch. Huge inertia.",
    },
    "limestone": {
        "lambda": 1.4,
        "rho": 2200.0,
        "Cp": 850.0,
        "desc": "Soft stone (tuffeau/limestone). Slightly less cold than granite.",
    },
    "rammed_earth": {
        "lambda": 0.85,
        "rho": 1900.0,
        "Cp": 1100.0,
        "desc": "Compacted earth. Ecological with excellent inertia.",
    },
    "oak_wood": {
        "lambda": 0.17,
        "rho": 750.0,
        "Cp": 1600.0,
        "desc": "Hardwood, structural use.",
    },
    "pine_wood": {
        "lambda": 0.13,
        "rho": 450.0,
        "Cp": 1600.0,
        "desc": "Light softwood. Typical for timber frame structures.",
    },
}

# insulation materials

insulation_materials = {
    "glass_wool": {
        "lambda": 0.035,
        "rho": 15.0,
        "Cp": 850.0,
        "desc": "Standard mineral/fiberglass wool. Very light, poor for thermal time lag.",
    },
    "rock_wool": {
        "lambda": 0.038,
        "rho": 40.0,
        "Cp": 850.0,
        "desc": "Similar to glass wool but denser and fire resistant.",
    },
    "expanded_polystyrene_EPS": {
        "lambda": 0.038,
        "rho": 20.0,
        "Cp": 1450.0,
        "desc": "Standard white foam. Insensitive to moisture.",
    },
    "extruded_polystyrene_XPS": {
        "lambda": 0.032,
        "rho": 35.0,
        "Cp": 1450.0,
        "desc": "Dense blue/orange foam. Higher performance.",
    },
    "polyurethane_PU": {
        "lambda": 0.024,
        "rho": 32.0,
        "Cp": 1400.0,
        "desc": "PIR/PUR panel. Max insulation for minimal thickness.",
    },
    "dense_wood_fiber": {
        "lambda": 0.042,
        "rho": 160.0,
        "Cp": 2100.0,
        "desc": "Rigid bio-based insulation. Excellent thermal time lag (phase shift).",
    },
    "cellulose_wadding": {
        "lambda": 0.040,
        "rho": 55.0,
        "Cp": 1900.0,
        "desc": "Recycled paper. Good compromise between performance/inertia/ecology.",
    },
    "expanded_cork": {
        "lambda": 0.040,
        "rho": 110.0,
        "Cp": 1600.0,
        "desc": "Rot-proof, natural, good acoustic properties.",
    },
    "straw_bale": {
        "lambda": 0.065,
        "rho": 90.0,
        "Cp": 1700.0,
        "desc": "Agricultural. Requires large thicknesses (35cm+).",
    },
    "aerogel": {
        "lambda": 0.015,
        "rho": 150.0,
        "Cp": 1000.0,
        "desc": "Ultra-high performance material (and ultra-expensive). Nanotechnology.",
    },
}
