# 数据库表结构与关联关系

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

## 关联关系说明

- **作者与笔记、笔记详情关联：**  
  - **xhs_notes** 和 **xhs_note_details** 均包含字段 `auther_user_id`，用于关联 **xhs_authers** 表，从而确定每个笔记或详细内容的作者。

- **笔记与评论关联：**  
  - **xhs_comments** 表中通过 `note_id` 指定了所属的笔记；同时，通过 `parent_comment_id` 实现评论与回复（子评论）的层级关系。

- **评论与 @ 用户关联：**  
  - **xhs_comment_at_users** 表通过 `comment_id` 与 **xhs_comments** 建立关联，用于记录在某评论中被 @ 的所有用户信息。

- **关键词群与笔记关联：**  
  - 关键词群信息存储在 **xhs_keyword_groups** 中；而 **xhs_keyword_group_notes** 表则将关键词群（group_id）和笔记（note_id）关联起来，实现多对多关系，从而记录“某个关键词群查询到的帖子”这一关系。
