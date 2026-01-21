def test_navigation_to_group(page):
    page.goto("https://brasil.bnpparibas/pt/")

    # Fecha cookies se aparecer
    try:
        page.wait_for_selector("text=Permitir tudo", timeout=5000)
        page.click("text=Permitir tudo", force=True)
    except:
        pass


    # Navega para a seção "GRUPO BNP PARIBAS"
    page.wait_for_selector("text=GRUPO BNP PARIBAS", timeout=10000)
    page.click("text=GRUPO BNP PARIBAS")
    page.wait_for_timeout(3000)

    # Agora o submenu deve estar visível
    page.wait_for_selector("text=Quem somos", timeout=10000)
    page.click("text=Quem somos", force=True)

    # Aguarda carregamento da página final
    page.wait_for_timeout(3000)
    assert "Quem somos" in page.inner_text("main")