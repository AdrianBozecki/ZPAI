from enums import UnitOfMeasureEnum, UnitSystemEnum


class UnitConverter:
    METRIC_CONVERSIONS = {
        UnitOfMeasureEnum.GRAM: (1, UnitOfMeasureEnum.GRAM),
        UnitOfMeasureEnum.KILOGRAM: (1, UnitOfMeasureEnum.KILOGRAM),
        UnitOfMeasureEnum.MILLILITER: (1, UnitOfMeasureEnum.MILLILITER),
        UnitOfMeasureEnum.LITER: (1, UnitOfMeasureEnum.LITER),
        UnitOfMeasureEnum.PIECE: (1, UnitOfMeasureEnum.PIECE),
        UnitOfMeasureEnum.OUNCE: (28.35, UnitOfMeasureEnum.GRAM),
        UnitOfMeasureEnum.POUND: (0.4566, UnitOfMeasureEnum.KILOGRAM),
        UnitOfMeasureEnum.PINT: (568, UnitOfMeasureEnum.MILLILITER),
        UnitOfMeasureEnum.QUART: (1.136, UnitOfMeasureEnum.LITER),
        UnitOfMeasureEnum.GALLON: (4.5461, UnitOfMeasureEnum.LITER),
        UnitOfMeasureEnum.TEASPOON: (5, UnitOfMeasureEnum.GRAM),
        UnitOfMeasureEnum.TABLESPOON: (15, UnitOfMeasureEnum.GRAM),
        UnitOfMeasureEnum.CUP: (250, UnitOfMeasureEnum.GRAM),
    }

    IMPERIAL_CONVERSIONS = {
        UnitOfMeasureEnum.GRAM: (0.035274, UnitOfMeasureEnum.OUNCE),
        UnitOfMeasureEnum.KILOGRAM: (2.20462, UnitOfMeasureEnum.POUND),
        UnitOfMeasureEnum.MILLILITER: (0.033814, UnitOfMeasureEnum.OUNCE),
        UnitOfMeasureEnum.LITER: (0.26, UnitOfMeasureEnum.GALLON),
        UnitOfMeasureEnum.PIECE: (1, UnitOfMeasureEnum.PIECE),
        UnitOfMeasureEnum.OUNCE: (1, UnitOfMeasureEnum.OUNCE),
        UnitOfMeasureEnum.POUND: (1, UnitOfMeasureEnum.POUND),
        UnitOfMeasureEnum.PINT: (1, UnitOfMeasureEnum.PINT),
        UnitOfMeasureEnum.QUART: (1, UnitOfMeasureEnum.QUART),
        UnitOfMeasureEnum.GALLON: (1, UnitOfMeasureEnum.GALLON),
        UnitOfMeasureEnum.TEASPOON: (0.17636981, UnitOfMeasureEnum.OUNCE),
        UnitOfMeasureEnum.TABLESPOON: (0.529109429, UnitOfMeasureEnum.OUNCE),
        UnitOfMeasureEnum.CUP: (14, UnitOfMeasureEnum.OUNCE),
    }

    @classmethod
    def convert_unit(cls, unit: UnitOfMeasureEnum, value: float, conversion_type: UnitSystemEnum) -> \
    tuple[float, str]:
        if conversion_type == UnitSystemEnum.METRIC:
            conversion_dict = cls.METRIC_CONVERSIONS
        elif conversion_type == UnitSystemEnum.IMPERIAL:
            conversion_dict = cls.IMPERIAL_CONVERSIONS
        else:
            raise ValueError(
                "Invalid conversion_type. Expected UnitSystemEnum.METRIC or UnitSystemEnum.IMPERIAL.")

        conversion_factor, target_unit = conversion_dict.get(unit, (1, 'unknown'))
        return round(value * conversion_factor, 2), target_unit