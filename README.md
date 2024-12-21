# Pokemon TCG Pocket Pack Opening Simulator

## User Guide

TBD -- need to create a release executable first

## Development Guide

### Prerequisites

- Clone/download/fork the `ptcgp-sim` repository
- [Install Python](https://wiki.python.org/moin/BeginnersGuide/Download)

From your local `ptcgp-sim` directory:

- Create and activate a Python virtual environment (venv). If you are using PowerShell:

```bash
python3 -m venv ptcgp-sim
./ptcgp-sim/Scripts/activate
```

Your prompt will show `(ptcgp-sim)` at the start if your venv is active.

- Install Python package requirements:

```bash
python3 -m pip install -r requirements.txt
```

**Note**: To deactivate your `ptcgp-sim` venv, type `deactivate` and you will return to your user Python environment.

### Running the simulator

Run the following command from your local `ptcgp-sim` directory:

```bash
python3 ./main.py
```

Optional args:

- `--batch-mode` or `-b`: open packs instantaneously by removing waits and "continue" prompts
  - Example: `python3 ./main.py --batch-mode` or `python3 ./main.py -b`
- `--use-collection <filename>` or `-I <filename>`: load and add to an existing collection rather than starting from an empty collection

If saving results to files during development, the generated JSON is stored at `./collections/<filename>.json`.

### Running tests

This project uses pytest for its unit tests. Refer to the [pytest docs](https://docs.pytest.org/en/stable/getting-started.html) for help authoring unit tests.

If you need to mock a dependency for a test, please use `unittest.mock` rather than `monkeypatch` for project consistency.

Run the following command from your local `ptcgp-sim` directory:

```bash
python3 -m pytest
```

To run a tests from a specific file:

```bash
python3 -m pytest ./tests/modules/test_pack.py
```

### Creating a release executable

This project uses PyInstaller to create new releases. [Read more about PyInstaller here.](https://pyinstaller.org/en/stable/usage.html)

TL;DR: if you want to create a `.exe`, run the following from within `ptcgp-sim`:

```bash
python3 -m PyInstaller ./main.py --name ptcgp-sim
```

This will create a local `./dist` directory that stores your release directory.
