import sys
from playwright.sync_api import sync_playwright
import json


def main(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        next_button = page.get_by_label("Next page").last
        org_cards = page.locator("app-orgs-card")

        while True:
            page.wait_for_load_state("networkidle")
            for org_card in org_cards.all():
                org_anchor = org_card.locator("a")
                with context.expect_page() as org_page_event:
                    org_anchor.click()

                org_page = org_page_event.value
                org_page.wait_for_load_state("networkidle")
                org = {
                    "title": org_page.locator(
                        "app-org-page-title .title"
                    ).text_content(),
                    "subtitle": org_page.locator("app-org-info .hd").text_content(),
                    "technologies": org_page.locator(
                        "app-org-info .tech__content"
                    ).text_content(),
                    "topics": org_page.locator(
                        "app-org-info .topics__content"
                    ).text_content(),
                    "link": org_page.locator(
                        "app-org-info .link__wrapper a"
                    ).get_attribute("href"),
                    "ideas": org_page.locator(".button-wrapper a").get_attribute(
                        "href"
                    ),
                    "summary": org_page.locator("app-org-info .bd").text_content(),
                }
                org_page.close()

                print(json.dumps(org, indent=4))

            if next_button.is_disabled():
                break
            else:
                next_button.click()


if __name__ == "__main__":
    url = sys.argv[1]
    main(url)
