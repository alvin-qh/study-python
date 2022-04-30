# 数据库访问

## 1. MySQL 数据库

进入 `../docker/mysql`，执行

```bash
$ docker-compose up -d
```

在 docker 容器内启动 `mysql-client`

```bash
$ docker exec -it percona mysql -uroot -p
```

创建演示数据库

```sql
mysql> CREATE DATABASE `study_python` DEFAULT CHARSET=utf8mb4;
```

删除演示数据库

```sql
mysql> DROP DATABASE `study_python`
```

## 2. 使用 Alembic

执行升级脚本

```bash
$ alembic upgrade head
```

执行降级脚本

```bash
$ alembic downgrade base
```
