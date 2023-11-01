from pytest import mark
from relay.mutation import schema


@mark.asyncio
async def test_client_id_mutation() -> None:
    query = """
        mutation($shipInput: IntroduceShipMutationInput!) {
            introduceShip(input: $shipInput) {
                ship {
                    id
                    name
                    faction {
                        id
                        name
                    }
                }
                faction {
                    id
                    name
                }
            }
        }
    """

    args = {
        "shipInput": {"shipName": "Millennium Falcon", "factionId": "rebel_alliance"}
    }
    result = schema.execute(query, variables=args)

    assert result.errors is None
    assert result.data is not None
    assert result.data == {
        "introduceShip": {
            "faction": {
                "id": "rebel_alliance",
                "name": "Rebel Alliance",
            },
            "ship": {
                "faction": {
                    "id": "rebel_alliance",
                    "name": "Rebel Alliance",
                },
                "id": "1",
                "name": "Millennium Falcon",
            },
        }
    }

    query = """
        query($id: ID!) {
            ship(id: $id) {
                id
                name
                faction {
                    id
                    name
                }
            }
        }
    """

    args = {"id": 1}
    result = schema.execute(query, variables=args)

    assert result.errors is None
    assert result.data is not None
    assert result.data == {
        "ship": {
            "id": "1",
            "name": "Millennium Falcon",
            "faction": {
                "id": "rebel_alliance",
                "name": "Rebel Alliance",
            },
        }
    }
