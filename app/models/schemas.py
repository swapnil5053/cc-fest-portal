from pydantic import BaseModel, constr, conint


class RegisterForm(BaseModel):
    username: constr(min_length=3, max_length=32)
    password: constr(min_length=6, max_length=128)


class LoginForm(BaseModel):
    username: constr(min_length=3, max_length=32)
    password: constr(min_length=6, max_length=128)


class EventCreateForm(BaseModel):
    name: constr(min_length=3, max_length=100)
    description: constr(min_length=10, max_length=300)
    fee: conint(ge=0)
    capacity: conint(ge=1)
