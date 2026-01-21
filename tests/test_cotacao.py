import re
import logging

logger = logging.getLogger(__name__)

def test_cotacao(page):
    page.goto("https://brasil.bnpparibas/pt/")

    # Fecha cookies se aparecer
    try:
        page.wait_for_selector("text=Permitir tudo", timeout=5000)
        page.click("text=Permitir tudo", force=True)
    except:
        pass

    # Rola até o final da página
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(3000)

    # Captura cotação completa
    try:
        cotacao = page.locator("text=COTAÇÃO").locator("xpath=..").inner_text()
        print("📊 Cotação encontrada:\n", cotacao)

        # Extrai valor em €
        valor_match = re.search(r"\d+,\d+€|\d+\.\d+€", cotacao)
        valor = valor_match.group(0) if valor_match else None

        # Extrai data/hora
        data_match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \(PARIS TIME\)", cotacao)
        data = data_match.group(0) if data_match else None

        print(f"💶 Valor: {valor}")
        print(f"🕒 Data/Hora: {data}")
        logger.info(f"💶 Valor: {valor}")
        logger.info(f"🕒 Data/Hora: {data}")

        assert valor is not None and data is not None
    except Exception as e:
        print(f"⚠️ Cotação não encontrada: {e}")
        assert False

    # Evidência visual
    page.screenshot(path="screenshots/cotacao.png", full_page=True)