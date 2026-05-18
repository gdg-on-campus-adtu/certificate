### 1. How to work with this notebook?

This notebook can be scaffolded using [Nix](https://nixos.org) and
[direnv](https://direnv.net). To scaffold, run:

```fish
direnv allow
```

Now, follow the generic instructions (last updated w.r.t to a distribution on
18th May, 2026):

```fish
# Setup env variables:
cp .env.example .env
# Now, change it with your own credentials

# Setup assets:
mkdir assets
# Now, save the record as "assets/record.xlsx"
# Save the certificate template as "assets/certificate.png"
# Save the font you want to use for the name as "assets/font.ttf"

# Now, run the marimo notebook and perform the needed:
uv run poe notebook
```

### 2. Licensing

This repository is made available in the public domain under
[CC0 1.0 Universal](/LICENSE).
