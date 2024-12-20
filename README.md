# Pokemon TCG Pocket Pack Opening Simulator

## User Guide

TBD -- need to create a release executable first

## Development Guide

### Prerequisites

- Clone/download/fork the `ptcgp-sim` repository
- [Install Python](https://wiki.python.org/moin/BeginnersGuide/Download)

Run the following commands from your local `ptcgp-sim` directory:

```bash
pip install -r requirements.txt
```

This will install the python packages that the simulator requires.

### Running the simulator

Run the following command from your local `ptcgp-sim` directory:

```bash
python3 ./main.py
```

Optional args:

- `--express-mode` or `-e`: open packs instantaneously by removing waits and "continue" prompts
  - Example: `python3 ./main.py --express-mode` or `python3 ./main.py -e`

If saving results to files during development, the generated JSON is stored at `./collections/<filename>.json`.
