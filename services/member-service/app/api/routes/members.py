from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberResponse
from app.services.member_service import (
    create_member,
    get_member,
    list_members,
)


router = APIRouter(prefix="/members", tags=["members"])


@router.post("", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def register_member(
    payload: MemberCreate,
    db: Session = Depends(get_db),
) -> Member:
    return create_member(db, payload.name)


@router.get("", response_model=list[MemberResponse])
def read_members(db: Session = Depends(get_db)) -> list[Member]:
    return list_members(db)


@router.get("/{member_id}", response_model=MemberResponse)
def read_member(member_id: int, db: Session = Depends(get_db)) -> Member:
    member = get_member(db, member_id)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integrante no encontrado",
        )
    return member
