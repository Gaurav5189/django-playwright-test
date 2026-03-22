# Django + Playwright Integration Playground

This repository is my personal testing ground for understanding how Playwright interacts with Django's live server and database transactions. I built this to prepare for the Django GSoC 2026 project: "Switch to Playwright tests for integration testing."

## What's inside

I wanted to explore both the synchronous and asynchronous Playwright APIs alongside Django.
- `myapp/tests_login_playwright.py`: Uses `async_playwright` with Django's `LiveServerTestCase` to test authentication flows.
- `tests/test_playwright_demo.py`: Uses the sync API with `pytest-django` (`@pytest.mark.django_db`) to test database-backed list and create views.
- I also experimented with the Playwright `codegen` tool to see how easily it can generate tests for Django templates.

## Next Steps
Now that I have a solid grasp of the API boundaries, my next step is moving over to my `django/django` fork (mine named: `Gaurav5189/gsoc-playwright-django-tests-PoC`) to start building a native `PlaywrightLiveServerTestCase` class for the core framework.