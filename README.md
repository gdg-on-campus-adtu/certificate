### 1. How to work with this notebook?

This notebook can be scaffolded using [Nix](https://nixos.org) and
[direnv](https://direnv.net). To scaffold, run:

```fish
direnv allow
```

Now, follow the generic instructions:

```fish
# Install dependencies into the active venv.
uv sync --active

# Setup env variables.
cp .env.example .env
# Now, change it with your own credentials.

# Setup assets
mkdir assets
# Now, download the CSV from Bevy and save it as "assets/attendance.csv".
# Put your certificate template in assets as "assets/certificate.png".
# Lastly, the font you want to use for the name should be available as "assets/font.otf".

# Now, run the marimo notebook and perform the needed:
marimo edit src/notebook.py
```

### 2. Licensing

This repository is made available in the public domain under
[CC0 1.0 Universal](/LICENSE).
