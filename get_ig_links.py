"""
Obtenedor de links de un perfil de Instagram (posts + reels)
- Sin duplicados
- En orden de aparicion (de arriba hacia abajo)
- Salida: un link por linea en <usuario>.txt

Uso:
    python get_ig_links.py <usuario>
    python get_ig_links.py <usuario> --headless
    python get_ig_links.py <usuario> --user-data-dir "C:\\Users\\stgom\\AppData\\Local\\Google\\Chrome\\User Data"
"""

import argparse
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


POST_MARKERS = ("/p/", "/reel/")
SCROLL_PAUSE = 2.0
MAX_STALE_ROUNDS = 4


def build_driver(user_data_dir: str | None, chromedriver_path: str | None, headless: bool):
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("log-level=3")
    if user_data_dir:
        options.add_argument(f"user-data-dir={user_data_dir}")
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1280,2000")

    if chromedriver_path:
        return webdriver.Chrome(service=Service(chromedriver_path), options=options)
    return webdriver.Chrome(options=options)


def collect_links_in_order(driver, seen: set, ordered: list) -> int:
    """Toma los anchors actuales del DOM y agrega los nuevos manteniendo el orden."""
    added = 0
    anchors = driver.find_elements(By.XPATH, "//a[@href]")
    for a in anchors:
        href = a.get_attribute("href") or ""
        if not any(m in href for m in POST_MARKERS):
            continue
        # Normalizar: quitar query string para deduplicar bien
        clean = href.split("?")[0].rstrip("/")
        if clean in seen:
            continue
        seen.add(clean)
        ordered.append(clean)
        added += 1
    return added


def scrape_profile(user: str, user_data_dir: str | None, chromedriver_path: str | None, headless: bool) -> list:
    driver = build_driver(user_data_dir, chromedriver_path, headless)
    seen: set = set()
    ordered: list = []
    try:
        driver.get(f"https://www.instagram.com/{user}/")
        time.sleep(5)

        collect_links_in_order(driver, seen, ordered)

        last_height = driver.execute_script("return document.body.scrollHeight")
        stale_rounds = 0

        while stale_rounds < MAX_STALE_ROUNDS:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE)

            added = collect_links_in_order(driver, seen, ordered)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height and added == 0:
                stale_rounds += 1
            else:
                stale_rounds = 0
                last_height = new_height
    finally:
        driver.quit()

    return ordered


def main():
    parser = argparse.ArgumentParser(description="Extrae los links de posts y reels de un perfil de Instagram.")
    parser.add_argument("user", help="Nombre de usuario de Instagram (sin @)")
    parser.add_argument("--user-data-dir", default=os.environ.get("CHROME_USER_DATA_DIR"),
                        help="Ruta al perfil de Chrome (para usar tu sesion ya iniciada). "
                             "Tambien se puede setear via env CHROME_USER_DATA_DIR.")
    parser.add_argument("--chromedriver", default=os.environ.get("CHROMEDRIVER_PATH"),
                        help="Ruta al ejecutable de chromedriver. Si no se pasa, se usa el del PATH/Selenium Manager.")
    parser.add_argument("--headless", action="store_true", help="Correr sin ventana del navegador.")
    parser.add_argument("-o", "--output", help="Archivo de salida. Por defecto <usuario>.txt")
    args = parser.parse_args()

    user = args.user.strip().lstrip("@")
    output = args.output or f"{user.replace('.', '')}.txt"

    print(f"Abriendo perfil de @{user} ...")
    links = scrape_profile(user, args.user_data_dir, args.chromedriver, args.headless)

    if not links:
        print("No se encontraron links. Posibles causas: necesitas iniciar sesion (--user-data-dir), "
              "el perfil es privado, o Instagram cargo lento.", file=sys.stderr)
        sys.exit(1)

    with open(output, "w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")

    print(f"Listo. {len(links)} links guardados en {output}")


if __name__ == "__main__":
    main()
