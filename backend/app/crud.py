from sqlalchemy.orm import Session

from app import models


# Find a company by its ticker symbol
def get_company(db: Session, symbol: str):
    return db.query(models.Company).filter(
        models.Company.symbol == symbol.upper()
    ).first()


# Add a new company to the database
def create_company(db: Session, symbol: str, name: str = None):
    company = models.Company(
        symbol=symbol.upper(),
        name=name
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company


# Get all saved companies
def get_companies(db: Session):
    return db.query(models.Company).all()


# Delete a company from the database
def delete_company(db: Session, company):
    db.delete(company)
    db.commit()

    return company
from sqlalchemy.orm import Session
from app import models


def get_company(db: Session, symbol: str):
    return db.query(models.Company).filter(
        models.Company.symbol == symbol.upper()
    ).first()


def create_company(db: Session, symbol: str, name: str = None):
    company = models.Company(
        symbol=symbol.upper(),
        name=name
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company


def get_companies(db: Session):
    return db.query(models.Company).all()
