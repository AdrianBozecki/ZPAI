from pydantic import BaseModel


class BaseUserEntity(BaseModel):
    email: str
    password: str
    name: str
    lastname: str
    phone_number: str



class CreateUserEntity(BaseUserEntity):
    ...


class UserEntity(BaseUserEntity):
    id: int  # noqa: A003
    user_details_id: int
