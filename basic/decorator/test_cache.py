from .cache import Cache


class TestCache:
    def setup_method(self) -> None:
        self._cache = Cache()

    def teardown_method(self) -> None:
        self._cache.clear()

    def test_set_get(self) -> None:
        self._cache.set("A", 100)
        assert self._cache.get("A") == 100

    def test_keys_items(self) -> None:
        self._cache.set("A", 100)
        self._cache.set("B", 200)
        assert list(self._cache.keys()) == ["A", "B"]
        assert list(self._cache.items()) == [("A", 100), ("B", 200)]

    def test_delete(self) -> None:
        self._cache.set("A", 100)
        self._cache.delete("A")

        assert self._cache.get("A") is None

    def test_delete_many(self) -> None:
        self._cache.set("-A=", 100)
        self._cache.set("-B=", 200)
        self._cache.delete_many(prefix="-", suffix="=")

        assert self._cache.get("-A=") is None
        assert self._cache.get("-B=") is None

    def test_populate(self) -> None:
        data = {"A": 100, "B": 200}
        self._cache.populate(data)

        assert self._cache.get("A") == 100
        assert self._cache.get("B") == 200


def make_name(prefix: str) -> str:
    pass
