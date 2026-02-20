import os
from fastapi import UploadFile

from google import genai
from google.genai import types

from app.schemas.dtos import JobOfferDto 

class AIExtractionService:
    def __init__(self):
        # CORRECTION 1 : Mettre le bon nom de variable d'environnement
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = 'gemini-2.5-flash'

    async def extract_from_payload_file(self, file: UploadFile) -> JobOfferDto:
        print(self.client)
        prompt = """
        Tu es un expert en ressources humaines et un spécialiste de l'analyse de données structurées. 
        Ton objectif est d'analyser le document fourni (qui peut être un texte, une image ou un PDF représentant une offre d'emploi) et d'en extraire toutes les informations pertinentes pour remplir scrupuleusement le schéma JSON attendu.

        Voici tes consignes strictes pour l'extraction :

        1. CORRESPONDANCE DES ÉNUMÉRATIONS (Enums) :
           - Analyse le sens du texte pour déduire la bonne valeur de l'énumération.
           - Diplômes (SchoolLevel) : "Bac+4", "Maîtrise" ou "Master 1" -> MASTER. "Bac+2" ou "BTS" -> BTS.
           - Documents (DocumentType) : Si le texte demande "CNI", "Carte d'identité" ou "Passeport", utilise IDENTITY_DOC. Pour "Lettre de motivation", utilise COVER_LETTER.
           - Contrat (ContractType) : Mappe des termes comme "Temps plein" à CDI ou CDD selon le contexte, "Stage" à INTERNSHIP.
           - Les tags sont de type Competence, outils ou domaine

        2. GESTION DU CHAMP "DESCRIPTION" (CRITIQUE) :
           - Le champ description doit contenir un texte riche et lisible résumant les missions et le profil de l'offre.
           - UTILISE UNIQUEMENT LE FORMAT MARKDOWN pour formater cette description (utilise des puces -, du gras **texte**, et des sauts de ligne). 
           - NE GÉNÈRE SOUS AUCUN PRÉTEXTE un format JSON imbriqué. Renvoie uniquement une chaîne de caractères Markdown propre.

        3. DONNÉES MANQUANTES ET FIDÉLITÉ :
           - Si une information n'est pas explicitement mentionnée, laisse le champ à null (ou une liste vide []).
           - N'invente JAMAIS d'informations.

        4. LOCALISATION ET LANGUES :
           - Identifie clairement le pays et les villes de travail.
           - Extrais toutes les langues requises mentionnées.

        5. BOOLÉENS :
           - Mets is_urgent à true uniquement si le texte mentionne "urgent", "dès que possible" ou "ASAP". Sinon, laisse à false.
        """

        if not file:
            raise ValueError("Vous devez fournir un fichier.")

        contents = [prompt]

        file_bytes = await file.read()
        contents.append(
            types.Part.from_bytes(
                data=file_bytes,
                mime_type=file.content_type
            )
        )

        try:
            # CORRECTION 2 : Utiliser .aio pour l'appel asynchrone et ajouter "await"
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=JobOfferDto, 
                    temperature=0.1
                )
            )
            
            return JobOfferDto.model_validate_json(response.text)

        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction par l'IA : {str(e)}") 