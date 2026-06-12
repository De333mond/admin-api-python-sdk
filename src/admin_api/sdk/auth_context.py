from dataclasses import dataclass


@dataclass
class User:
    user_id: str


@dataclass
class AuthContext:
    user: User
