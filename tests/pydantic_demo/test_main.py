import json
import shutil
from pathlib import Path
from typing import Generator

import pytest

INPUT = Path(__file__).parent.joinpath("inputs")
OUTPUT = Path(__file__).parent.joinpath("outputs")


class TestMain:
    @pytest.fixture(scope="function", autouse=True)
    def setting(self) -> Generator[None, None, None]:
        print("setup")
        yield
        print("teardown")
        shutil.rmtree(OUTPUT)
        OUTPUT.mkdir(exist_ok=True)
        OUTPUT.joinpath(".gitkeep").touch()

    def test_main_succeeded(self):
        from pydantic_demo.main import main

        input_path = str(INPUT.joinpath("test_main_succeeded.json"))
        argv = ["--input-path", input_path, "--output-path", str(OUTPUT)]
        actual = main(argv)
        assert actual == 0

        actual_file = next(OUTPUT.glob("*.json"))
        assert actual_file

        with open(actual_file) as f:
            s = f.read()
            actual_contents = json.loads(s)
            actual_contents["user_id"] = "*****"
        assert actual_contents == {
            "user_detail": {"name": "taro", "age": 20, "email": "abc@testmail.com"},
            "created_at": "2023-01-01T00:00:00.123Z",
            "updated_at": "2023-01-02T23:59:59.999Z",
            "user_id": "*****",
        }
