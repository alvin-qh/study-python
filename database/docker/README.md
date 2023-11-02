# 测试镜像容器

测试镜像容器中包含了多个数据库容器实例, 参见: [docker-compose.yml](./docker-compose.yml) 文件中的定义

## 1. Percona 容器

## 2. MongoDB 容器

为了能使用 MongoDB 的事务功能, MongoDB 容器是以单机集群的方式启动的 (单节点副本), 具体方式如下:

1. 在 [docker-compose.yml](./docker-compose.yml) 文件的 `mongo` 配置中设置了 `command` 项, 为 mongo 启动增加了 `--replSet rs0` 命令行参数, 表示加入集群 `rs0`;

   ```yaml
   mongo:
     ...
     command: --replSet rs0
   ```

2. 在容器第一次启动成功后, 执行如下命令初始化集群:

   ```bash
   docker exec -it mongo mongosh "mongodb://mongo:27017?replicaSet=rs0&directConnection=true" --eval '
      config = {
          "_id": "rs0",
          "members": [
          {
              "_id": 0,
              "host": "mongo:27017"
          }
          ]
      };
      rs.initiate();
      rs.status();
   '
   ```

3. 一旦开启集群模式, 则无法直接为 mongo 设置用户名和密码, 即启用 [env/mongo.env](./env/mongo.env) 中的环境变量会导致 mongo 无法正常启动, 需要设置 Key 文件 (参见: <https://www.mongodb.com/docs/manual/tutorial/enforce-keyfile-access-control-in-existing-replica-set/> 中的介绍). 并在 [docker-compose.yml](./docker-compose.yml) 中为启动命令增加 `--keyFile` 参数

   ```yaml
   mongo:
     ...
     command: --replSet rs0 --keyFile <path-to-keyfile>
   ```
