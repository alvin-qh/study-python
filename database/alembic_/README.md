# Alembic

## 1. 配置

### 1.1. 相关 Python 包

```plaintext
PyMySql
alembic
SQLAlchemy
```

### 1.2. 初始化

指定目录，生成 Alembic 配置内容

```bash
$ alembic init <dir>
```

上述命令会在目标目录中的 `scripts` 目录下，创建如下内容

```plaintext
versions        <dir>   存放数据库脚本
alembic.ini     <file>  存放 Alembic 配置
env.py          <file>  存放 Alembic 环境变量
script.py.mako  <file>  存放数据库脚本模板
```

编辑 `alembic.ini` 文件, 修改 `script_location` 配置，确保指向 `scripts` 目录。

编辑 `alembic.ini` 文件, 设置数据库连接地址如下:

```ini
sqlalchemy.url = mysql+pymysql://<user>:<password>:@localhost/<database>
```

如果非要使用其它 `.ini` 文件，则需要通过 `-c` 选项指定:

```bash
$ alembic -c test.ini upgrade head
```

## 2. 使用

将数据库更新/恢复到指定版本的脚本

```bash
$ alembic upgrade <Revision ID>
$ alembic downgrade <Revision ID>
```

将数据库更新到最新版本

```bash
$ alembic upgrade head
```

将数据库恢复到最初版本

```bash
$ alembic downgrade base
```

查看数据库的当前版本

```bash
$ alembic current
```

查看数据库的更新历史

```bash
$ alembic history
```
