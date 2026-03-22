import os

# Playwright's sync API uses asyncio internally; Django blocks sync ORM calls
# from async contexts unless this is set (safe for tests only).
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')

import pytest
from django.contrib.auth.models import User
from playwright.sync_api import Browser, Page, Playwright, sync_playwright


@pytest.fixture(scope='session')
def playwright() -> Playwright:
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope='session')
def browser(playwright: Playwright) -> Browser:
    b = playwright.chromium.launch()
    yield b
    b.close()


@pytest.fixture
def page(browser: Browser) -> Page:
    context = browser.new_context()
    p = context.new_page()
    yield p
    context.close()


@pytest.fixture
def demo_user(db):
    return User.objects.create_user(
        username='playwright',
        email='pw@example.com',
        password='test-pass-123',
    )
