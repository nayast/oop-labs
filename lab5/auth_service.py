import pickle
import os
from typing import Optional
from user import User
from interfaces import IAuthService, IUserRepository


class AuthService(IAuthService):
    def __init__(self, user_repo: IUserRepository, session_file: str = 'session.pkl'):
        self.session_file = session_file
        self._current_user: Optional[User] = None
        self._user_repo = user_repo
        self._load_session()

    def _load_session(self):
        try:
            with open(self.session_file, 'rb') as f:
                self._current_user = self._user_repo.get_by_id(pickle.load(f))
        except FileNotFoundError:
            self._current_user = None

    def _save_session(self):
        if self._current_user:
            with open(self.session_file, 'wb') as f:
                pickle.dump(self._current_user.id, f)
        else:
            try:
                os.remove(self.session_file)
            except FileNotFoundError:
                pass

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> Optional[User]:
        return self._current_user

    def sign_in(self, user: User) -> None:
        self._current_user = user
        self._save_session()

    def sign_out(self, user: User) -> None:
        if self._current_user and self._current_user.id == user.id:
            self._current_user = None
            self._save_session()
