import json
import os
import instructor
from groq import AsyncGroq
from app.schemas.dtos import MatchingScoreResponse

class AIMatchingService:
    def __init__(self):
        # Initialisation du client Groq patché avec Instructor
        self.client = instructor.from_groq(AsyncGroq(api_key=os.getenv("GROQ_API_KEY")))
        self.model_name = os.getenv("GROQ_MODEL_NAME")

    def _clean_lexical(self, json_desc: str) -> str:
        """Nettoie le JSON de l'éditeur de texte riche."""
        if not json_desc or not str(json_desc).startswith("{"): return str(json_desc)
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

    def _format_offer_for_prompt(self, offer) -> str:
        """Adapte l'objet (DB Model ou Pydantic DTO) en texte clair."""
        if hasattr(offer, 'model_dump'):
            title = offer.title
            contract = offer.contract_type.value if offer.contract_type else "Non précisé"
            country = offer.work_country_location
            cities = offer.work_cities
            languages = offer.required_languages
            tags = [t.name for t in offer.tag_dto] if offer.tag_dto else []
            desc_text = offer.description 
        else:
            title = offer.title
            contract = offer.contract_type
            country = offer.work_country_location
            cities = [c.city for c in offer.cities] if offer.cities else []
            languages = [l.language for l in offer.languages] if offer.languages else []
            tags = [t.name for t in offer.tags] if offer.tags else []
            desc_text = self._clean_lexical(offer.description)

        return f"""
        --- OFFRE D'EMPLOI ---
        Titre : {title}
        Type de contrat : {contract}
        Pays : {country}
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
            # Appel à Groq via Instructor
            response = await self.client.chat.completions.create(
                model=self.model_name,
                response_model=MatchingScoreResponse, # Pydantic Model direct
                messages=[
                    {"role": "system", "content": "Tu es un assistant spécialisé en ressources humaines. Tu dois répondre avec un JSON parfaitement structuré."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            # Instructor renvoie directement l'objet Pydantic validé !
            return response
            
        except Exception as e:
            raise Exception(f"Erreur d'analyse IA avec Groq : {str(e)}")