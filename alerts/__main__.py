"""
Discord Service Status Alert Module
====================================

This module provides functionality to send service status alerts to Discord
using webhooks with formatted UI layouts.

The module can be executed as a command-line script to notify Discord channels
about service status changes (e.g., STARTED, STOPPED, ERROR).

Example:
    $ python -m alerts my_service STARTED
    $ python -m alerts database_service ERROR

Environment Variables:
    DISCORD_WEBHOOK_URL: Discord webhook URL for sending notifications (required)
"""

import asyncio
import argparse
import discord
import os
import time
from typing import List

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
"""str: Discord webhook URL retrieved from environment variable."""

LayoutItem = discord.ui.Item[discord.ui.LayoutView]
"""Type alias for Discord UI layout items."""

LayoutContainer = discord.ui.Container[discord.ui.LayoutView]
"""Type alias for Discord UI layout containers."""


def build_container(service_name: str, new_status: str) -> LayoutContainer:
    """
    Build a Discord UI container with formatted status notification.

    Creates a visual layout container containing service status information,
    including the service name, new status, and timestamp of the alert.

    :param service_name: Name of the service reporting the status
    :type service_name: str
    :param new_status: Current status of the service (e.g., STARTED, STOPPED, ERROR)
    :type new_status: str
    :return: Container with formatted notification UI elements
    :rtype: LayoutContainer
    """
    items: List[LayoutItem] = []
    items.append(discord.ui.TextDisplay(content="## Status Notification"))
    items.append(
        discord.ui.Separator(visible=True, spacing=discord.SeparatorSpacing.large)
    )
    items.append(discord.ui.TextDisplay(content=f"Service: `{service_name}`"))
    items.append(discord.ui.TextDisplay(content=f"New status: `{new_status}`"))
    items.append(
        discord.ui.Separator(visible=True, spacing=discord.SeparatorSpacing.small)
    )
    items.append(
        discord.ui.TextDisplay(content=f"Alert triggered at <t:{int(time.time())}:R>")
    )

    return discord.ui.Container(
        *items,
        accent_colour=discord.Colour.darker_grey(),
        spoiler=False,
    )


async def send_webhook(service_name: str, status: str):
    """
    Send a status alert to Discord via webhook.

    Constructs and sends a formatted status notification to the configured
    Discord webhook URL. Also sends an @everyone mention to alert all members.

    :param service_name: Name of the service reporting the status
    :type service_name: str
    :param status: Current status of the service
    :type status: str
    :raises ValueError: If DISCORD_WEBHOOK_URL environment variable is not set
    """
    if WEBHOOK_URL is None:
        raise ValueError("DISCORD_WEBHOOK_URL environment variable is not set.")
    webhook = discord.SyncWebhook.from_url(WEBHOOK_URL)
    layout_view = discord.ui.LayoutView(timeout=None)
    layout_view.add_item(build_container(service_name, status))
    webhook.send(view=layout_view)
    webhook.send("@everyone")


def main():
    """
    Main entry point for the alerts CLI application.

    Parses command-line arguments and sends a service status alert to Discord.
    Expects two positional arguments: service name and status.
    """
    parser = argparse.ArgumentParser(
        description="Send a service status alert to Discord"
    )
    parser.add_argument("service", type=str, help="Name of the service")
    parser.add_argument(
        "status",
        type=str,
        help="New status of the service (e.g., STARTED, STOPPED, ERROR)",
    )

    args = parser.parse_args()
    asyncio.run(send_webhook(args.service, args.status))
