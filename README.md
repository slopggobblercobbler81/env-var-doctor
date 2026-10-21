# env-var-doctor

[![CI](https://github.com/slopggobblercobbler81/env-var-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/slopggobblercobbler81/env-var-doctor/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Validate, analyze, and check your `.env` files against `.env.example` templates with ease.

## Installation

```bash
pip install .
```

## Usage

```bash
env-var-doctor --check --env .env --example .env.example
```

### CLI Flags

- `--env`: Path to the `.env` file (default: `.env`)
- `--example`: Path to the `.env.example` file (default: `.env.example`)
- `--strict`: Treat extra environment variables as errors
- `--check`: Exit with a non-zero status code if any errors or missing variables are found


Documentation update for release.
