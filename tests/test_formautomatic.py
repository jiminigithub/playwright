def test_formulario_obrigatorios(page):
    page.goto("https://jobs.gem.com/felix/am9icG9zdDpbX4Ewoaozk99vJjdyGiDz")  # substitua pela URL real


    # Rola até o final da página para garantir que o formulário seja renderizado
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_selector("text=Ready to apply?", timeout=10000)
    page.wait_for_timeout(5000)

    # Dados conhecidos
    dados = {
        "First name": "Jimini Andersson",
        "Last name": "Costa",
        "Email": "jimini_anderson@msn.com",
        "LinkedIn URL": "https://linkedin.com/in/jimini",
        "Phone number": "+55 13 99999-9999",
        "Location": "Santos, SP, Brasil"
    }

    # Detecta campos obrigatórios por atributos HTML
    obrigatorios = page.locator("input[required], textarea[required], input[aria-required='true'], textarea[aria-required='true']")
    count = obrigatorios.count()
    print(f"🔍 Detectados {count} campos obrigatórios.")

    for i in range(count):
        campo = obrigatorios.nth(i)
        label = campo.locator("xpath=ancestor::div//label").first.inner_text()
        label_limpo = label.replace("*", "").strip()

        valor = dados.get(label_limpo)
        if valor:
            campo.fill(valor)
            print(f"✅ Preenchido: {label_limpo} → {valor}")
        else:
            print(f"⚠️ Sem dado conhecido para '{label_limpo}'")

    # Evidência visual
    page.screenshot(path="screenshots/formulario_job_application.png", full_page=True)