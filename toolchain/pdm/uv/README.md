# 集成 PDM 和 UV

可以将 UV 和 PDM 继承在一起, 发挥 PDM 的丰富功能和 UV 的高性能

首先, 通过 PDM 正常创建一个项目

其次, 启用 PDM 的 UV 集成

```bash
pdm config --local use_uv true
```

此时, 会在当前项目下创建 `pdm.toml` 文件, 其内容包括:

```toml
use_uv = true
```

> 如果命令中缺省了 `--local` 参数, 则配置文件会写入到当前用户目录下 `.pdm/config.toml` 文件中, 表示全局配置, 不建议使用

注意: 一旦当前项目集成了 UV 工具, 则当前项目所引用的本地库必须符合如下要求之一:

- 本地库项目需要通过 UV 创建;
- 本地库项目需要通过集成了 UV 工具的的 PDM 创建;
