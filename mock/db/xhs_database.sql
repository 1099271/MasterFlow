-- 小红书笔记摘要信息表
CREATE TABLE `xhs_notes` (
  `note_id` VARCHAR(64) NOT NULL COMMENT '笔记唯一标识',
  `note_url` VARCHAR(255) NOT NULL COMMENT '笔记详情页面 URL',
  `note_xsec_token` VARCHAR(255) DEFAULT NULL COMMENT '笔记鉴权 token',
  `note_cover_url_pre` VARCHAR(255) DEFAULT NULL COMMENT '笔记封面预览图 URL',
  `note_cover_url_default` VARCHAR(255) DEFAULT NULL COMMENT '笔记默认封面图 URL',
  `note_cover_width` INT UNSIGNED DEFAULT NULL COMMENT '封面图片宽度（像素）',
  `note_cover_height` INT UNSIGNED DEFAULT NULL COMMENT '封面图片高度（像素）',
  `note_display_title` VARCHAR(255) DEFAULT NULL COMMENT '笔记展示标题',
  `note_model_type` VARCHAR(32) DEFAULT NULL COMMENT '笔记模型类型',
  `note_card_type` VARCHAR(32) DEFAULT NULL COMMENT '笔记卡片类型',
  `note_liked` TINYINT(1) DEFAULT 0 COMMENT '是否已点赞（0:未点赞, 1:已点赞）',
  `note_liked_count` INT UNSIGNED DEFAULT 0 COMMENT '点赞数量',
  `note_sticky` TINYINT(1) DEFAULT 0 COMMENT '是否置顶（0:否, 1:是）',
  `auther_user_id` VARCHAR(64) NOT NULL COMMENT '作者唯一标识，关联 xhs_authers 表',
  `auther_home_page_url` VARCHAR(255) DEFAULT NULL COMMENT '作者主页 URL（冗余字段）',
  `auther_avatar` VARCHAR(255) DEFAULT NULL COMMENT '作者头像 URL（冗余字段）',
  `auther_nick_name` VARCHAR(128) DEFAULT NULL COMMENT '作者昵称（冗余字段）',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`note_id`),
  KEY `idx_auther_user_id` (`auther_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小红书笔记摘要信息表';


-- 小红书笔记详情表
CREATE TABLE `xhs_note_details` (
  `note_id` VARCHAR(64) NOT NULL COMMENT '笔记唯一标识，与 xhs_notes 对应',
  `note_url` VARCHAR(255) NOT NULL COMMENT '笔记详情页面 URL',
  `note_last_update_time` DATETIME DEFAULT NULL COMMENT '笔记最后更新时间',
  `note_create_time` DATETIME DEFAULT NULL COMMENT '笔记创建时间',
  `note_model_type` VARCHAR(32) DEFAULT NULL COMMENT '笔记模型类型',
  `note_card_type` VARCHAR(32) DEFAULT NULL COMMENT '笔记卡片类型',
  `note_display_title` VARCHAR(255) DEFAULT NULL COMMENT '笔记展示标题',
  `note_desc` TEXT COMMENT '笔记描述内容（包含话题及文本描述）',
  `comment_count` INT UNSIGNED DEFAULT 0 COMMENT '评论数量',
  `note_liked_count` INT UNSIGNED DEFAULT 0 COMMENT '点赞数量',
  `share_count` INT UNSIGNED DEFAULT 0 COMMENT '分享数量',
  `collected_count` INT UNSIGNED DEFAULT 0 COMMENT '收藏数量',
  `video_id` VARCHAR(64) DEFAULT NULL COMMENT '视频标识（如存在）',
  `video_h266_url` VARCHAR(255) DEFAULT NULL COMMENT '视频 H266 URL',
  `video_a1_url` VARCHAR(255) DEFAULT NULL COMMENT '视频 a1 URL',
  `video_h264_url` VARCHAR(255) DEFAULT NULL COMMENT '视频 H264 URL',
  `video_h265_url` VARCHAR(255) DEFAULT NULL COMMENT '视频 H265 URL',
  `note_duration` INT UNSIGNED DEFAULT NULL COMMENT '视频时长（秒）',
  `note_image_list` JSON DEFAULT NULL COMMENT '笔记图片列表（JSON 数组）',
  `note_tags` JSON DEFAULT NULL COMMENT '笔记标签数组（JSON 数组）',
  `note_liked` TINYINT(1) DEFAULT 0 COMMENT '是否已点赞（0:未点赞, 1:已点赞）',
  `collected` TINYINT(1) DEFAULT 0 COMMENT '是否已收藏（0:未收藏, 1:已收藏）',
  `auther_user_id` VARCHAR(64) NOT NULL COMMENT '作者唯一标识，关联 xhs_authers 表',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`note_id`),
  KEY `idx_auther_user_id` (`auther_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小红书笔记详情表';


-- 小红书作者信息表
CREATE TABLE `xhs_authers` (
  `auther_user_id` VARCHAR(64) NOT NULL COMMENT '作者唯一标识',
  `auther_home_page_url` VARCHAR(255) DEFAULT NULL COMMENT '作者主页 URL',
  `auther_avatar` VARCHAR(255) DEFAULT NULL COMMENT '作者头像 URL',
  `auther_nick_name` VARCHAR(128) DEFAULT NULL COMMENT '作者昵称',
  `auther_desc` TEXT COMMENT '作者简介',
  `auther_interaction` INT UNSIGNED DEFAULT 0 COMMENT '互动数',
  `auther_ip_location` VARCHAR(64) DEFAULT NULL COMMENT '作者所在地',
  `auther_red_id` VARCHAR(64) DEFAULT NULL COMMENT '红书 ID',
  `auther_tags` JSON DEFAULT NULL COMMENT '作者标签数组（JSON 格式）',
  `auther_fans` INT UNSIGNED DEFAULT 0 COMMENT '粉丝数量',
  `auther_follows` INT UNSIGNED DEFAULT 0 COMMENT '关注数量',
  `auther_gender` VARCHAR(16) DEFAULT NULL COMMENT '作者性别',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`auther_user_id`),
  UNIQUE KEY `uk_auther_red_id` (`auther_red_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小红书作者信息表';


-- 小红书评论@用户信息表
CREATE TABLE `xhs_comment_at_users` (
  `id` BIGINT AUTO_INCREMENT NOT NULL COMMENT '自增主键',
  `comment_id` VARCHAR(64) NOT NULL COMMENT '关联的评论ID，关联 xhs_comments(comment_id)',
  `at_user_id` VARCHAR(64) NOT NULL COMMENT '被@的用户ID',
  `at_user_nickname` VARCHAR(128) DEFAULT NULL COMMENT '被@的用户昵称',
  `at_user_home_page_url` VARCHAR(255) DEFAULT NULL COMMENT '被@用户主页 URL',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_comment_id` (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小红书评论@用户信息表，用于存储评论中@的用户数据';


-- 小红书评论表
CREATE TABLE `xhs_comments` (
  `comment_id` VARCHAR(64) NOT NULL COMMENT '评论唯一标识',
  `note_id` VARCHAR(64) NOT NULL COMMENT '所属笔记ID，关联 xhs_notes 或 xhs_note_details',
  `parent_comment_id` VARCHAR(64) DEFAULT NULL COMMENT '父评论ID，顶级评论为 NULL，子评论存储其顶级评论的 comment_id',
  `comment_user_id` VARCHAR(64) NOT NULL COMMENT '评论者用户ID',
  `comment_user_image` VARCHAR(255) DEFAULT NULL COMMENT '评论者头像 URL',
  `comment_user_nickname` VARCHAR(128) DEFAULT NULL COMMENT '评论者昵称',
  `comment_user_home_page_url` VARCHAR(255) DEFAULT NULL COMMENT '评论者主页 URL',
  `comment_content` TEXT COMMENT '评论内容',
  `comment_like_count` INT UNSIGNED DEFAULT 0 COMMENT '评论点赞数',
  `comment_sub_comment_count` INT UNSIGNED DEFAULT 0 COMMENT '子评论数量',
  `comment_create_time` DATETIME DEFAULT NULL COMMENT '评论创建时间',
  `comment_liked` TINYINT(1) DEFAULT 0 COMMENT '是否点赞（0：未点赞，1：已点赞）',
  `comment_show_tags` JSON DEFAULT NULL COMMENT '评论显示标签（例如标识是否作者评论等，存 JSON 数组）',
  `comment_sub_comment_cursor` VARCHAR(64) DEFAULT NULL COMMENT '子评论分页游标（如接口返回）',
  `comment_sub_comment_has_more` TINYINT(1) DEFAULT 0 COMMENT '子评论是否有更多（0：否，1：是）',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`comment_id`),
  KEY `idx_note_id` (`note_id`),
  KEY `idx_parent_comment_id` (`parent_comment_id`),
  KEY `idx_comment_user_id` (`comment_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小红书评论表，存储笔记下的评论及回复，使用 parent_comment_id 区分层级';


-- 关键词群表（存储关键词群基本信息）
CREATE TABLE `xhs_keyword_groups` (
  `group_id` INT NOT NULL AUTO_INCREMENT COMMENT '关键词群唯一标识',
  `group_name` VARCHAR(255) NOT NULL COMMENT '关键词群名称或描述',
  `keywords` JSON DEFAULT NULL COMMENT '该关键词群包含的关键词列表（JSON 数组）',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='关键词群表，用于存储关键词群信息';


-- 关键词群与笔记关联关系表
CREATE TABLE `xhs_keyword_group_notes` (
  `id` BIGINT AUTO_INCREMENT NOT NULL COMMENT '自增主键',
  `group_id` INT(11) NOT NULL COMMENT '关键词群ID，关联 xhs_keyword_groups(group_id)',
  `note_id` VARCHAR(64) NOT NULL COMMENT '笔记ID，关联 xhs_notes(note_id)',
  `retrieved_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '该笔记被采集的时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_group_note` (`group_id`, `note_id`),
  KEY `idx_note_id` (`note_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='关键词群与笔记关联关系表，用于记录某个关键词群查询到的帖子';
