## Overview

This project will mirror the organization structure of the current Akamai configuration in the [Akamai Control Panel](https://control.akamai.com) to a local folder structure.

This enables walking into the folder structure to back up individual hostname configurations in Akamai with infrastructure as code (IaC) using code with Terraform by importing it via [the Akamai CLI](https://github.com/akamai/cli-terraform).

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [Akamai API access credentials](doc/access.md)

## Setting Up Credentials

This tool must have the following environment variables.

You can put these credentials into `.env.sh` and run `source .env.sh`.

```bash
AKAMAI_PAPI_HOST=akaa-XXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXX.luna.akamaiapis.net \
AKAMAI_PAPI_ACCESS_TOKEN=akaa-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx \
AKAMAI_PAPI_CLIENT_TOKEN=akaa-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx \
AKAMAI_PAPI_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaa12345xyz= \
```

## Running the code

- Setup your environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py -h
```

- Upgrading old dependencies

```bash
pip install --upgrade --force-reinstall -r requirements.txt
```

- Freezing dependencies

```bash
pip freeze > requirements.txt
```
