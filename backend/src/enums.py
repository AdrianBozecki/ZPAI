import enum


class LikeDislikeEnum(enum.Enum):
    LIKE = 1
    DISLIKE = -1

class UnitOfMeasureEnum(enum.Enum):
    GRAM = "GRAM"
    KILOGRAM = "KILOGRAM"
    MILLILITER = "MILLILITER"
    LITER = "LITER"
    PIECE = "PIECE"
    OUNCE = "OUNCE"
    POUND = "POUND"
    PINT = "PINT"
    QUART = "QUART"
    GALLON = "GALLON"
    TEASPOON = "TEASPOON"
    TABLESPOON = "TABLESPOON"
    CUP = "CUP"

class UnitSystemEnum(enum.Enum):
    METRIC = "METRIC"
    IMPERIAL = "IMPERIAL"