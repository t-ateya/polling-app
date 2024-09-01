from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.services import utils

router = APIRouter()

@router.delete("/{poll_id}/")
def delete_poll(poll_id: UUID):
    if not utils.get_poll(poll_id):
        raise HTTPException(status_code = 404, detail="A poll by that id not found")
    utils.delete_poll(poll_id)
    return {"message": "The poll was deleted successfully"}
