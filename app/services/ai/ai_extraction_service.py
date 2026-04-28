import os
import instructor
from groq import AsyncGroq

import io
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from fastapi import UploadFile
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
           - Le champ description doit contenir un texte riche et lisible résumant les missions, le profil de l'offre, profil recherché(compétence, formation et expérience) et comment postuler  avec les parties suivante: .
           - Renvoie uniquement une chaîne de caractères Markdown propre comme celui ci et rien d'autre, pas de txte simple: 
                "{\"root\":{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous recherchez un stage académique au sein d’une entreprise offrant un cadre de travail 100% à distance et digital, où vous pourrez exprimer tout votre potentiel dans des conditions ultra-modernes et flexibles ?\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Nous vous proposons une période pratique de six (06) mois, au sein de notre \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"structure à taille humaine, \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"en qualité d'\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assistant(e) Administratif(ve) et RH - Stagiaire, avec possibilité d'évolution en CDI.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Nos conditions de travail\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\" :\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"L'ensemble de notre équipe évoluant en 100% télétravail, u\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":8,\"mode\":\"normal\",\"style\":\"\",\"text\":\"n ordinateur personnel connecté à internet sera \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":9,\"mode\":\"normal\",\"style\":\"\",\"text\":\"indispensable \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":8,\"mode\":\"normal\",\"style\":\"\",\"text\":\"à la réussite de votre projet de stage.\",\"type\":\"text\",\"version\":1},{\"type\":\"linebreak\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"NB : Vous effectuez votre stage depuis votre domicile : \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"aucun déplacement n'est requis.\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"MISSIONS : \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Sous la supervision de notre Direction, durant ce \",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"stage valorisant et riche en apprentissage\",\"type\":\"text\",\"version\":1},{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\", vous serez en charge de :\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Mener des actions destinées à enrichir, renforcer et diversifier notre CVthèque\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":1},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Rédiger et publier des offres emploi sur notre plateforme innovante , ou celles de nos partenaires\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":2},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assurer une réponse de premier niveau, un retour constructif et une orientation bienveillante aux candidats en recherche, via une excellente qualité rédactionnelle\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":3},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Être force de propositions pour instaurer une politique RH adaptée \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":4},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Développer et optimiser l'organisation de la gestion administrative et RH\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":5},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assurer quotidiennement le classement et l'archivage des documents \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":6},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Assister notre General Manager, dans la gestion des ressources humaines et la vie de l'entreprise\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":7},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Toute autre mission liée aux besoins de l'entreprise\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":8}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"list\",\"version\":1,\"listType\":\"bullet\",\"start\":1,\"tag\":\"ul\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"PROFIL : \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Etudiant(e) ou jeune diplômé(e) en Licence ou Master 1 ou 2 \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":1},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous possédez un ordinateur portable personnel et un accès internet permanent\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":2},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous êtes très organisé(e), autonome, rigoureux(se), ponctuel et fiable\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":3},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avez un bon niveau sur Excel, Word, Powerpoint, Canva et outils informatiques (Outlook, Google Drive, Google Meet)\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":4},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avec un excellent niveau d'orthographe et de grammaire\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":5},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avez bonnes connaissances (même théoriques) du Droit du Travail\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":6},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Vous avez une appétence pour les chiffres\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"listitem\",\"version\":1,\"value\":7}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"list\",\"version\":1,\"listType\":\"bullet\",\"start\":1,\"tag\":\"ul\"},{\"children\":[{\"detail\":0,\"format\":1,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Date de début et durée du stage : \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":1,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Lundi 2 février 2026 (date souhaitée)\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"6 mois, renouvelable une fois.\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Intéressé(e) par cette offre ? \",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"},{\"children\":[{\"detail\":0,\"format\":0,\"mode\":\"normal\",\"style\":\"\",\"text\":\"Envoyez votre CV et un mail de présentation (pitch mail)\",\"type\":\"text\",\"version\":1}],\"direction\":null,\"format\":\"start\",\"indent\":0,\"type\":\"paragraph\",\"version\":1,\"textFormat\":0,\"textStyle\":\"\"}],\"direction\":null,\"format\":\"\",\"indent\":0,\"type\":\"root\",\"version\":1}}"
           
        3. DONNÉES MANQUANTES ET FIDÉLITÉ :
           - Si une information n'est pas explicitement mentionnée, laisse le champ à null (ou une liste vide []).
           - N'invente JAMAIS d'informations.

        4. LOCALISATION ET LANGUES :
           - Identifie clairement le pays et les villes de travail.
           - Extrais toutes les langues requises mentionnées.

        5. BOOLÉENS :
           - Mets is_urgent à true uniquement si le texte mentionne "urgent", "dès que possible" ou "ASAP". Sinon, laisse à false.
        Voici tes consignes STRICTES DE FORMATAGE (CRITIQUE) :

         - FORMAT UUID : Le champ `id` exige un format UUID strict. Si le texte contient un ID numérique (ex: 1165314), NE LE METS PAS. Génère un UUID v4 aléatoire (ex: "550e8400-e29b-41d4-a716-446655440000").
         - FORMAT DATE : Les dates (`publishedAt`, `expirationDate`) DOIVENT être au format ISO 8601 complet (ex: "2026-04-28T00:00:00Z"). Ne renvoie jamais une simple date courte.
         - ENUMS ET VALEURS NULLES : Pour `contractType` et `jobType`, utilise UNIQUEMENT les valeurs autorisées. Si l'information est absente, mets `null`. Ne mets JAMAIS une chaîne vide ("").
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
    
    async def extract_from_payload_file(self, file: UploadFile) -> JobOfferDto:
        """
        Extrait le texte d'un PDF ou d'une image, puis l'envoie à Groq pour structuration.
        """
        if not file:
            raise ValueError("Veuillez fournir un fichier.")

        file_bytes = await file.read()
        extracted_text = ""

        try:
            # --- 1. CAS DU PDF ---
            if file.content_type == "application/pdf":
                reader = PdfReader(io.BytesIO(file_bytes))
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"

            elif file.content_type in ["image/jpeg", "image/jpg", "image/png", "image/webp"]:
                image = Image.open(io.BytesIO(file_bytes))
                extracted_text = pytesseract.image_to_string(image, lang='fra+eng')

            else:
                raise ValueError(f"Format non supporté : {file.content_type}")

            if not extracted_text or not extracted_text.strip():
                raise ValueError("Le fichier semble vide ou illisible (aucun texte extrait).")

            return await self.extract_from_payload_text(extracted_text)

        except Exception as e:
            raise Exception(f"Erreur lors du traitement du fichier : {str(e)}")
            
        finally:
            # Bonne pratique : remettre le curseur du fichier à zéro si un autre composant doit le lire
            await file.seek(0)