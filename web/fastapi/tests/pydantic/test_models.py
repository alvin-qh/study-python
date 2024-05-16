from datetime import UTC, datetime

from pydantic_.models import Org
from pytest_mock import MockerFixture


def test_org_to_json(mocker: MockerFixture) -> None:
    with mocker.patch("datetime.datetime.now") as mocked_now:
        org = Org(
            id=1001,
            name="Alvin",
            created_by=1001,
            created_at=datetime.now(UTC),
            updated_by=1001,
            updated_at=datetime.now(UTC),
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
