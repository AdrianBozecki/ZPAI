import enum


class LikeDislikeEnum(enum.Enum):
    LIKE = 1
    DISLIKE = -1


class UnitOfMeasureEnum(enum.Enum):
    GRAM = "GRAM"
    MILLILITER = "MILLILITER"
    CENTIMETER = "CENTIMETER"
    PIECE = "PIECE"
