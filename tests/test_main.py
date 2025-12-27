import os
import sys
from unittest import mock

import pytest

import alerts.__main__ as main


def test_build_container_structure() -> None:
    service = "test_service"
    status = "STARTED"
    container = main.build_container(service, status)
    assert hasattr(container, "children")
    texts = [item.content for item in container.children if hasattr(item, "content")]
    assert any("Status Notification" in t for t in texts)
    assert any(service in t for t in texts)
    assert any(status in t for t in texts)


@pytest.mark.asyncio  # type: ignore
@mock.patch("alerts.__main__.discord.SyncWebhook")
async def test_send_webhook_success(mock_webhook: mock.Mock) -> None:
    os.environ["DISCORD_WEBHOOK_URL"] = "https://discord.com/api/webhooks/test"
    main.WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
    with mock.patch("alerts.__main__.build_container") as mock_build:
        mock_build.return_value = mock.Mock()
        with mock.patch("alerts.__main__.discord.ui.LayoutView") as mock_layout:
            mock_layout.return_value = mock.Mock(add_item=mock.Mock())
            await main.send_webhook("service", "STARTED")
            assert mock_webhook.from_url.called
            assert mock_layout.return_value.add_item.called


@pytest.mark.asyncio  # type: ignore
@mock.patch("alerts.__main__.discord.SyncWebhook")
async def test_send_webhook_no_url(mock_webhook: mock.Mock) -> None:
    if "DISCORD_WEBHOOK_URL" in os.environ:
        del os.environ["DISCORD_WEBHOOK_URL"]
    main.WEBHOOK_URL = None
    with pytest.raises(ValueError):
        await main.send_webhook("service", "STARTED")


def test_main_parsing(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {}

    async def fake_run(service: str, status: str) -> None:
        called["service"] = service
        called["status"] = status

    monkeypatch.setattr(main, "send_webhook", fake_run)
    monkeypatch.setattr(sys, "argv", ["alerts", "svc", "STOPPED"])
    main.main()
    assert called["service"] == "svc"
    assert called["status"] == "STOPPED"
