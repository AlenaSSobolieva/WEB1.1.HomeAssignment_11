# fastapi_contacts/app/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_contacts.app import crud, database, models

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define API routes and operations
@router.post("/contacts/", response_model=models.Contact)
def create_contact(contact_data: dict, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact_data)

@router.get("/contacts/", response_model=list[models.Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)

@router.get("/contacts/{contact_id}", response_model=models.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    return crud.get_contact_by_id(db, contact_id)

@router.put("/contacts/{contact_id}", response_model=models.Contact)
def update_contact(contact_id: int, contact_data: dict, db: Session = Depends(get_db)):
    return crud.update_contact(db, contact_id, contact_data)

@router.delete("/contacts/{contact_id}", response_model=models.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    return crud.delete_contact(db, contact_id)
