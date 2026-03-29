import json
from google import genai
from google.genai import types
from app.schemas.dtos import MatchingScoreResponse
# import de ton modèle JobOffer

class AIMatchingService:
    def __init__(self, client: genai.Client):
        self.client = client
        self.model_name = 'gemini-2.5-flash'

    def _format_offer_for_prompt(self, offer) -> str:
        """Transforme ton objet SQLAlchemy en texte clair pour l'IA."""
        
        # On utilise ton ancienne fonction pour nettoyer le JSON Lexical de la description
        def clean_lexical(json_desc):
            if not json_desc or not json_desc.startswith("{"): return str(json_desc)
            try:
                data = json.loads(json_desc)
                def recurse(node):
                    text = ""
                    if "text" in node: text += node["text"] + " "
                    if "children" in node:
                        for child in node["children"]: text += recurse(child)
                    return text
                return recurse(data.get("root", {}))
            except:
                return str(json_desc)

        desc_text = clean_lexical(offer.description)
        cities = [c.city for c in offer.cities] if offer.cities else []
        languages = [l.language for l in offer.languages] if offer.languages else []
        tags = [t.name for t in offer.tags] if offer.tags else []

        return f"""
        --- OFFRE D'EMPLOI ---
        Titre : {offer.title}
        Type de contrat : {offer.contract_type}
        Pays : {offer.work_country_location}
        Villes : {', '.join(cities)}
        Langues requises : {', '.join(languages)}
        Mots-clés/Tags : {', '.join(tags)}
        Description et Missions : {desc_text}
        """

    async def compute_matching(self, cv_text: str, offer) -> MatchingScoreResponse:
        offer_context = self._format_offer_for_prompt(offer)
        
        prompt = f"""
        Tu es un recruteur expert impitoyable mais juste. Ton rôle est d'évaluer la compatibilité entre un CV et une offre d'emploi.
        
        {offer_context}
        
        --- CV DU CANDIDAT ---
        {cv_text}
        
        --- INSTRUCTIONS D'ÉVALUATION STRICTES ---
        1. Ne donne JAMAIS 100% au score global à moins que le candidat ne soit un clone parfait de l'offre. Les bons matchs tournent autour de 70-85%.
        2. Analyse l'expérience RÉELLE : calcule mentalement les années d'expérience en regardant les dates des emplois, ne cherche pas juste le mot "ans".
        3. Comprends la sémantique : Si le CV dit "NodeJS" et l'offre "Javascript backend", c'est un match.
        4. Si une langue obligatoire ou une compétence cruciale est manquante, pénalise lourdement le score correspondant.
        5. Justifie ton score de manière professionnelle, comme si tu parlais au manager qui recrute.
        """

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=MatchingScoreResponse, 
                    temperature=0.0 # Température 0 : on veut de la logique pure, pas de créativité
                )
            )
            
            return MatchingScoreResponse.model_validate_json(response.text)
        except Exception as e:
            raise Exception(f"Erreur d'analyse IA : {str(e)}")