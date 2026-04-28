import os
import instructor
from groq import AsyncGroq
from app.schemas.dtos import JobOfferDto, JobOfferList 

class AIExtractionService:
    def __init__(self):
        # Initialisation du client Groq patché avec Instructor
        self.client = instructor.from_groq(AsyncGroq(api_key=os.getenv("GROQ_API_KEY")))
        self.model_name = os.getenv("GROQ_MODEL_NAME")
        
        self.prompt = """
        Tu es un expert en ressources humaines et un spécialiste de l'analyse de données structurées. 
        Ton objectif est d'analyser le texte fourni représentant une offre d'emploi et d'en extraire toutes les informations pertinentes pour remplir scrupuleusement le schéma JSON attendu.

        Voici tes consignes strictes pour l'extraction :

        1. CORRESPONDANCE DES ÉNUMÉRATIONS (Enums) :
           - Analyse le sens du texte pour déduire la bonne valeur de l'énumération.
           - Diplômes (SchoolLevel) : "Bac+4", "Maîtrise" ou "Master 1" -> MASTER. "Bac+2" ou "BTS" -> BTS.
           - Documents (DocumentType) : Si le texte demande "CNI", "Carte d'identité" ou "Passeport", utilise IDENTITY_DOC. Pour "Lettre de motivation", utilise COVER_LETTER.
           - Contrat (ContractType) : Mappe des termes comme "Temps plein" à CDI ou CDD selon le contexte, "Stage" à INTERNSHIP.
           - Les tags sont de type Competence, outils ou domaine

        2. GESTION DU CHAMP "DESCRIPTION" (CRITIQUE) :
           - Le champ description doit contenir un texte riche et lisible résumant les missions, le profil de l'offre, profil recherché(compétence, formation et expérience) et comment postuler.
           - Renvoie uniquement une chaîne de caractères Markdown propre structurée (utilise des puces et du gras). 
           - NE renvoie PAS l'arbre JSON Lexical ultra complexe, contente-toi d'un beau Markdown.

        3. DONNÉES MANQUANTES ET FIDÉLITÉ :
           - Si une information n'est pas explicitement mentionnée, laisse le champ à null (ou une liste vide []).
           - N'invente JAMAIS d'informations.

        4. LOCALISATION ET LANGUES :
           - Identifie clairement le pays et les villes de travail.
           - Extrais toutes les langues requises mentionnées.

        5. BOOLÉENS :
           - Mets is_urgent à true uniquement si le texte mentionne "urgent", "dès que possible" ou "ASAP". Sinon, laisse à false.
        Voici tes consignes STRICTES DE FORMATAGE (CRITIQUE) :

        1. FORMAT UUID : Le champ `id` exige un format UUID strict. Si le texte contient un ID numérique (ex: 1165314), NE LE METS PAS. Génère un UUID v4 aléatoire (ex: "550e8400-e29b-41d4-a716-446655440000").
        2. FORMAT DATE : Les dates (`publishedAt`, `expirationDate`) DOIVENT être au format ISO 8601 complet (ex: "2026-04-28T00:00:00Z"). Ne renvoie jamais une simple date courte.
        3. ENUMS ET VALEURS NULLES : Pour `contractType` et `jobType`, utilise UNIQUEMENT les valeurs autorisées. Si l'information est absente, mets `null`. Ne mets JAMAIS une chaîne vide ("").
        """

    async def extract_from_payload_text(self, text: str) -> JobOfferDto:
        if not text:
            raise ValueError("You have to provide a text.")

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                response_model=JobOfferDto, 
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.1
            )
            return response

        except Exception as e:
            raise Exception(f"Error while extracting the information by AI (Groq) : {str(e)}") 
        
    async def extract_multiple_from_text(self, text: str) -> list[JobOfferDto]:
        prompt_multiple = """
        Tu es un expert en recrutement. Je vais te donner le texte brut extrait de la page "Carrières" d'une entreprise.
        Ton objectif est de trouver TOUTES les offres d'emploi listées sur cette page et de les extraire dans une liste structurée.

        Règles STRICTES DE FORMATAGE (CRITIQUE) :
        1. ID (UUID) : Le champ `id` attend un format UUID. Si le site utilise un ID numérique (ex: "1172363"), ignore-le. Génère un UUID v4 valide et aléatoire pour chaque offre.
        2. DATES : Les champs de type date (`publishedAt`) DOIVENT être au format ISO 8601 (ex: "2026-04-28T00:00:00Z").
        3. VALEURS VIDES : Si une information (salaire, type de contrat, etc.) n'est pas sur la page, mets la valeur à `null`. Ne mets jamais de chaîne vide `""`.

        Règles métier :
        4. Trouve chaque poste proposé et crée une entrée.
        5. Applique les mêmes règles de correspondance d'Enums, de description Markdown propre, de localisation et de langues que d'habitude.
        6. Si tu ne trouves aucune offre d'emploi, renvoie une liste vide [].
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                response_model=JobOfferList, 
                messages=[
                    {"role": "system", "content": prompt_multiple},
                    {"role": "user", "content": text}
                ],
                temperature=0.1
            )
            
            # response est déjà un objet JobOfferList validé
            return response.offers

        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction multiple par l'IA (Groq) : {str(e)}")