from pathlib import Path


def get_testdata_file(filename: str) -> Path:
    return Path(__file__).parent / "test_data" / filename


def get_testdata_text(filename: str) -> str:
    return get_testdata_file(filename).read_text("utf-8")


def get_testdata_binary(filename: str) -> bytes:
    return get_testdata_file(filename).read_bytes()
