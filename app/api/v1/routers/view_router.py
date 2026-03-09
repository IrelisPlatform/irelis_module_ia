from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

# On indique à FastAPI où trouver les fichiers HTML
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", name="dashboard")
async def afficher_dashboard(request: Request):
    # On retourne le fichier HTML en lui passant des variables (le "context")
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "titre": "Tableau de bord",
            "utilisateur": "Recruteur Pro",
            "session_id": "12345-ABC"
        }
    )