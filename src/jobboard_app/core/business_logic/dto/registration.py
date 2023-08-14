from dataclasses import dataclass


@dataclass
class RegistrationDTO:
    username: str
    password: str
    email: str
    role: str

    def __str__(self) -> str:
        return f"username={self.username} email={self.email} role={self.role}"
