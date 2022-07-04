from .mutation import schema


def test_create_person1() -> None:
    query = """
        mutation($name: String!, $age: Int!) {
            __typename
            name
            age
        }
    """

    r = schema.execute(query)
    assert r.errors is None
