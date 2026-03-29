import asyncio
from bs4 import BeautifulSoup
import markdownify
from playwright.async_api import async_playwright
import logging

# On importe ton service IA existant
from app.services.ai.ai_extraction_service import AIExtractionService
from app.schemas.dtos import JobOfferDto

logger = logging.getLogger(__name__)

class WebScrapingService:
    def __init__(self):
        self.ai_service = AIExtractionService()

    async def get_clean_text_from_url(self, url: str) -> str:
        """Charge la page avec un navigateur (Playwright), attend le JS, et extrait le Markdown."""
        async with async_playwright() as p:
            # Lancement d'un navigateur invisible
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # On va sur l'URL et on attend que le réseau soit calme (JS chargé)
                await page.goto(url, wait_until="networkidle", timeout=30000)
                html_content = await page.content()
            except Exception as e:
                logger.error(f"Erreur de navigation sur {url} : {e}")
                return ""
            finally:
                await browser.close()

        # Nettoyage avec BeautifulSoup : on retire ce qui perturbe l'IA
        soup = BeautifulSoup(html_content, "html.parser")
        for element in soup(["script", "style", "nav", "footer", "aside"]):
            element.decompose()

        # Conversion en Markdown clair
        main_content = str(soup.body) if soup.body else str(soup)
        clean_markdown = markdownify.markdownify(main_content, heading_style="ATX").strip()
        
        return clean_markdown

    async def scrape_offers_list(self, url: str) -> list[JobOfferDto]:
        """Scrape l'URL et extrait la liste des offres d'emploi."""
        page_text = await self.get_clean_text_from_url(url)
        
        if not page_text or len(page_text) < 50:
            raise ValueError("Impossible de lire la page ou la page est vide.")

        # On passe le texte nettoyé à Gemini
        offers = await self.ai_service.extract_multiple_from_text(page_text)
        return offers
    
    async def scrape_and_extract_offer(self, url: str) -> JobOfferDto | None:
        """Scrape l'URL d'une offre spécifique et extrait les détails de l'offre."""
        page_text = await self.get_clean_text_from_url(url)
        
        if not page_text or len(page_text) < 50:
            raise ValueError("Impossible de lire la page ou la page est vide.")

        offers = await self.ai_service.extract_multiple_from_text(page_text)
        return offers[0] if len(offers)>0 else None
    