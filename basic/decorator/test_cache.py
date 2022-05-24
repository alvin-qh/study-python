from pytest import raises

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


class TestMemoCache:
    def setup_method(self) -> None:
        from .cache import _cache
        _cache.clear()

    def test_check_duplicated_cache_key(self) -> None:
        from .cache import _check_duplicated_cache_key

        _check_duplicated_cache_key("demo1()")
        with raises(KeyError):
            _check_duplicated_cache_key("demo1()")

        _check_duplicated_cache_key("demo2_{a}_{b}")
        with raises(KeyError):
            _check_duplicated_cache_key("demo2_{a}_{b}")

    def test_get_default_args(self) -> None:
        from .cache import _get_default_args

        def demo1() -> None:
            pass

        d = _get_default_args(demo1)
        assert d == {}

        def demo2(a: int = 1, b: int = 2) -> None:
            pass

        d = _get_default_args(demo2)
        assert d == {"a": 1, "b": 2}

    def test_interpolate_str_by_function(self) -> None:
        from .cache import _interpolate_str

        def demo(a: int, b: str, c: bool = False) -> None:
            pass

        s = _interpolate_str(
            "demo_{a}_{b}_{c}",
            demo,
            None,
            (1, "A", True),
            {},
        )
        assert s == "demo_1_A_True"

        s = _interpolate_str(
            "demo_{a}_{b}_{c}",
            demo,
            None,
            (),
            {
                "a": 1,
                "b": "A",
                "c": True,
            }
        )
        assert s == "demo_1_A_True"

    def test_interpolate_str_by_method(self) -> None:
        from .cache import _interpolate_str

        class Demo:
            name = "Demo"

            def demo(self, a: int, b: str, c: bool = False) -> None:
                pass

        d = Demo()

        s = _interpolate_str(
            "demo_{self.name}_{a}_{b}_{c}",
            d.demo,
            d,
            (1, "A", True),
            {},
        )
        assert s == "demo_Demo_1_A_True"

        s = _interpolate_str(
            "demo_{self.name}_{a}_{b}_{c}",
            d.demo,
            d,
            (),
            {
                "a": 1,
                "b": "A",
                "c": True,
            }
        )
        assert s == "demo_Demo_1_A_True"
