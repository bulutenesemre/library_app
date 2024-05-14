import logging

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.db import repositories, schemas
from app.core.config import get_db
from app.db.models import User

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/", response_model=schemas.PatronBase)
def create_patron(patron: schemas.PatronBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        created_patron = repositories.PatronRepository.create_patron(db=db, patron=patron)
        logger.info(f"Patron created: {created_patron}")
        return created_patron
    except Exception as e:
        logger.error(f"Error creating patron: {e}")
        raise


@router.get("/", response_model=List[schemas.PatronBase])
def read_patrons(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        patrons = repositories.PatronRepository.get_all_patrons(db=db)
        logger.info("Retrieved all patrons")
        return patrons
    except Exception as e:
        logger.error(f"Error retrieving patrons: {e}")
        raise


@router.get("/{patron_id}", response_model=schemas.PatronBase)
def read_patron_by_id(patron_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        patron = repositories.PatronRepository.get_patron_by_id(db=db, patron_id=patron_id)
        if patron is None:
            logger.error(f"Patron with ID {patron_id} not found")
            raise HTTPException(status_code=404, detail="Patron not found")
        else:
            logger.info(f"Retrieved patron with ID {patron_id}")
            return patron
    except Exception as e:
        logger.error(f"Error retrieving patron with ID {patron_id}: {e}")
        raise


@router.put("/{patron_id}", response_model=schemas.PatronBase)
def update_patron(patron_id: int, patron: schemas.PatronBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        updated_patron = repositories.PatronRepository.update_patron(db=db, patron_id=patron_id, patron=patron)
        if updated_patron is None:
            logger.error(f"Patron with ID {patron_id} not found")
            raise HTTPException(status_code=404, detail="Patron not found")
        else:
            logger.info(f"Updated patron with ID {patron_id}")
            return updated_patron
    except Exception as e:
        logger.error(f"Error updating patron with ID {patron_id}: {e}")
        raise


@router.delete("/{patron_id}")
def delete_patron(patron_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        deleted = repositories.PatronRepository.delete_patron(db=db, patron_id=patron_id)
        if not deleted:
            logger.error(f"Patron with ID {patron_id} not found")
            raise HTTPException(status_code=404, detail="Patron not found")
        else:
            logger.info(f"Deleted patron with ID {patron_id}")
            return {"message": "Patron deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting patron with ID {patron_id}: {e}")
        raise