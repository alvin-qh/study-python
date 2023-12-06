from pydantic_.models import Org


def test_org_to_json() -> None:
    org = Org(
        id=1001,
        name="Alvin",
    )

    assert org.model_dump() == dict(org) == {"id": 1001, "name": "Alvin"}
    assert org.model_dump_json() == '{"id":1001,"name":"Alvin"}'


def test_org_from_json() -> None:
    org = Org(**{"id": 1001, "name": "Alvin"})
    assert org.id == 1001
    assert org.name == "Alvin"

    org = Org.model_validate({"id": 1001, "name": "Alvin"})
    assert org.id == 1001
    assert org.name == "Alvin"

    org = Org.model_validate_json('{"id":1001,"name":"Alvin"}')
    assert org.id == 1001
    assert org.name == "Alvin"
