import os
from dataclasses import dataclass
from typing import Any, Type, cast

from dotenv import load_dotenv


@dataclass
class Config:
    TOKEN: str
    DEV_GUILD: int | None

    def __post_init__(self) -> None:
        load_dotenv()

        for field in self.__dataclass_fields__.values():
            field_name: str = field.name
            field_type: Type = field.type

            setattr(self, field_name, self._get_env_value(field_name, field_type))

    def _get_env_value(self, field_name: str, field_type: Type) -> Any:
        env_value: str = os.getenv(field_name)

        return cast(field_type, env_value)
