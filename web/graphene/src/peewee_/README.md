# Peewee with PostgreSQL

## 1. 按照数据库驱动

Peewee 要求使用 `psycopg2` 作为驱动, 但某些系统上无法直接通过 Python 安装此驱动, 原因是所需的依赖库未安装, 导致无法正确编译 `psycopg2` 依赖库

解决此问题有如下几种方法

1. 安装 `psycopg2-binary`, 即编译好的 `psycopg2` 二进制分发包, 这个包为大部分 macOS 和 Linux 提供了 `wheels` 文件, 但仍会出现系统不兼容的清空

   ```bash
   pdm add psycopg2-binary
   ```

2. 安装 `psycopg2` 编译的依赖库, 这样就可以正确编译

   ```bash
   sudo apt install libpq-dev python3-dev
   ```

   对于 CentOS, 可以安装如下依赖库

   ```bash
   sudo yum install python-devel postgresql-devel
   ```

3. 也可以安装全量的编译环境

   ```bash
   sudo apt install build-essential
   ```

   或者

   ```bash
   sudo apt install postgresql-server-dev-all
   ```
