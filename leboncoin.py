from playwright.async_api import async_playwright
import asyncio, random, csv, os
from urllib.parse import urljoin

url = "https://www.leboncoin.fr/"
chemin_csv = r"C:\Users\ighik\OneDrive\Escritorio\html\BOTS\leboncoin_nom.csv"

# - Recherche
async def search(page, query="voiture"):
    await page.wait_for_timeout(random.randint(800, 1500))
    await page.mouse.move(200, 300)

    # Cookies
    btn = page.locator("button", has_text="Accepter")
    if await btn.count() > 0:
        await btn.first.click()

    await page.wait_for_timeout(random.randint(800, 1500))
    await page.mouse.move(300, 400)

    await page.fill('[data-test-id="extendable-input"]', query)
    await page.wait_for_timeout(random.randint(500, 1200))

    btn = page.locator('button[title="Valider votre recherche"]')
    if await btn.count() > 0:
        await btn.first.click()

    await page.wait_for_selector('[data-test-id="ad"]')

# - Nettoyage overlays
async def clean_overlays(page):
    await page.wait_for_timeout(random.randint(500, 1200))
    await page.mouse.move(250, 350)
    await page.evaluate("""
const selectors = ['#fixedban', 'div[id*="banner"]'];
                    selectors.forEach(sel => {
                        document.querySelectorAll(sel).forEach(el => el.remove());
                    });""")

# - Collecte des annonces
async def collect_data(page):
    data = []
    annonces = page.locator('[data-test-id="ad"]')
    total = await annonces.count()
    print(f"{total} annonces trouvées")

    for i in range(total):
        annonce = annonces.nth(i)

        # Nom des annonces
        try:
            nom = (await annonce.locator('[data-test-id="adcard-title"]').text_content()).strip()
        except:
            nom = "Pas de nom"

        # Prix des annonces
        try:
            prix = (await annonce.locator('[data-test-id="price"]').text_content()).strip()
        except:
            prix = "Pas de prix"
        
        # Lien annonces
        try:
            lien = await annonce.locator("a").first.get_attribute("href")
            lien = urljoin(url, lien)
        except:
            lien = ""

        print(nom, prix, lien)
        data.append({"Nom": nom, "Prix": prix, "Lien": lien})
    return data

# - Gestion du navigateur, user agent et anti-bot et csv
async def main():
    # Ouverture du CSV dès le départ
    csv_file = open(chemin_csv, "a", newline="", encoding="utf-8-sig")
    writer = csv.DictWriter(csv_file, fieldnames=["Nom", "Prix", "Lien"])
    if csv_file.tell() == 0:
        writer.writeheader()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=500,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"),
            locale="fr-FR",
            timezone_id="Europe/Paris"
        )

        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        page = await context.new_page()

        # Navigation principale
        await page.goto(url)
        await page.wait_for_load_state("domcontentloaded")

        # Recherche + overlays
        await search(page, "voiture")
        await clean_overlays(page)

        # Boucle multi-pages
        page_count = 0
        
        while True:
            try:
                data = await collect_data(page)

                # Écriture sur le CSV après chaque page
                for row in data:
                    writer.writerow(row)
                csv_file.flush()
                os.fsync(csv_file.fileno())
                page_count += 1
                print(f"Page {page_count} enregistrée dans le CSV")

            except Exception as e:
                print(f"Erreur lors de la collecte des annonces : {e}")

            # Pagination
            next_btn = page.locator('[data-spark-component="pagination-next-trigger"]')
            try:
                await next_btn.wait_for(state="visible")
                await page.wait_for_timeout(random.randint(800, 1500))
                await page.mouse.move(200, 300)
                href = await next_btn.get_attribute("href")
            except:
                href = None

            if href:
                next_url = urljoin(url, href)
                await page.goto(next_url, wait_until="domcontentloaded" )
                print(f"Page suivante : {next_url}")
                await page.wait_for_selector('[data-test-id="ad"]')
            else:
                print("Plus de page suivante")
                break

        csv_file.close()
        print("Scraping terminé")

if __name__ == "__main__":
    asyncio.run(main())
