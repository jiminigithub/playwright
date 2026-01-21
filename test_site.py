import google.genai as genai

#client = genai.Client(api_key="")

# Lista todos os modelos disponíveis
#for m in client.models.list():
    #print(m.name)

from playwright.sync_api import sync_playwright
import google.genai as genai

# Configure sua chave Gemini
client = genai.Client(api_key="")  # substitua pela sua chave

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://brasil.bnpparibas/pt/", timeout=60000)

        # Fecha a janela de cookies se aparecer
        try:
            page.wait_for_selector("text=Permitir tudo", timeout=5000)
            page.click("text=Permitir tudo")
            print("✅ Janela de cookies fechada com sucesso.")
        except:
            print("⚠️ Janela de cookies não apareceu ou já estava fechada.")

        # Navega para a seção "GRUPO BNP PARIBAS"
        page.wait_for_selector("text=GRUPO BNP PARIBAS", timeout=10000)
        page.click("text=GRUPO BNP PARIBAS")
        page.wait_for_timeout(3000)

        # Aguarda carregamento da seção "Quem somos"
        page.wait_for_selector("text=Quem somos", timeout=10000)
        page.wait_for_timeout(3000)

        # Navega para a seção "Quem somos"
        page.click("text=Quem somos")
        page.wait_for_timeout(3000)

        # Extrai texto visível da página
        try:
            texto = page.locator("main").inner_text()
            if not texto.strip():
                print("⚠️ Nenhum texto capturado em <main>, tentando <body>...")
                texto = page.locator("body").inner_text()
        except Exception as e:
            print(f"⚠️ Erro ao extrair texto: {e}")
            texto = page.locator("body").inner_text()

        # Mostra parte do texto para validação
        print("\n📄 Texto extraído (prévia):\n")
        print(texto[:500])

        browser.close()
    return texto


def analisar_com_gemini(texto):
    partes = [texto[i:i + 2000] for i in range(0, len(texto), 2000)]
    for i, parte in enumerate(partes, 1):
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=f"Resuma e gere insights sobre este trecho ({i}):\n\n{parte}",
            config={"max_output_tokens": 800}
        )
        print(f"\n🔍 Análise do bloco {i}:\n")
        print(response.text)


# Executa tudo
if __name__ == "__main__":
    texto_extraido = run()
    analisar_com_gemini(texto_extraido)
