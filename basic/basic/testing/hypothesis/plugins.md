# pytest 运行插件

Hypothesis 包含一个插件来改进与 pytest 的集成，它是默认激活的(但不影响其他测试插件)。它的目的是通过提供额外的信息和方便的配置选项来改进 Hypothesis 和 pytest 之间的集成。

- `pytest --hypothesis-show-statistics` 可用于显示测试和数据生成的统计

- `pytest --hypothesis-profile=<profile name>` 加载通过 `settings.register_profile` 函数设置的配置文件名称

- `pytest --hypothesis-verbosity=<level name>` 设置测试日志输出的详细程度，参考 `settings(verbosity=...)` 配置项

- `pytest --hypothesis-seed=<an int>` 设置特殊的种子用于产生失败的测试用例

- `pytest --hypothesis-explain` 在输出中包含对每个用例生成阶段的解释性日志

所有以 Hypothesis 定义的测试都自动加上 `@pytest.mark.hypothesis` 装饰器
