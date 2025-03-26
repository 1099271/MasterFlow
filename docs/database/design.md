# 数据库设计文档

## 概述

MasterFlow 系统的数据库设计专注于小红书数据的收集、分析与处理。整个数据库设计基于关系型数据库（MySQL），采用了规范化设计原则，确保数据的完整性和查询效率。

## 数据库表结构与关联关系

下面整理了一份表格，概述了所有生成的表、各自的作用以及它们之间的关联关系。

| 表名                        | 作用说明                                                         | 主要字段（主键/关键字段）                                                                                                            | 表之间的关联关系                                                    |
| --------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **xhs_authers**             | 存储小红书作者（auther）的详细信息                                | auther_user_id (PK), auther_home_page_url, auther_avatar, auther_nick_name, auther_desc, auther_interaction 等                      | 被 **xhs_notes** 和 **xhs_note_details** 通过 auther_user_id 引用      |
| **xhs_notes**               | 存储从关键词或作者接口中获取的笔记摘要（帖子）信息                  | note_id (PK), note_url, note_xsec_token, note_cover_url_pre, note_cover_url_default, note_display_title, note_liked_count, auther_user_id (FK) | 引用 **xhs_authers**（auther_user_id）；与 **xhs_note_details** 通过 note_id 关联；与 **xhs_comments** 通过 note_id 关联；通过 **xhs_keyword_group_notes** 建立与关键词群的关联 |
| **xhs_note_details**        | 存储单个笔记的详细内容（如描述、图片列表、评论数、视频信息等）         | note_id (PK), note_last_update_time, note_create_time, note_desc, comment_count, note_image_list, note_tags 等, auther_user_id (FK)    | 引用 **xhs_authers**（auther_user_id）；与 **xhs_notes** 通过 note_id 对应     |
| **xhs_comments**            | 存储某个笔记下的所有评论及其回复（采用扁平化设计，通过 parent_comment_id 表示层级） | comment_id (PK), note_id, parent_comment_id, comment_user_id, comment_content, comment_like_count, comment_create_time 等                 | 每条评论通过 note_id 关联到 **xhs_notes**；子评论通过 parent_comment_id 与父评论关联；评论中出现 @ 用户的信息由 **xhs_comment_at_users** 记录 |
| **xhs_comment_at_users**    | 存储评论中出现的 @ 用户信息（可能一个评论包含多个 @ 用户）             | id (PK), comment_id (FK), at_user_id, at_user_nickname, at_user_home_page_url                                                         | 通过 comment_id 与 **xhs_comments** 建立关联                         |
| **xhs_keyword_groups**      | 存储关键词群信息，记录一个关键词群包含哪些关键词                      | group_id (PK), group_name, keywords (JSON 数组), created_at                                                                            | 与 **xhs_keyword_group_notes** 通过 group_id 关联                      |
| **xhs_keyword_group_notes** | 记录关键词群与笔记之间的多对多关联（即某个关键词群查询到了哪些笔记）     | id (PK), group_id (FK), note_id (FK), retrieved_at                                                                                    | group_id 关联 **xhs_keyword_groups**，note_id 关联 **xhs_notes**       |
| **xhs_topic_discussions**   | 存储小红书话题讨论量记录                                          | id (PK), topic_name, topic_type, view_num, smart, record_date                                                                      | 独立表，用于统计分析                                               |
| **llm_note_diagnosis**      | 存储大模型对笔记的分析诊断结果                                    | id (PK), note_id (FK), llm_name, diagnosis_data (JSON), created_at                                                                | 通过 note_id 与 **xhs_notes** 关联                                  |
| **user**                    | 存储系统用户信息                                                 | id (PK), username, email, hashed_password, is_active                                                                             | 系统用户表                                                         |
| **item**                    | 存储系统中的各类项目                                              | id (PK), title, description, owner_id (FK)                                                                                       | 通过 owner_id 与 **user** 表关联                                   |

## 关联关系说明

### 1. 作者与笔记、笔记详情关联

