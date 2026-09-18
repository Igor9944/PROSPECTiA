from datetime import date, datetime, timezone
from enum import Enum

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.activity import Activity
from app.models.company import Company
from app.models.contact import Contact
from app.models.conversion import Conversion
from app.models.enums import FollowUpStatus, ProspectStatus
from app.models.follow_up import FollowUp
from app.models.prospect import Prospect
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.schemas.contact import ContactCreate, ContactUpdate
from app.schemas.conversion import ConversionCreate
from app.schemas.follow_up import FollowUpCreate, FollowUpUpdate
from app.schemas.prospect import ProspectCreate, ProspectUpdate
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.services.qualification import qualify_prospect


def dump_data(payload) -> dict:
    data = payload.model_dump() if hasattr(payload, "model_dump") else dict(payload)
    return {key: (value.value if isinstance(value, Enum) else value) for key, value in data.items()}


def apply_updates(instance, data: dict):
    for key, value in data.items():
        if value is not None:
            setattr(instance, key, value.value if isinstance(value, Enum) else value)
    if hasattr(instance, "updated_at"):
        instance.updated_at = datetime.now(timezone.utc)
    return instance


class UserService:
    def list(self, db: Session) -> list[User]:
        return db.query(User).order_by(User.id).all()

    def get(self, db: Session, user_id: int) -> User | None:
        return db.get(User, user_id)

    def create(self, db: Session, payload: UserCreate) -> User:
        user = User(
            name=payload.name,
            email=payload.email,
            password_hash=get_password_hash(payload.password),
            role=payload.role.value if isinstance(payload.role, Enum) else payload.role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user: User, payload: UserUpdate) -> User:
        data = payload.model_dump(exclude_unset=True)
        password = data.pop("password", None)
        apply_updates(user, data)
        if password:
            user.password_hash = get_password_hash(password)
        db.commit()
        db.refresh(user)
        return user


class CompanyService:
    def list(self, db: Session) -> list[Company]:
        return db.query(Company).order_by(Company.name).all()

    def get(self, db: Session, company_id: int) -> Company | None:
        return db.get(Company, company_id)

    def create(self, db: Session, payload: CompanyCreate) -> Company:
        company = Company(**dump_data(payload))
        db.add(company)
        db.commit()
        db.refresh(company)
        return company

    def update(self, db: Session, company: Company, payload: CompanyUpdate) -> Company:
        apply_updates(company, payload.model_dump(exclude_unset=True))
        db.commit()
        db.refresh(company)
        return company

    def delete(self, db: Session, company: Company) -> None:
        db.delete(company)
        db.commit()


class ProspectService:
    def query(self, db: Session):
        return db.query(Prospect).options(joinedload(Prospect.company), joinedload(Prospect.assigned_user))

    def list_filtered(
        self,
        db: Session,
        *,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        industry: str | None = None,
        assigned_to: int | None = None,
        min_score: float | None = None,
        city: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        page: int = 1,
        page_size: int = 20,
        sort: str = "created_at",
        order: str = "desc",
    ):
        query = self.query(db).join(Company)
        if search:
            like = f"%{search}%"
            query = query.filter(or_(Company.name.ilike(like), Prospect.notes.ilike(like), Company.city.ilike(like)))
        if status:
            query = query.filter(Prospect.status == status)
        if priority:
            query = query.filter(Prospect.priority == priority)
        if industry:
            query = query.filter(Company.industry == industry)
        if assigned_to:
            query = query.filter(Prospect.assigned_to == assigned_to)
        if min_score is not None:
            query = query.filter(Prospect.score >= min_score)
        if city:
            query = query.filter(Company.city.ilike(f"%{city}%"))
        if date_from:
            query = query.filter(Prospect.created_at >= datetime.combine(date_from, datetime.min.time()))
        if date_to:
            query = query.filter(Prospect.created_at <= datetime.combine(date_to, datetime.max.time()))
        sortable = {
            "created_at": Prospect.created_at,
            "score": Prospect.score,
            "priority": Prospect.priority,
            "status": Prospect.status,
            "estimated_value": Prospect.estimated_value,
        }
        column = sortable.get(sort, Prospect.created_at)
        query = query.order_by(column.desc() if order == "desc" else column.asc())
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def get(self, db: Session, prospect_id: int) -> Prospect | None:
        return self.query(db).filter(Prospect.id == prospect_id).first()

    def create(self, db: Session, payload: ProspectCreate) -> Prospect:
        prospect = Prospect(**dump_data(payload))
        db.add(prospect)
        db.commit()
        db.refresh(prospect)
        qualification = qualify_prospect(db, prospect)
        prospect.score = qualification.score
        prospect.priority = qualification.priority.value
        db.commit()
        return self.get(db, prospect.id)

    def update(self, db: Session, prospect: Prospect, payload: ProspectUpdate) -> Prospect:
        apply_updates(prospect, payload.model_dump(exclude_unset=True))
        db.commit()
        return self.get(db, prospect.id)

    def delete(self, db: Session, prospect: Prospect) -> None:
        db.delete(prospect)
        db.commit()

    def apply_qualification(self, db: Session, prospect: Prospect):
        qualification = qualify_prospect(db, prospect)
        prospect.score = qualification.score
        prospect.priority = qualification.priority.value
        db.commit()
        return qualification


