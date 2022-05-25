import timeit

from pytest import raises

from .cache import Cache, memo


class TestCache:
    """
    测试 Cache 类
    """

    def setup_method(self) -> None:
        """
        每个测试开始前, 生成缓存对象
        """
        self._cache = Cache()

    def teardown_method(self) -> None:
        """
        每个测试结束后, 清空缓存内容
        """
        self._cache.clear()

    def test_set_get(self) -> None:
        """
        测试设置缓存和获取缓存内容
        """
        # 通过 Key 设置一个缓存
        self._cache.set("A", 100)
        # 根据 Key 获取设置的缓存内容
        assert self._cache.get("A") == 100

    def test_keys_items(self) -> None:
        """
        测试获取缓存中所有的 Key 值以及所有的缓存项
        """
        self._cache.set("A", 100)
        self._cache.set("B", 200)

        # 获取缓存中所有的 Key 值列表
        assert list(self._cache.keys()) == ["A", "B"]
        # 获取所有的缓存项, 是一个 Key/Value 的二元组
        assert list(self._cache.items()) == [("A", 100), ("B", 200)]

    def test_delete(self) -> None:
        """
        测试删除一个已有 Key
        """
        self._cache.set("A", 100)

        # 删除已有的 Key
        self._cache.delete("A")
        assert self._cache.get("A") is None

    def test_delete_many(self) -> None:
        """
        根据所给的前缀和后缀删除对应的 Key
        """
        self._cache.set("-A=", 100)
        self._cache.set("-B=", 200)

        # 根据所给的前缀和后缀删除对应的 Key
        self._cache.delete_many(prefix="-", suffix="=")
        assert self._cache.get("-A=") is None
        assert self._cache.get("-B=") is None

    def test_populate(self) -> None:
        """
        通过一个 Dict[str, Any] 对象设置缓存内容
        """
        # Dict 对象
        data = {"A": 100, "B": 200}

        # 通过 Dict 对象设置缓存内容
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

    def test_memo(self) -> None:
        """
        测试函数缓存

        计算斐波那契数列第 100 项

        计算通过递归进行, 且递归层次比较深, 所以不通过缓存会经过漫长的执行时间. 通过添加缓存, 可以
        避免深度递归 (每次递归的结果会被缓存), 在很快的时间内计算完毕
        """
        @memo("fib({n})")  # 以 fib 和参数 n 作为 Key 记录缓存
        def fib(n: int) -> int:
            """
            计算第 n 项斐波那契数列

            通过增加 `fib({n})` 缓存, 每个数列项只需计算一次, 避免深度递归

            Args:
                n (int): 表示要计算第 n 项斐波那契数列值

            Returns:
                int: 第 n 项斐波那契数列值
            """
            if n < 2:
                return n

            return fib(n - 1) + fib(n - 2)

        # 记录起始时间
        start = timeit.default_timer()

        # 计算第 100 项数列值
        r = fib(100)

        # 确认数列值结果
        assert r == 354224848179261915075

        # 确认计算时间
        assert 0 < timeit.default_timer() - start < 3
