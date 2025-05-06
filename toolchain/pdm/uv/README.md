# 集成 PDM 和 UV

可以将 UV 和 PDM 继承在一起, 发挥 PDM 的丰富功能和 UV 的高性能

首先, 通过 PDM 正常创建一个项目

```bash
pdm init
```

其次, 启用 PDM 的 UV 集成

```bash
pdm config --local use_uv true
```

注意: 一旦当前项目集成了 UV 工具, 则当前项目所引用的本地库必须符合如下要求之一:

- 本地库项目需要通过 UV 创建;
- 本地库项目需要通过集成了 UV 工具的的 PDM 创建;
