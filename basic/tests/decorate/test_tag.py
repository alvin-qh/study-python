from basic.decorate.tag import HtmlTag, html_tag, tag


def test_tag_decorator() -> None:
    """
    演示最基本的装饰器用法

    通过 `tag` 函数对 `demo` 函数进行装饰
    """

    @tag
    def demo() -> str:
        """
        被装饰函数, 其返回值会被代理函数放在一个 json 字符串中
        """
        return "demo worked"

    # 验证装饰器是否起效
    assert demo() == '{"wrapped": true, "result": "demo worked"}'


def test_html_tag_decorator() -> None:
    """
    演示通过闭包创建装饰器函数
    """

    @html_tag(tag_name="div", style="display:block", clazz="col-md-2")
    def demo1() -> str:
        return "Hello"

    @html_tag(tag_name="div", click="alter('ok')")
    def demo2() -> str:
        return ""

    assert demo1() == '<div class="col-md-2" style="display:block">Hello</div>'
    assert demo2() == "<div click=\"alter('ok')\"/>"


def test_html_tag_class_decorator() -> None:
    """
    演示通过仿函数类对象创建装饰器函数

    Returns:
        _type_: _description_
    """

    @HtmlTag(tag_name="div", style="display:block", clazz="col-md-2")
    def demo1() -> str:
        return "Hello"

    @HtmlTag(tag_name="div", click="alter('ok')")
    def demo2() -> str:
        return ""

    assert demo1() == '<div class="col-md-2" style="display:block">Hello</div>'
    assert demo2() == "<div click=\"alter('ok')\"/>"
