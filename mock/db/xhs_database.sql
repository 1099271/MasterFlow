-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2025-03-10 10:11:54
-- 服务器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `test`
--

-- --------------------------------------------------------

--
-- 表的结构 `xhs_authers`
--

CREATE TABLE IF NOT EXISTS `xhs_authers` (
  `auther_user_id` varchar(64) NOT NULL COMMENT '作者唯一标识',
  `auther_home_page_url` varchar(255) DEFAULT NULL COMMENT '作者主页 URL',
  `auther_avatar` varchar(255) DEFAULT NULL COMMENT '作者头像 URL',
  `auther_nick_name` varchar(128) DEFAULT NULL COMMENT '作者昵称',
  `auther_desc` text DEFAULT NULL COMMENT '作者简介',
  `auther_interaction` int(10) UNSIGNED DEFAULT 0 COMMENT '互动数',
  `auther_ip_location` varchar(64) DEFAULT NULL COMMENT '作者所在地',
  `auther_red_id` varchar(64) DEFAULT NULL COMMENT '红书 ID',
  `auther_tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '作者标签数组（JSON 格式）' CHECK (json_valid(`auther_tags`)),
  `auther_fans` int(10) UNSIGNED DEFAULT 0 COMMENT '粉丝数量',
  `auther_follows` int(10) UNSIGNED DEFAULT 0 COMMENT '关注数量',
  `auther_gender` varchar(16) DEFAULT NULL COMMENT '作者性别',
  `created_at` datetime DEFAULT current_timestamp() COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '记录更新时间',
  PRIMARY KEY (`auther_user_id`),
  UNIQUE KEY `uk_auther_red_id` (`auther_red_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='小红书作者信息表';

-- --------------------------------------------------------

--
-- 表的结构 `xhs_comments`
--

CREATE TABLE IF NOT EXISTS `xhs_comments` (
  `comment_id` varchar(64) NOT NULL COMMENT '评论唯一标识',
  `note_id` varchar(64) NOT NULL COMMENT '所属笔记ID，关联 xhs_notes 或 xhs_note_details',
  `parent_comment_id` varchar(64) DEFAULT NULL COMMENT '父评论ID，顶级评论为 NULL，子评论存储其顶级评论的 comment_id',
  `comment_user_id` varchar(64) NOT NULL COMMENT '评论者用户ID',
  `comment_user_image` varchar(255) DEFAULT NULL COMMENT '评论者头像 URL',
  `comment_user_nickname` varchar(128) DEFAULT NULL COMMENT '评论者昵称',
  `comment_user_home_page_url` varchar(255) DEFAULT NULL COMMENT '评论者主页 URL',
  `comment_content` text DEFAULT NULL COMMENT '评论内容',
  `comment_like_count` int(10) UNSIGNED DEFAULT 0 COMMENT '评论点赞数',
  `comment_sub_comment_count` int(10) UNSIGNED DEFAULT 0 COMMENT '子评论数量',
  `comment_create_time` datetime DEFAULT NULL COMMENT '评论创建时间',
  `comment_liked` tinyint(1) DEFAULT 0 COMMENT '是否点赞（0：未点赞，1：已点赞）',
  `comment_show_tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '评论显示标签（例如标识是否作者评论等，存 JSON 数组）' CHECK (json_valid(`comment_show_tags`)),
  `comment_sub_comment_cursor` varchar(64) DEFAULT NULL COMMENT '子评论分页游标（如接口返回）',
  `comment_sub_comment_has_more` tinyint(1) DEFAULT 0 COMMENT '子评论是否有更多（0：否，1：是）',
  `created_at` datetime DEFAULT current_timestamp() COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '记录更新时间',
  PRIMARY KEY (`comment_id`),
  KEY `idx_note_id` (`note_id`),
  KEY `idx_parent_comment_id` (`parent_comment_id`),
  KEY `idx_comment_user_id` (`comment_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='小红书评论表，存储笔记下的评论及回复，使用 parent_comment_id 区分层级';

-- --------------------------------------------------------

--
-- 表的结构 `xhs_comment_at_users`
--

CREATE TABLE IF NOT EXISTS `xhs_comment_at_users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `comment_id` varchar(64) NOT NULL COMMENT '关联的评论ID，关联 xhs_comments(comment_id)',
  `at_user_id` varchar(64) NOT NULL COMMENT '被@的用户ID',
  `at_user_nickname` varchar(128) DEFAULT NULL COMMENT '被@的用户昵称',
  `at_user_home_page_url` varchar(255) DEFAULT NULL COMMENT '被@用户主页 URL',
  `created_at` datetime DEFAULT current_timestamp() COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_comment_id` (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='小红书评论@用户信息表，用于存储评论中@的用户数据';

-- --------------------------------------------------------

--
-- 表的结构 `xhs_keyword_groups`
--

CREATE TABLE IF NOT EXISTS `xhs_keyword_groups` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '关键词群唯一标识',
  `group_name` varchar(255) NOT NULL COMMENT '关键词群名称或描述',
  `keywords` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '该关键词群包含的关键词列表（JSON 数组）' CHECK (json_valid(`keywords`)),
  `created_at` datetime DEFAULT current_timestamp() COMMENT '记录创建时间',
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='关键词群表，用于存储关键词群信息';

-- --------------------------------------------------------

--
-- 表的结构 `xhs_keyword_group_notes`
--

CREATE TABLE IF NOT EXISTS `xhs_keyword_group_notes` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `group_id` varchar(64) NOT NULL COMMENT '关键词群ID，关联 xhs_keyword_groups(group_id)',
  `note_id` varchar(64) NOT NULL COMMENT '笔记ID，关联 xhs_notes(note_id)',
  `retrieved_at` datetime DEFAULT current_timestamp() COMMENT '该笔记被采集的时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_group_note` (`group_id`,`note_id`),
  KEY `idx_note_id` (`note_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='关键词群与笔记关联关系表，用于记录某个关键词群查询到的帖子';

-- --------------------------------------------------------

--
-- 表的结构 `xhs_notes`
--

CREATE TABLE IF NOT EXISTS `xhs_notes` (
  `note_id` varchar(64) NOT NULL COMMENT '笔记唯一标识',
  `note_url` varchar(255) NOT NULL COMMENT '笔记详情页面 URL',
  `note_xsec_token` varchar(255) DEFAULT NULL COMMENT '笔记鉴权 token',
  `note_cover_url_pre` varchar(255) DEFAULT NULL COMMENT '笔记封面预览图 URL',
  `note_cover_url_default` varchar(255) DEFAULT NULL COMMENT '笔记默认封面图 URL',
  `note_cover_width` int(10) UNSIGNED DEFAULT NULL COMMENT '封面图片宽度（像素）',
  `note_cover_height` int(10) UNSIGNED DEFAULT NULL COMMENT '封面图片高度（像素）',
  `note_display_title` varchar(255) DEFAULT NULL COMMENT '笔记展示标题',
  `note_model_type` varchar(32) DEFAULT NULL COMMENT '笔记模型类型',
  `note_card_type` varchar(32) DEFAULT NULL COMMENT '笔记卡片类型',
  `note_liked` tinyint(1) DEFAULT 0 COMMENT '是否已点赞（0:未点赞, 1:已点赞）',
  `note_liked_count` int(10) UNSIGNED DEFAULT 0 COMMENT '点赞数量',
  `note_sticky` tinyint(1) DEFAULT 0 COMMENT '是否置顶（0:否, 1:是）',
  `auther_user_id` varchar(64) NOT NULL COMMENT '作者唯一标识，关联 xhs_authers 表',
  `auther_home_page_url` varchar(255) DEFAULT NULL COMMENT '作者主页 URL（冗余字段）',
  `auther_avatar` varchar(255) DEFAULT NULL COMMENT '作者头像 URL（冗余字段）',
  `auther_nick_name` varchar(128) DEFAULT NULL COMMENT '作者昵称（冗余字段）',
  `created_at` datetime DEFAULT current_timestamp() COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '记录更新时间',
  PRIMARY KEY (`note_id`),
  KEY `idx_auther_user_id` (`auther_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='小红书笔记摘要信息表';

-- --------------------------------------------------------

--
-- 表的结构 `xhs_note_details`
--

CREATE TABLE IF NOT EXISTS `xhs_note_details` (
  `note_id` varchar(64) NOT NULL COMMENT '笔记唯一标识，与 xhs_notes 对应',
  `note_url` varchar(255) NOT NULL COMMENT '笔记详情页面 URL',
  `note_last_update_time` datetime DEFAULT NULL COMMENT '笔记最后更新时间',
  `note_create_time` datetime DEFAULT NULL COMMENT '笔记创建时间',
  `note_model_type` varchar(32) DEFAULT NULL COMMENT '笔记模型类型',
  `note_card_type` varchar(32) DEFAULT NULL COMMENT '笔记卡片类型',
  `note_display_title` varchar(255) DEFAULT NULL COMMENT '笔记展示标题',
  `note_desc` text DEFAULT NULL COMMENT '笔记描述内容（包含话题及文本描述）',
  `comment_count` int(10) UNSIGNED DEFAULT 0 COMMENT '评论数量',
  `note_liked_count` int(10) UNSIGNED DEFAULT 0 COMMENT '点赞数量',
  `share_count` int(10) UNSIGNED DEFAULT 0 COMMENT '分享数量',
  `collected_count` int(10) UNSIGNED DEFAULT 0 COMMENT '收藏数量',
  `video_id` varchar(64) DEFAULT NULL COMMENT '视频标识（如存在）',
  `video_h266_url` varchar(255) DEFAULT NULL COMMENT '视频 H266 URL',
  `video_a1_url` varchar(255) DEFAULT NULL COMMENT '视频 a1 URL',
  `video_h264_url` varchar(255) DEFAULT NULL COMMENT '视频 H264 URL',
  `video_h265_url` varchar(255) DEFAULT NULL COMMENT '视频 H265 URL',
  `note_duration` int(10) UNSIGNED DEFAULT NULL COMMENT '视频时长（秒）',
  `note_image_list` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '笔记图片列表（JSON 数组）' CHECK (json_valid(`note_image_list`)),
  `note_tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL COMMENT '笔记标签数组（JSON 数组）' CHECK (json_valid(`note_tags`)),
  `note_liked` tinyint(1) DEFAULT 0 COMMENT '是否已点赞（0:未点赞, 1:已点赞）',
  `collected` tinyint(1) DEFAULT 0 COMMENT '是否已收藏（0:未收藏, 1:已收藏）',
  `auther_user_id` varchar(64) NOT NULL COMMENT '作者唯一标识，关联 xhs_authers 表',
  `created_at` datetime DEFAULT current_timestamp() COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '记录更新时间',
  PRIMARY KEY (`note_id`),
  KEY `idx_auther_user_id` (`auther_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='小红书笔记详情表';

-- --------------------------------------------------------

--
-- 表的结构 `xhs_topic_discussions`
--

CREATE TABLE IF NOT EXISTS `xhs_topic_discussions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `topic_name` varchar(255) NOT NULL COMMENT '话题名称',
  `topic_type` varchar(32) NOT NULL COMMENT '话题类型，例如 official',
  `view_num` bigint(20) UNSIGNED NOT NULL COMMENT '讨论量/浏览数',
  `smart` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否智能（0: False，1: True）',
  `record_date` date NOT NULL COMMENT '记录日期（只保留到日期）',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_topic_date` (`topic_name`,`record_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='小红书话题讨论量记录表，每日记录话题的讨论量';
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
