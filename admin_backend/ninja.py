from typing import Any, Optional

from django.http import HttpRequest
from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication


class GlobalJWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        user_and_token = JWTAuthentication().authenticate(request)
        if user_and_token is not None:
            user = user_and_token[0]
            request.user = user
            request.claims = user_and_token[1]
            return user
        else:
            return None


api = NinjaAPI(auth=GlobalJWTAuth())


@api.get("/hello")
def hello(request, name: str = "world"):
    print(request.user)
    print(repr(request.claims))
    return f"Hello {name}"


@api.get("/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}


class HelloSchema(Schema):
    name: str = "world"


@api.post("/hello_schema")
def hello_schema(request, data: HelloSchema):
    return f"Hello {data.name}"


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users don't have the following fields, so provide defaults.
    email: str = None
    first_name: str = None
    last_name: str = None


@api.get("/me", response=UserSchema)
def me(request):
    return request.user
