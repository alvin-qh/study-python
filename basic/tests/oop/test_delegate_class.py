from basic.oop.delegate import Delegate


def test_delegate_class() -> None:
    """测试代理类型"""

    class Class1:
        """定义被代理类型"""

        def run[T: (int, float)](self, a: T, b: T) -> T:
            return a + b

    class Class2:
        """接口实现定义被代理类型类"""

        def run[T: (int, float)](self, a: T, b: T) -> T:
            return a * b

    # 实例化被代理对象
    c1, c2 = Class1(), Class2()

    # 确认被代理对象执行方法的返回值
    assert c1.run(1, 2) == 3
    assert c2.run(1, 2) == 2

    # 创建代理对象
    c1_d = Delegate(c1)
    c2_d = Delegate(c2)

    # 验证代理对象执行被代理方法的返回值
    assert c1_d.run(1, 2) == "Result is: 3"
    assert c2_d.run(1, 2) == "Result is: 2"

    # 验证代理对象可以访问被代理对象的实例
    assert c1_d.instance is c1
    assert c2_d.instance is c2
