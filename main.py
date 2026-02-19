import json
import sys

from playwright.sync_api import sync_playwright, Page


def locate_text(page: Page, selector: str) -> str | None:
    text = page.locator(selector).text_content()
    if text:
        text.strip()
    return text


def locate_url(page: Page, selector: str) -> str | None:
    return page.locator(selector).get_attribute("href")


def main(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        next_button = page.get_by_label("Next page").last
        org_cards = page.locator("app-orgs-card")

        while True:
            org_cards.first.wait_for()
            for org_card in org_cards.all():
                org_anchor = org_card.locator("a")
                with context.expect_page() as org_page_event:
                    org_anchor.click()
                org_page = org_page_event.value

                title = locate_text(org_page, "app-org-page-title .title")
                subtitle = locate_text(org_page, "app-org-info .hd")
                tech = locate_text(org_page, "app-org-info .tech__content")
                topics = locate_text(org_page, "app-org-info .topics__content")
                link = locate_url(org_page, "app-org-info .link__wrapper a")
                ideas = locate_url(org_page, ".button-wrapper a")
                summary = locate_text(org_page, "app-org-info .bd")

                org = {
                    "title": title,
                    "subtitle": subtitle,
                    "technologies": tech,
                    "topics": topics,
                    "link": link,
                    "ideas": ideas,
                    "summary": summary,
                }
                print(json.dumps(org, ensure_ascii=True, indent=4))

                org_page.close()
                break
            break

            if next_button.is_disabled():
                break
            else:
                next_button.click()


if __name__ == "__main__":
    url = sys.argv[1]
    main(url)
