from .type_name import schema


def test_define_type_name() -> None:
    query = """
        query {
            song {
                songName
            }
        }
    """

    r = schema.execute(query)
    assert r.errors is None

    assert r.data == {
        "song": {
            "songName": "Hello Song"
        }
    }