class ContactService:
    def list_for_prospect(self, db: Session, prospect_id: int) -> list[Contact]:
        return db.query(Contact).filter(Contact.prospect_id == prospect_id).all()

    def get(self, db: Session, contact_id: int) -> Contact | None:
        return db.get(Contact, contact_id)

    def create(self, db: Session, payload: ContactCreate) -> Contact:
        contact = Contact(**dump_data(payload))
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact

    def update(self, db: Session, contact: Contact, payload: ContactUpdate) -> Contact:
        apply_updates(contact, payload.model_dump(exclude_unset=True))
        db.commit()
        db.refresh(contact)
        return contact

    def delete(self, db: Session, contact: Contact) -> None:
        db.delete(contact)
        db.commit()


class ActivityService:
    def list(self, db: Session, prospect_id: int | None = None) -> list[Activity]:
        query = db.query(Activity)
        if prospect_id:
            query = query.filter(Activity.prospect_id == prospect_id)
        return query.order_by(Activity.created_at.desc()).all()

    def get(self, db: Session, activity_id: int) -> Activity | None:
        return db.get(Activity, activity_id)

    def create(self, db: Session, payload: ActivityCreate, user_id: int) -> Activity:
        activity = Activity(**dump_data(payload), user_id=user_id)
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    def update(self, db: Session, activity: Activity, payload: ActivityUpdate) -> Activity:
        apply_updates(activity, payload.model_dump(exclude_unset=True))
        db.commit()
        db.refresh(activity)
        return activity


class FollowUpService:
    def list(self, db: Session, bucket: str | None = None) -> list[FollowUp]:
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start.replace(hour=23, minute=59, second=59)
        query = db.query(FollowUp)
        if bucket == "today":
            query = query.filter(FollowUp.due_date >= today_start, FollowUp.due_date <= today_end)
        elif bucket == "overdue":
            query = query.filter(FollowUp.due_date < today_start, FollowUp.status == FollowUpStatus.PENDING.value)
        elif bucket == "upcoming":
            query = query.filter(FollowUp.due_date > today_end)
        return query.order_by(FollowUp.due_date.asc()).all()

    def get(self, db: Session, follow_up_id: int) -> FollowUp | None:
        return db.get(FollowUp, follow_up_id)

    def create(self, db: Session, payload: FollowUpCreate) -> FollowUp:
        follow_up = FollowUp(**dump_data(payload))
        db.add(follow_up)
        db.commit()
        db.refresh(follow_up)
        return follow_up

    def update(self, db: Session, follow_up: FollowUp, payload: FollowUpUpdate) -> FollowUp:
        apply_updates(follow_up, payload.model_dump(exclude_unset=True))
        db.commit()
        db.refresh(follow_up)
        return follow_up


class ConversionService:
    def list(self, db: Session) -> list[Conversion]:
        return db.query(Conversion).order_by(Conversion.converted_at.desc()).all()

    def convert(self, db: Session, payload: ConversionCreate, user_id: int) -> Conversion:
        prospect = db.get(Prospect, payload.prospect_id)
        if not prospect:
            raise ValueError("Prospect introuvable")
        conversion = Conversion(
            prospect_id=payload.prospect_id,
            converted_by=user_id,
            department=payload.department.value,
            value=payload.value,
            notes=payload.notes,
        )
        prospect.status = ProspectStatus.CONVERTED.value
        db.add(conversion)
        db.commit()
        db.refresh(conversion)
        return conversion


user_service = UserService()
company_service = CompanyService()
prospect_service = ProspectService()
contact_service = ContactService()
activity_service = ActivityService()
follow_up_service = FollowUpService()
conversion_service = ConversionService()
