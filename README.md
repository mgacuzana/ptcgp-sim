# Pokemon TCG Pocket Pack Opening Simulator

## Prerequisites

- Clone/download/fork the `ptcgp-sim` repository
- [Install Python](https://wiki.python.org/moin/BeginnersGuide/Download)

Run the following commands from your local `ptcgp-sim` directory:

```bash
pip install -r requirements.txt
```

This will install the python packages that the simulator requires.

## Running the simulator

Run the following command from your local `ptcgp-sim` directory:

```bash
python3 ./main.py
```

Optional args:

- `--express-mode` or `-e`: open packs instantaneously by removing waits and "continue" prompts
  - Example: `python3 ./main.py --express-mode` or `python3 ./main.py -e`
