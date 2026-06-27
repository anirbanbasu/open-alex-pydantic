from open_alex_pydantic import hello


def test_hello_returns_expected_message() -> None:
    assert hello() == "Hello from open-alex-pydantic!"
