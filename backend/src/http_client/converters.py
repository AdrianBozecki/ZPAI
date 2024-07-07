from business_logic.entities.spooncular_recipes import SpooncularRecipeEntity, \
    SpooncularIngredientsEntity


def convert_from_json_to_entity(json: dict[str, any]) -> SpooncularRecipeEntity:
    json = json[0]
    return SpooncularRecipeEntity(
        title=json["title"],
        image=json["image"],
        missed_ingredients=[SpooncularIngredientsEntity.model_validate(i) for i in json["missedIngredients"]],
        used_ingredients=[SpooncularIngredientsEntity.model_validate(i) for i in json["usedIngredients"]],
    )