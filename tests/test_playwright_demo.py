import re

import pytest
from playwright.sync_api import Page, expect

from myapp.models import DemoItem


@pytest.mark.django_db
def test_home_loads(page: Page, live_server):
    page.goto(live_server.url)
    expect(page.get_by_test_id('page-title')).to_have_text(
        'Playwright + Django demo'
    )


@pytest.mark.django_db
def test_add_item_flow(page: Page, live_server):
    page.goto(f'{live_server.url}/demo/items/add/')
    page.get_by_test_id('item-title').fill('E2E item')
    page.get_by_test_id('item-notes').fill('Created by Playwright')
    page.get_by_test_id('submit-item').click()
    expect(page).to_have_url(re.compile(r'.*/demo/items/$'))
    expect(page.get_by_test_id('flash-message')).to_contain_text('saved')
    expect(page.get_by_test_id('item-title-text')).to_have_text('E2E item')


@pytest.mark.django_db
def test_contact_form_flash(page: Page, live_server):
    page.goto(f'{live_server.url}/demo/contact/')
    page.get_by_test_id('contact-name').fill('Alex')
    page.get_by_test_id('contact-email').fill('alex@example.com')
    page.get_by_test_id('contact-message').fill('Hello from tests')
    page.get_by_test_id('submit-contact').click()
    expect(page.get_by_test_id('flash-message')).to_contain_text('Thanks, Alex')


@pytest.mark.django_db
def test_dashboard_requires_login(page: Page, live_server):
    page.goto(f'{live_server.url}/demo/dashboard/')
    expect(page).to_have_url(re.compile(r'.*/accounts/login/.*'))


@pytest.mark.django_db
def test_login_and_dashboard(page: Page, live_server, demo_user):
    page.goto(f'{live_server.url}/accounts/login/')
    page.get_by_test_id('login-username').fill('playwright')
    page.get_by_test_id('login-password').fill('test-pass-123')
    page.get_by_test_id('submit-login').click()
    expect(page).to_have_url(re.compile(r'.*/demo/dashboard/.*'))
    expect(page.get_by_test_id('welcome-text')).to_contain_text('playwright')


@pytest.mark.django_db
def test_item_list_shows_seed_data(page: Page, live_server):
    DemoItem.objects.create(title='Seed', notes='from factory')
    page.goto(f'{live_server.url}/demo/items/')
    expect(page.get_by_test_id('item-title-text')).to_have_text('Seed')
