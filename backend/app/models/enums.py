from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    COMMERCIAL = "COMMERCIAL"
    MANAGER = "MANAGER"


class ProspectStatus(str, Enum):
    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    CONTACTED = "CONTACTED"
    FOLLOW_UP = "FOLLOW_UP"
    NEGOTIATION = "NEGOTIATION"
    CONVERTED = "CONVERTED"
    LOST = "LOST"
    LATER = "LATER"


class ProspectPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class ActivityType(str, Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    LINKEDIN = "LINKEDIN"
    MEETING = "MEETING"
    NOTE = "NOTE"
    OTHER = "OTHER"


class FollowUpStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"


class Department(str, Enum):
    COMMERCIAL = "Commercial"
    SUPPORT = "Support"
    TECHNIQUE = "Technique"
    COMPTABILITE = "Comptabilité"
    DIRECTION = "Direction"
