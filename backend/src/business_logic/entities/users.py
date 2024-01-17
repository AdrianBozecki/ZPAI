from pydantic import BaseModel


class BaseUserEntity(BaseModel):
    email: str
    name: str
    lastname: str
    phone_number: str



class CreateUserEntity(BaseUserEntity):
    password: str


class UserEntity(BaseUserEntity):
    id: int  # noqa: A003
    user_details_id: int
