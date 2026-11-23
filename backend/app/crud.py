
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
