# kub-course

### User installation

Create the Python virtual environment and install the local library to do the exercises.

```bash
uv venv --system-site-packages
source .venv/bin/activate
uv pip install -r pyproject.toml --extra dev --extra test
pipx run build
uv pip install dist/*.whl
```