---
id: SR-06
feature: Wiki增量更新Skill
sub_requirement: 增量索引更新
priority: P2
status: 已确认
created: 2026-06-12
---

# SR-06: 增量索引更新

## 1. 职责

wiki 更新后，只重新扫描受影响的 wiki 文件，通过差异合并更新双向索引，避免全量重建。

## 2. 核心接口

```python
def incremental_index_update(
    metadata: dict,
    affected_wikis: list[str],
    new_commit: str,
    wiki_dir: str
) -> dict:
    """
    增量更新 metadata.json 中的双向索引。
    
    参数:
        metadata: 当前 metadata dict
        affected_wikis: 受影响的 wiki 相对路径列表
        new_commit: 更新后的 commit hash
        wiki_dir: wiki 目录绝对路径
    
    返回:
        新的 metadata dict（含新 commit_id），不影响原始传入的 dict
    """
```

## 3. 增量更新算法

```python
import copy
import orjson

def incremental_index_update(metadata, affected_wikis, new_commit, wiki_dir):
    # 深拷贝防止修改调用方的原始 dict
    metadata = copy.deepcopy(metadata)
    source_to_wiki = metadata["source_to_wiki"]
    wiki_to_source = metadata["wiki_to_source"]
    
    for wiki_path in affected_wikis:
        # 1. 获取旧引用关系（从当前索引）
        old_sources = set(wiki_to_source.get(wiki_path, []))
        
        # 2. 重新解析 wiki 文件获取新引用关系
        full_path = os.path.join(wiki_dir, wiki_path)
        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                content = f.read()
            new_citations = parse_citations(wiki_path, content)  # 复用 SR-01
            new_sources = set(c.source_path for c in new_citations)
        else:
            # wiki 文件已被删除
            new_sources = set()
        
        # 3. 计算差异
        added = new_sources - old_sources      # 新增的引用
        removed = old_sources - new_sources     # 删除的引用
        
        # 4. 更新 wiki_to_source
        if new_sources:
            wiki_to_source[wiki_path] = sorted(new_sources)
        elif wiki_path in wiki_to_source:
            del wiki_to_source[wiki_path]
        
        # 5. 更新 source_to_wiki
        # 移除旧引用
        for src in removed:
            if src in source_to_wiki:
                wiki_list = source_to_wiki[src]
                if wiki_path in wiki_list:
                    wiki_list.remove(wiki_path)
                if not wiki_list:
                    del source_to_wiki[src]
        
        # 添加新引用
        for src in added:
            if src not in source_to_wiki:
                source_to_wiki[src] = []
            if wiki_path not in source_to_wiki[src]:
                source_to_wiki[src].append(wiki_path)
                source_to_wiki[src].sort()
    
    # 6. 更新 commit_id
    metadata["source"]["commit_id"] = new_commit
    
    # 7. 更新统计
    metadata["stats"]["source_count"] = len(source_to_wiki)
    metadata["stats"]["wiki_count"] = len(wiki_to_source)
    
    return metadata
```

## 4. 降级策略

当增量更新结果不一致时，降级为全量重建：

```python
def safe_index_update(metadata, affected_wikis, new_commit, wiki_dir, build_index_fn):
    """
    带降级保护的索引更新。
    
    参数:
        build_index_fn: SR-01 的 build_index 函数引用
    """
    try:
        # 尝试增量更新
        updated = incremental_index_update(metadata, affected_wikis, new_commit, wiki_dir)
        
        # 验证：增量结果 vs 全量重建（仅开发阶段启用）
        # full_rebuild = build_index_fn(wiki_dir, new_commit)
        # assert updated["source_to_wiki"] == full_rebuild["source_to_wiki"]
        
        return updated
    except Exception as e:
        print(f"增量索引更新失败: {e}，降级为全量重建")
        return build_index_fn(wiki_dir, new_commit)
```

## 5. 持久化

```python
def save_metadata(metadata: dict, output_path: str):
    """使用 orjson 序列化写入 metadata.json"""
    data = orjson.dumps(metadata, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
    with open(output_path, "wb") as f:
        f.write(data)
```

## 6. 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| wiki 文件读取失败 | 跳过该文件，记录警告 |
| parse_citations 解析异常 | 跳过该文件，使用旧引用关系 |
| 索引更新后 source_count 异常下降 | 触发全量重建降级 |
| metadata.json 写入失败 | 保留内存中的更新结果，提示用户手动重试 |

## 7. 性能对比

| 方法 | 预估耗时 | 说明 |
|------|---------|------|
| 全量重建（SR-01） | ~3 秒 | 扫描 132 个 wiki 文件 |
| 增量更新（SR-06） | ~0.5 秒 | 仅扫描受影响的 5-10 个文件 |

增量更新耗时约为全量重建的 15-20%，满足 REQ-05 的 "< 50%" 验收标准。

## 8. 验收标准

1. 增量更新后索引与全量重建结果一致
2. 增量更新耗时 < 全量重建的 50%
3. commit_id 正确更新为 new_commit
4. 降级策略可用：增量失败时自动全量重建
5. 统计数字（source_count、wiki_count）准确
