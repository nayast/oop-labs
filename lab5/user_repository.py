from typing import Optional
from user import User
from repository import DataRepository
from interfaces import IUserRepository

class UserRepository(DataRepository[User], IUserRepository):
    def get_by_login(self, login: str) -> Optional[User]:
        for user in self._data:
            if user.login == login:
                return user
        return None
