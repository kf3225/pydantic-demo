import json
import sys
import traceback
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import UUID4, BaseModel, DirectoryPath, EmailStr, Field, FilePath, PositiveInt, ValidationError
from pydantic_core import to_json


class BaseModelGenerator(BaseModel):
    @property
    def filename(self) -> str:
        raise NotImplementedError()

    def output(self, output_path: Path) -> bool:
        with open(output_path, mode="w", encoding="utf-8") as f:
            f.write(to_json(self, indent=2).decode())


class UserDetail(BaseModelGenerator):
    name: str
    age: PositiveInt
    email: EmailStr


class UserInfo(BaseModelGenerator):
    user_detail: UserDetail
    created_at: datetime
    updated_at: datetime | None
    user_id: UUID4 = Field(default_factory=lambda: uuid4())

    @property
    def filename(self) -> str:
        return str(self.user_id) + ".json"


class ScriptArgument(BaseModelGenerator):
    input_path: FilePath
    output_path: DirectoryPath


def parsed_args(argv: list[str]) -> ScriptArgument:
    parser = ArgumentParser()
    parser.add_argument("--input-path", dest="input_path", type=str, required=True)
    parser.add_argument("--output-path", dest="output_path", type=str, required=True)
    args = vars(parser.parse_args(argv))
    return ScriptArgument.model_validate(args)


def load_json(input_path: Path) -> dict[str, Any]:
    with open(input_path) as f:
        contents = json.loads(f.read())
    return contents


def main(argv: list[str]) -> int:
    try:
        args = parsed_args(argv)
        json_contents = load_json(args.input_path)
        user = UserInfo.model_validate(json_contents)

        user.output(output_path=args.output_path.joinpath(user.filename))
        return 0
    except ValidationError:
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
