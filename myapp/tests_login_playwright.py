import asyncio

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from playwright.async_api import async_playwright


class LoginFormTest(LiveServerTestCase):
    """Login flows with Playwright async API + Django live server."""

    def setUp(self):
        super().setUp()
        # LiveServerTestCase uses TransactionTestCase: DB is reset between tests,
        # so class-level setUpTestData would leave later tests without this user.
        User.objects.filter(username='testuser').delete()
        User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
        )

    def test_successful_login(self):
        async def run():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                try:
                    await page.goto(f'{self.live_server_url}/accounts/login/')
                    await page.fill('#id_username', 'testuser')
                    await page.fill('#id_password', 'testpass123')
                    await page.click('[data-testid="submit-login"]')
                    await page.wait_for_url(
                        f'{self.live_server_url}/demo/dashboard/',
                    )
                    heading = await page.locator('h1').text_content()
                    self.assertIn('Dashboard', heading or '')
                    body = await page.content()
                    self.assertIn('testuser', body)
                finally:
                    await context.close()
                    await browser.close()

        asyncio.run(run())

    def test_failed_login(self):
        async def run():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                try:
                    await page.goto(f'{self.live_server_url}/accounts/login/')
                    await page.fill('#id_username', 'wronguser')
                    await page.fill('#id_password', 'wrongpass')
                    await page.click('[data-testid="submit-login"]')
                    await page.wait_for_selector('[data-testid="login-error"]')
                    error_text = await page.locator(
                        '[data-testid="login-error"]',
                    ).text_content()
                    self.assertIsNotNone(error_text)
                    self.assertIn(
                        'username',
                        error_text.lower(),
                    )
                finally:
                    await context.close()
                    await browser.close()

        asyncio.run(run())
