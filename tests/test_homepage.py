def test_homepage_title(page):
    page.goto("https://brasil.bnpparibas/pt/")
    assert "BNP Paribas" in page.title()