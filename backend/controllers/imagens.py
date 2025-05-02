from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/imagens", tags=["Imagens"])

@router.get("/{categoria}/{id}/{nome_arquivo}")
def get_imagem(categoria: str, id: int, nome_arquivo: str):
    try:
        caminho = os.path.join("uploadFiles", categoria, str(id), nome_arquivo)

        if not os.path.isfile(caminho):
            raise HTTPException(status_code=404, detail="Imagem não encontrada")

        return FileResponse(caminho)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

