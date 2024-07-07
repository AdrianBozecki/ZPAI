from business_logic.entities.spooncular_recipes import SpooncularRecipeEntity, \
    SpooncularIngredientsEntity


def convert_from_json_to_entity(general_data: dict[str, any], additional_data: dict[str, any]) -> SpooncularRecipeEntity:
    return SpooncularRecipeEntity(
        title=general_data["title"],
        image=general_data["image"],
        missed_ingredients=[SpooncularIngredientsEntity.model_validate(i) for i in general_data["missedIngredients"]],
        used_ingredients=[SpooncularIngredientsEntity.model_validate(i) for i in general_data["usedIngredients"]],
        instructions=additional_data["instructions"],
        summary=additional_data["summary"],
    )