- **xhs_notes** 和 **xhs_note_details** 均包含字段 `auther_user_id`，用于关联 **xhs_authers** 表
- 这样可以通过作者快速查找其所有笔记，也可以从笔记或笔记详情追溯到作者信息
- 注意：笔记表中冗余存储了部分作者信息（如昵称、头像URL等），以减少频繁的表连接操作

### 2. 笔记与笔记详情关联

- **xhs_note_details** 以 `note_id` 为主键，与 **xhs_notes** 表形成一对一关系
- 笔记表存储基本信息，详情表存储完整内容（如正文描述、图片列表、视频URL等）
- 这种分离设计可以提高查询效率，因为大多数列表场景只需查询基本信息

### 3. 笔记与评论关联

- **xhs_comments** 表通过 `note_id` 字段关联到 **xhs_notes** 表
- 同时，通过 `parent_comment_id` 实现评论的层级关系（回复关系）
- 采用扁平化存储而非递归结构，便于查询和展示

### 4. 评论与 @ 用户关联

- **xhs_comment_at_users** 表通过 `comment_id` 与 **xhs_comments** 建立关联
- 一条评论可能 @ 多个用户，因此设计为一对多关系
- 存储被 @ 用户的ID、昵称和主页URL等信息

### 5. 关键词群与笔记关联

- **xhs_keyword_groups** 存储关键词群组信息
- **xhs_keyword_group_notes** 作为中间表，建立关键词群与笔记之间的多对多关系
- 通过这种设计，可以记录并分析某个关键词群所检索到的所有笔记

### 6. 大模型诊断与笔记关联

- **llm_note_diagnosis** 表存储大语言模型对笔记的分析结果
- 通过 `note_id` 关联到笔记，记录不同模型的分析诊断结果
- 诊断数据以JSON格式存储，便于存储复杂的结构化信息

## 数据库索引设计

为提高查询性能，系统在以下字段上建立了索引：

1. 所有主键（Primary Key）
2. 所有外键（Foreign Key）
3. 常用查询条件字段：
   - xhs_notes.note_display_title
   - xhs_authers.auther_nick_name
   - xhs_comments.comment_create_time
   - xhs_note_details.note_create_time

## 数据库关系图

```
+--------------+       +-------------+       +----------------+
| xhs_authers  |<------| xhs_notes   |<------| xhs_comments   |
+--------------+       +-------------+       +----------------+
       ^                    ^    ^                  ^
       |                    |    |                  |
       |                    |    |                  |
+----------------+          |    |         +---------------------+
| xhs_note_details|<---------    |         | xhs_comment_at_users|
+----------------+               |         +---------------------+
                                 |
                     +----------------------+       +------------------+
                     | xhs_keyword_group_notes|<-----| xhs_keyword_groups|
                     +----------------------+       +------------------+
```

## 数据类型与约束

1. **字符串字段**：
   - 用户ID、笔记ID等使用 VARCHAR(64)
   - URL类型字段使用 VARCHAR(255)
   - 较长文本内容使用 TEXT 类型

2. **JSON字段**：
   - 对于复杂结构数据（如标签列表、图片列表）使用 JSON 类型存储
   - 便于存储和查询半结构化数据

3. **时间字段**：
   - 均使用 DATETIME 类型
   - 创建和更新时间通过默认值和触发器自动维护

4. **外键约束**：
   - 所有关联关系都通过外键约束保证数据完整性
   - 删除笔记时，相关的评论、详情等通过级联删除保持一致性

## 数据量估计与扩展性

- 假设每日新增笔记数：10,000条
- 平均每条笔记评论数：50条
- 年增长数据量：约10GB

为应对未来可能的数据增长，建议：
1. 实施表分区策略（如按时间分区）
2. 考虑冷热数据分离存储
3. 针对大表实施分库分表策略

## 数据备份策略

1. 每日全量备份
2. 每小时增量备份
3. 备份文件异地存储
4. 定期进行恢复测试
