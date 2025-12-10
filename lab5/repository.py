import pickle
from typing import Generic, TypeVar, Optional, List
from interfaces import IDataRepository

T = TypeVar('T')

class DataRepository(IDataRepository[T], Generic[T]):
    def __init__(self, filename: str):
        self.filename = filename
        self._load()

    def _load(self):
        try:
            with open(self.filename, 'rb') as f:
                self._data: List[T] = pickle.load(f)
        except FileNotFoundError:
            self._data = []

    def _save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self._data, f)

    def get_all(self) -> List[T]:
        return self._data.copy()

    def get_by_id(self, id: int) -> Optional[T]:
        for item in self._data:
            if getattr(item, 'id', None) == id:
                return item
        return None

    def add(self, item: T) -> None:
        self._data.append(item)
        self._save()

    def update(self, item: T) -> None:
        for i, existing in enumerate(self._data):
            if getattr(existing, 'id', None) == getattr(item, 'id', None):
                self._data[i] = item
                self._save()
                return

    def delete(self, item: T) -> None:
        self._data = [i for i in self._data if getattr(i, 'id', None) != getattr(item, 'id', None)]
        self._save()
