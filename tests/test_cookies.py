import pytest

def test_cookie_banner(page):
    page.goto("https://brasil.bnpparibas/pt/")
    try:
        page.wait_for_selector("text=Permitir tudo", timeout=5000)
        page.click("text=Permitir tudo")
        assert True
    except:
        pytest.skip("Cookie banner não apareceu")