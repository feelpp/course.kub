# KUB Course - Building Energy Simulation

[![CI](https://github.com/feelpp/course.kub/workflows/CI/badge.svg)](https://github.com/feelpp/course.kub/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Educational Python library for building energy simulation using FMU (Functional Mock-up Units). Designed for training courses on thermal building physics and energy performance analysis.

## Features

- 🏗️ **FMU Simulation**: High-level wrapper for FMPy to run building energy simulations
- 📊 **Visualization**: Interactive Plotly-based plotting for temperature, heat flux, and energy analysis
- 📚 **Material Database**: Comprehensive thermal properties of construction and insulation materials
- 📓 **Training Notebooks**: Hands-on exercises covering:
  - Heat conduction and thermal resistance
  - Infrared and solar radiation
  - Building loss assessment
  - Weather data analysis
  - Case studies with optimization

## Quick Start

### Installation

#### Option 1: Using Dev Container (Recommended)

Open this repository in VS Code and click "Reopen in Container". Everything will be set up automatically.

#### Option 2: Using UV (Fast)

```bash
uv venv --system-site-packages
source .venv/bin/activate
uv pip install -e '.[dev,test]'
```

#### Option 3: Using pip

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e '.[dev,test]'
```

### Basic Usage

```python
from ktirio.ub.course.simlib import FMUSimulation
from ktirio.ub.course.plotlib import SimulationPlotFactory
from pathlib import Path

# Load and run an FMU simulation
fmu_path = Path("database/day1/FMUs/Exercises_Conduction_SteStaWalResCon_01.fmu")
sim = FMUSimulation(fmu_path)

# Configure simulation
sim.initialize(startTime=0.0, stopTime=3600.0, timeStep=1.0)
sim.initParameters({"Wall_Resistor.R": 1.5, "Wall_Conductor.G": 0.75})
sim.exitInitialization()

# Run and collect results
data = sim.run(["Wall_Resistor.port_b.T", "Wall_Conductor.port_b.Q_flow"])
sim.terminate()

# Visualize results
factory = SimulationPlotFactory()
factory.plot_subplots(
    time=data["time"],
    data_type="temperature",
    data_dict={"Temperature": data["Wall_Resistor.port_b.T"]},
    title="Wall Temperature Over Time"
)
```

### Material Database

```python
from ktirio.ub.course.simlib.materials import insulation_materials, structural_materials

# Access thermal properties
glass_wool = insulation_materials["glass_wool"]
print(f"Lambda: {glass_wool['lambda']} W/(m·K)")
print(f"Density: {glass_wool['rho']} kg/m³")
print(f"Specific heat: {glass_wool['Cp']} J/(kg·K)")
```

## Project Structure

```
course.kub/
├── .devcontainer/               # Development container configuration
├── .github/workflows/           # CI/CD pipelines
├── .vscode/                     # VS Code settings
├── database/                    # FMU files and data
│   ├── day1/                   # Day 1 exercises (conduction, radiation)
│   └── day2/                   # Day 2 exercises (optimization, weather)
├── notebooks/                   # Jupyter training notebooks
│   ├── trainingDay1/           # Basic physics exercises
│   └── trainingDay2/           # Advanced case studies
├── src/python/ktirio/ub/course/ # Main package
│   ├── plotlib/                # Visualization utilities
│   └── simlib/                 # Simulation and materials
└── tests/                       # Unit tests
```

## Development

### Running Tests

```bash
pytest                                           # Run all tests
pytest --cov=ktirio.ub.course --cov-report=html # With coverage report
```

### Code Quality

```bash
ruff check .                             # Lint code
ruff format .                            # Format code
ruff check --fix .                       # Auto-fix issues
```

### Building the Package

```bash
python -m build
pip install dist/*.whl
```

### Creating a Release

This project uses semantic versioning and automated releases via GitHub Actions.

**For stable releases:**

```bash
# Update version in pyproject.toml to match the release version
# Commit your changes
git add pyproject.toml
git commit -m "Bump version to 1.0.0"
git push origin main

# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

**For prereleases (alpha, beta, rc):**

```bash
# Use semver prerelease format
git tag v1.0.0-beta.1
git push origin v1.0.0-beta.1

# Or tag from a feature branch (automatically marked as prerelease)
git checkout develop
git tag v1.1.0-rc.1
git push origin v1.1.0-rc.1
```

The CI workflow will automatically:
- Run all tests and quality checks
- Build the package (wheel and sdist)
- Create a GitHub release with distribution files
- Mark as prerelease if the version contains `.alpha.`, `.beta.`, `.rc.`, or if tagged from a non-main branch
- Generate release notes from commits and PRs

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- **Philippe Pinçon** - philippe.pincon@cemosis.fr
- **Gwennolé Chappron** - gwennole.chappron@cemosis.fr
- **Christophe Prud'homme** - christophe.prudhomme@cemosis.fr

## Acknowledgments

- Part of the Ktirio Urban Building (KUB) project
- Uses [FMPy](https://github.com/CATIA-Systems/FMPy) for FMU simulation
- Built with [Plotly](https://plotly.com/python/) for interactive visualization
