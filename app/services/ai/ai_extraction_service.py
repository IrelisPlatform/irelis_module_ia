import os
from fastapi import UploadFile

from google import genai
from google.genai import types

from app.schemas.dtos import JobOfferDto, JobOfferList 

class AIExtractionService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = os.getenv("MODEL_NAME")
        self.prompt = """
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
           - Le champ description doit contenir un texte riche et lisible résumant les missions, le profil de l'offre, profil recherché(compétence, formation et expérience) et comment postuler  avec les parties suivante: .
           - Renvoie uniquement une chaîne de caractères Markdown propre comme celui ci : 
                "{\"root\":{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous recherchez un stage académique au sein d’une entreprise offrant un cadre de travail 100% à distance et digital, où vous pourrez exprimer tout votre potentiel dans des conditions ultra-modernes et flexibles ?\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Nous vous proposons une période pratique de six (06) mois, au sein de notre \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"structure à taille humaine, \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"en qualité d'\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assistant(e) Administratif(ve) et RH - Stagiaire, avec possibilité d'évolution en CDI.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Nos conditions de travail\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\" :\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"L'ensemble de notre équipe évoluant en 100% télétravail, u\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":8,\"mode\":\"normal\",\"style\":\"\",\"text\":\"n ordinateur personnel connecté à internet sera \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":9,\"mode\":\"normal\",\"style\":\"\",\"text\":\"indispensable \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":8,\"mode\":\"normal\",\"style\":\"\",\"text\":\"à la réussite de votre projet de stage.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"NB : Vous effectuez votre stage depuis votre domicile : \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"aucun déplacement n'est requis.\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"MISSIONS : \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Sous la supervision de notre Direction, durant ce \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"stage valorisant et riche en apprentissage\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\", vous serez en charge de :\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Mener des actions destinées à enrichir, renforcer et diversifier notre CVthèque\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":1},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Rédiger et publier des offres emploi sur notre plateforme innovante , ou celles de nos partenaires\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":2},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assurer une réponse de premier niveau, un retour constructif et une orientation bienveillante aux candidats en recherche, via une excellente qualité rédactionnelle\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":3},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Être force de propositions pour instaurer une politique RH adaptée \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":4},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Développer et optimiser l'organisation de la gestion administrative et RH\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":5},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assurer quotidiennement le classement et l'archivage des documents \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":6},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assister notre General Manager, dans la gestion des ressources humaines et la vie de l'entreprise\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":7},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Toute autre mission liée aux besoins de l'entreprise\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":8}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"list\",\"version\":1,\"listType\":\"bullet\",\"start\":1,\"tag\":\"ul\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"PROFIL : \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Etudiant(e) ou jeune diplômé(e) en Licence ou Master 1 ou 2 \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":1},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous possédez un ordinateur portable personnel et un accès internet permanent\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":2},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous êtes très organisé(e), autonome, rigoureux(se), ponctuel et fiable\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":3},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avez un bon niveau sur Excel, Word, Powerpoint, Canva et outils informatiques (Outlook, Google Drive, Google Meet)\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":4},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avec un excellent niveau d'orthographe et de grammaire\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":5},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avez bonnes connaissances (même théoriques) du Droit du Travail\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":6},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avez une appétence pour les chiffres\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":7}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"list\",\"version\":1,\"listType\":\"bullet\",\"start\":1,\"tag\":\"ul\"},{\"children\":[{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Date de début et durée du stage : \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":1,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Lundi 2 février 2026 (date souhaitée)\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"6 mois, renouvelable une fois.\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Intéressé(e) par cette offre ? \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Envoyez votre CV et un mail de présentation (pitch mail)\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"root\",\"version\":1}}"
           

        3. DONNÉES MANQUANTES ET FIDÉLITÉ :
           - Si une information n'est pas explicitement mentionnée, laisse le champ à null (ou une liste vide []).
           - N'invente JAMAIS d'informations.

        4. LOCALISATION ET LANGUES :
           - Identifie clairement le pays et les villes de travail.
           - Extrais toutes les langues requises mentionnées.

        5. BOOLÉENS :
           - Mets is_urgent à true uniquement si le texte mentionne "urgent", "dès que possible" ou "ASAP". Sinon, laisse à false.
        """

    async def extract_from_payload_file(self, file: UploadFile) -> JobOfferDto:

        if not file:
            raise ValueError("You have to provide a file.")

        contents = [self.prompt]

        file_bytes = await file.read()
        contents.append(
            types.Part.from_bytes(
                data=file_bytes,
                mime_type=file.content_type
            )
        )

        try:
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
            raise Exception(f"Error while extracting the information by AI : {str(e)}") 
        
    async def extract_from_payload_text(self, text: str) -> JobOfferDto:

        if not text:
            raise ValueError("You have to provide a text.")

        contents = [self.prompt]

        contents.append(text)

        try:
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
            raise Exception(f"Error while extracting the information by AI : {str(e)}") 
        


    async def extract_multiple_from_text(self, text: str) -> list[JobOfferDto]:
        prompt = """
        Tu es un expert en recrutement. Je vais te donner le texte brut extrait de la page "Carrières" d'une entreprise.
        Ton objectif est de trouver TOUTES les offres d'emploi listées sur cette page et de les extraire dans une liste structurée.

        Règles :
        1. Trouve chaque poste proposé et crée une entrée.
        Voici tes consignes strictes pour l'extraction :

        2. CORRESPONDANCE DES ÉNUMÉRATIONS (Enums) :
           - Analyse le sens du texte pour déduire la bonne valeur de l'énumération.
           - Diplômes (SchoolLevel) : "Bac+4", "Maîtrise" ou "Master 1" -> MASTER. "Bac+2" ou "BTS" -> BTS.
           - Documents (DocumentType) : Si le texte demande "CNI", "Carte d'identité" ou "Passeport", utilise IDENTITY_DOC. Pour "Lettre de motivation", utilise COVER_LETTER.
           - Contrat (ContractType) : Mappe des termes comme "Temps plein" à CDI ou CDD selon le contexte, "Stage" à INTERNSHIP.
           - Les tags sont de type Competence, outils ou domaine

        3. GESTION DU CHAMP "DESCRIPTION" (CRITIQUE) :
           - Le champ description doit contenir un texte riche et lisible résumant les missions, le profil de l'offre, profil recherché(compétence, formation et expérience) et comment postuler  avec les parties suivante: .
           - Renvoie uniquement une chaîne de caractères Markdown propre comme celui ci : 
                "{\"root\":{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous recherchez un stage académique au sein d’une entreprise offrant un cadre de travail 100% à distance et digital, où vous pourrez exprimer tout votre potentiel dans des conditions ultra-modernes et flexibles ?\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Nous vous proposons une période pratique de six (06) mois, au sein de notre \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"structure à taille humaine, \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"en qualité d'\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assistant(e) Administratif(ve) et RH - Stagiaire, avec possibilité d'évolution en CDI.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Nos conditions de travail\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\" :\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"L'ensemble de notre équipe évoluant en 100% télétravail, u\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":8,\"mode\":\"normal\",\"style\":\"\",\"text\":\"n ordinateur personnel connecté à internet sera \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":9,\"mode\":\"normal\",\"style\":\"\",\"text\":\"indispensable \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":8,\"mode\":\"normal\",\"style\":\"\",\"text\":\"à la réussite de votre projet de stage.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"NB : Vous effectuez votre stage depuis votre domicile : \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"aucun déplacement n'est requis.\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"MISSIONS : \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Sous la supervision de notre Direction, durant ce \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"stage valorisant et riche en apprentissage\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\", vous serez en charge de :\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Mener des actions destinées à enrichir, renforcer et diversifier notre CVthèque\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":1},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Rédiger et publier des offres emploi sur notre plateforme innovante , ou celles de nos partenaires\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":2},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assurer une réponse de premier niveau, un retour constructif et une orientation bienveillante aux candidats en recherche, via une excellente qualité rédactionnelle\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":3},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Être force de propositions pour instaurer une politique RH adaptée \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":4},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Développer et optimiser l'organisation de la gestion administrative et RH\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":5},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assurer quotidiennement le classement et l'archivage des documents \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":6},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assister notre General Manager, dans la gestion des ressources humaines et la vie de l'entreprise\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":7},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Toute autre mission liée aux besoins de l'entreprise\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":8}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"list\",\"version\":1,\"listType\":\"bullet\",\"start\":1,\"tag\":\"ul\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"PROFIL : \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Etudiant(e) ou jeune diplômé(e) en Licence ou Master 1 ou 2 \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":1},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous possédez un ordinateur portable personnel et un accès internet permanent\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":2},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous êtes très organisé(e), autonome, rigoureux(se), ponctuel et fiable\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":3},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avez un bon niveau sur Excel, Word, Powerpoint, Canva et outils informatiques (Outlook, Google Drive, Google Meet)\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":4},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avec un excellent niveau d'orthographe et de grammaire\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":5},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avez bonnes connaissances (même théoriques) du Droit du Travail\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":6},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avez une appétence pour les chiffres\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":7}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"list\",\"version\":1,\"listType\":\"bullet\",\"start\":1,\"tag\":\"ul\"},{\"children\":[{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Date de début et durée du stage : \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":1,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Lundi 2 février 2026 (date souhaitée)\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"6 mois, renouvelable une fois.\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Intéressé(e) par cette offre ? \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Envoyez votre CV et un mail de présentation (pitch mail)\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"root\",\"version\":1}}"
           

        4. DONNÉES MANQUANTES ET FIDÉLITÉ :
           - Si une information n'est pas explicitement mentionnée, laisse le champ à null (ou une liste vide []).
           - N'invente JAMAIS d'informations.

        5. LOCALISATION ET LANGUES :
           - Identifie clairement le pays et les villes de travail.
           - Extrais toutes les langues requises mentionnées.

        6. BOOLÉENS :
           - Mets is_urgent à true uniquement si le texte mentionne "urgent", "dès que possible" ou "ASAP". Sinon, laisse à false.
        7. Si tu ne trouves aucune offre d'emploi, renvoie une liste vide [].
        """

        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=[prompt, text],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    # ON PASSE LE SCHÉMA "JobOfferList" ICI
                    response_schema=JobOfferList, 
                    temperature=0.1
                )
            )
            
            # On parse le JSON retourné et on extrait la liste "offers"
            result = JobOfferList.model_validate_json(response.text)
            return result.offers

        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction multiple par l'IA : {str(e)}")