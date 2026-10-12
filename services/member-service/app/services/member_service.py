from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.member import Member

DEFAULT_MEMBER_NAMES = ("Polar", "Seven707", "Lupita")


def seed_default_members(db: Session) -> None:
    """Create the initial team only when no members have been registered."""
    if db.scalar(select(Member.id).limit(1)) is not None:
        return

    db.add_all(Member(name=name) for name in DEFAULT_MEMBER_NAMES)
    db.commit()


def create_member(db: Session, name: str) -> Member:
    member = Member(name=name)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def list_members(db: Session) -> list[Member]:
    return list(db.scalars(select(Member).order_by(Member.id)).all())


def get_member(db: Session, member_id: int) -> Member | None:
    return db.get(Member, member_id)
