import pytest
import pytest_html
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()




from pytest_html import extras

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Executa o teste
    outcome = yield
    rep = outcome.get_result()

    # Se falhou, captura screenshot
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_path = f"screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path)

            # Adiciona screenshot ao relatório HTML
            if hasattr(rep, "extra"):
                rep.extra.append(extras.image(screenshot_path))
            else:
                rep.extra = [extras.image(screenshot_path)]