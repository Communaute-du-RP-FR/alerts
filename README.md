# Alerts

A simple Python CLI tool to send service status notifications to Discord via webhooks.

## Features

- Send formatted status alerts to Discord channels
- Support for any service status (STARTED, STOPPED, ERROR, etc.)
- Automatic timestamp with relative time display
- @everyone mention to notify all channel members
- Clean UI layout with Discord's native components

## Installation

```bash
pip install git+https://github.com/Communaute-du-RP-FR/alerts.git
```

## Usage

Set your Discord webhook URL as an environment variable:

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

Send a status alert:

```bash
alerts my_service STARTED
alerts database_service ERROR
alerts web_server STOPPED
```

Or run as a Python module:

```bash
python -m alerts my_service STARTED
```

## Requirements

- Python >= 3.9
- discord.py
- requests

## License

MIT
