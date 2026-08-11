分布式缓存与分布式锁工具集，封装 Redis 单例客户端、常用缓存操作（Hash/Set/List）及基于 Django cache 的分布式锁装饰器。

单例 Redis 客户端，支持从 settings 初始化。
- 符号: `RedisClient(Singleton)` / `RedisClient.from_envs(prefix, prefer_type)`
- 位置: `src/bk_monitor_base/metadata/utils/redis_client.py`
- 说明:
  - `from_envs()`: 从环境变量创建 Redis 连接
  - 支持 sentinel（哨兵）和 standalone 模式
  - 哨兵模式下自动发现 master，随机节点顺序

静态工具类，封装常用 Redis 操作。
- 符号: `RedisTools`
- 位置: `src/bk_monitor_base/metadata/utils/redis_tools.py`
- 方法:
  - `push_and_publish_spaces(key, channel, space)`: 推送并发布空间变更
  - `push_space_to_redis(key, space)`: sadd 推送空间
  - `publish(channel, msg_list)`: 发布消息
  - `hset_to_redis(key, field, value)`: Hash 单字段写入
  - `hmset_to_redis(key, field_value)`: Hash 批量写入
  - `hget` / `hmget` / `hgetall` / `hkeys` / `hdel`: Hash 读取/删除
  - `sadd` / `smembers` / `srem`: Set 操作
  - `get_list(key)`: get + JSON 反序列化
  - 自动通过 `setup_client()` 初始化（兼容异常）

独立的 bkbase Redis 连接创建。
- 符号: `bkbase_redis_client()`
- 位置: `src/bk_monitor_base/metadata/utils/redis_tools.py`

基于 Django cache 的分布式锁装饰器。
- 符号: `share_lock(ttl=600, identify=None)`
- 位置: `src/bk_monitor_base/metadata/utils/lock.py`
- 说明:
  - 使用 `set(key, token, nx=True)` 原子获取锁
  - 识别同名函数通过 `identify` 自定义 cache_key
  - 必须放在 `@periodic_task` 下方
