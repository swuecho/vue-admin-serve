from typing import Any, Optional

from django.http import HttpRequest
from ninja import NinjaAPI, Schema
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication


class GlobalJWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        user_and_token = JWTAuthentication().authenticate(request)
        if user_and_token is not None:
            [user, claims] = user_and_token
            request.user = user
            request.claims = claims
            return user
        else:
            return None


api = NinjaAPI(auth=GlobalJWTAuth())


@api.get("/ninja_demo/hello")
def hello(request, name: str = "world"):
    print(request.user)
    print(request.claims)
    return f"Hello {name}"


@api.get("/ninjia_demo/math")
def math(request, a: int, b: int):
    return {"add": a + b, "multiply": a * b}


class HelloSchema(Schema):
    name: str = "world"


@api.post("/ninja_demo/hello_schema")
def hello_schema(request, data: HelloSchema):
    return f"Hello {data.name}"


class UserSchema(Schema):
    username: str
    is_authenticated: bool
    # Unauthenticated users don't have the following fields, so provide defaults.
    email: str = None
    first_name: str = None
    last_name: str = None


@api.get("/ninja_demo/me", response=UserSchema)
def me(request):
    print((1, request.claims))
    claims = request.claims
    print(type(claims))
    jwt_payload = claims.payload
    print(jwt_payload)
    role = request.claims.get("role")
    print(role)
    return request.user
