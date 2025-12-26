from typing import Protocol, TypeVar, Generic, Any, List, Callable
from abc import ABC, abstractmethod

TEventArgs = TypeVar('TEventArgs')

class EventHandler(Protocol[TEventArgs]):
    def handle(self, sender: Any, args: TEventArgs) -> None:
        ...

class EventArgs:
    pass

class Event(Generic[TEventArgs]):
    def __init__(self) -> None:
        self._handlers: List[EventHandler[TEventArgs]] = []

    def __iadd__(self, handler: EventHandler[TEventArgs]) -> 'Event[TEventArgs]':
        if handler not in self._handlers:
            self._handlers.append(handler)
        return self

    def __isub__(self, handler: EventHandler[TEventArgs]) -> 'Event[TEventArgs]':
        if handler in self._handlers:
            self._handlers.remove(handler)
        return self

    def invoke(self, sender: Any, args: TEventArgs) -> None:
        for handler in self._handlers[:]:
            try:
                handler.handle(sender, args)
            except Exception as ex:
                print(f"Ошибка в обработчике: {ex}")

## !! базовый класс
class ObservableObject:
    def __init__(self) -> None:
        self.property_changing = Event[PropertyChangingEventArgs]()
        self.property_changed = Event[PropertyChangedEventArgs]()
        self._validators: Dict[str, Callable[[Any], bool]] = {}

    def register_validator(self, prop_name: str, validator: Callable[[Any], bool]) -> None:
        self._validators[prop_name] = validator

    def _set_property(self, prop_name: str, value: Any) -> None:
        private_attr = f"_{prop_name}"
        if not hasattr(self, private_attr):
            raise AttributeError(f"Свойство '{prop_name}' не инициализировано в __init__")
        old_value = getattr(self, private_attr)
        if old_value == value:
            return
        args = PropertyChangingEventArgs(prop_name, old_value, value)
        self.property_changing.invoke(self, args)

        if prop_name in self._validators:
            if not self._validators[prop_name](value):
                print(f"Валидация не прошла :( свойство '{prop_name}' отклонено валидатором")
                args.can_change = False

        if not args.can_change:
            return

        setattr(self, private_attr, value)
        self.property_changed.invoke(self, PropertyChangedEventArgs(prop_name))

class PropertyChangedEventArgs(EventArgs):
    def __init__(self, property_name: str) -> None:
        self.property_name = property_name

class PropertyChangingEventArgs(EventArgs):
    def __init__(self, property_name: str, old_value: Any, new_value: Any) -> None:
        self.property_name = property_name
        self.old_value = old_value
        self.new_value = new_value
        self.can_change = True

class PropertyChangedEventHandler:
    def handle(self, sender: Any, args: PropertyChangedEventArgs) -> None:
        print(f"Свойство '{args.property_name}' изменено в {type(sender).__name__}")

class PropertyChangingEventHandler:
    def handle(self, _: Any, args: PropertyChangingEventArgs) -> None:
        print(f"Попытка изменения '{args.property_name}': {args.old_value} -> {args.new_value}")

class Person(ObservableObject):
    def __init__(self, name: str, age: int, email: str) -> None:
        super().__init__()
        self._name = name
        self._age = age
        self._email = email

        ## !! Свои валиадторы
        self.register_validator("name", lambda v: v is not None and str(v).strip() != "")
        self.register_validator("age", lambda v: isinstance(v, int) and v >= 0)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._set_property("name", value)

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        self._set_property("age", value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._set_property("email", value)


class Product(ObservableObject):
    def __init__(self, name: str, price: float, quantity: int) -> None:
        super().__init__()
        self._name = name
        self._price = price
        self._quantity = quantity

        ## !! Свои валиадторы
        self.register_validator("name", lambda v: v is not None and str(v).strip() != "")
        self.register_validator("price", lambda v: isinstance(v, (int, float)) and v >= 0)
        self.register_validator("quantity", lambda v: isinstance(v, int) and v >= 0)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._set_property("name", value)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        self._set_property("price", value)

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        self._set_property("quantity", value)

def main():
    changing_handler = PropertyChangingEventHandler()
    changed_handler = PropertyChangedEventHandler()

    person = Person("Джон", 25, "john@example.com")
    person.property_changing += changing_handler
    person.property_changed += changed_handler

    print("--- Person ---")
    print(f"Инициализация: name={person.name}, age={person.age}, email={person.email}")

    person.name = "Настя"
    print(f"Имя после изменений: {person.name}")

    person.name = ""
    print(f"Имя после неправильных изменений: {person.name}")

    person.age = 22
    print(f"Возраст после изменений: {person.age}")

    person.age = -5
    print(f"Возраст после неправильных изменений: {person.age}")

    product = Product("Плашка оперативы на 16Гб", 20_000_000_000.0, 1)
    product.property_changing += changing_handler
    product.property_changed += changed_handler

    print("\n--- Product ---")
    print(f"Инициалиизация: name={product.name}, price={product.price}, quantity={product.quantity}")

    product.price = 120_000_000_000.0
    product.quantity = 1
    print(f"После изменений: price={product.price}, quantity={product.quantity}")

    product.name = None
    print(f"После неправильных изменений: {product.name}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Ошибка: {e}")
