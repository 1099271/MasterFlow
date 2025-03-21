-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: master_flow
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `llm_configurations`
--

DROP TABLE IF EXISTS `llm_configurations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `llm_configurations` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `config_alias` varchar(128) NOT NULL COMMENT '配置别名，唯一标识，用于与诊断和标签提取挂钩',
  `model_name` varchar(128) NOT NULL COMMENT '模型名称',
  `parameter_size` varchar(64) NOT NULL COMMENT '模型参数大小（例如 7B, 13B, 175B）',
  `temperature` decimal(3,2) DEFAULT NULL COMMENT '温度设置',
  `top_p` decimal(3,2) DEFAULT NULL,
  `max_tokens` int DEFAULT NULL,
  `model_type` varchar(32) DEFAULT NULL,
  `other_params` json DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_config_alias` (`config_alias`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='LLM模型配置表，用于存储模型名称、参数大小、温度设置、类型等参数，作为 llm_note_tag_extraction 与 llm_note_diagnosis 的挂钩依据';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `llm_note_diagnosis`
--

DROP TABLE IF EXISTS `llm_note_diagnosis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `llm_note_diagnosis` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `note_id` varchar(64) NOT NULL COMMENT '笔记ID，关联 xhs_notes(note_id)',
  `llm_name` varchar(128) NOT NULL COMMENT 'LLM模型名称',
  `geo_tags` json DEFAULT NULL COMMENT '提取的地理位置标签，用 "/" 分隔',
  `cultural_tags` json DEFAULT NULL COMMENT '提取的文化元素标签，用 "/" 分隔',
  `other_tags` json DEFAULT NULL COMMENT '提取的其他方面标签，用 "/" 分隔',
  `user_gender` varchar(16) DEFAULT NULL COMMENT '推断的性别',
  `user_age_range` varchar(64) DEFAULT NULL COMMENT '推断的年龄区间',
  `user_location` varchar(128) DEFAULT NULL COMMENT '推断的地理位置',
  `user_tags` json DEFAULT NULL COMMENT '用户特征标签，用 "/" 分隔',
  `post_summary` json DEFAULT NULL COMMENT '2-3句话总结帖子核心内容',
  `post_publish_time` varchar(64) DEFAULT NULL COMMENT '推断的发布时间或 "未知"',
  `content_tendency` varchar(16) DEFAULT NULL COMMENT '内容偏向性（正面/中性/负面）',
  `content_tendency_reason` json DEFAULT NULL COMMENT '内容偏向性原因',
  `has_visited` tinyint(1) DEFAULT NULL COMMENT '是否去过（1:是, 0:否）',
  `diagnosed_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '诊断时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_note_id` (`note_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='LLM笔记诊断与反馈表，用于存储大模型对笔记的判断和反馈，包括关键词提取和数据信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `llm_note_tag_extraction`
--

DROP TABLE IF EXISTS `llm_note_tag_extraction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `llm_note_tag_extraction` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `note_id` varchar(64) NOT NULL COMMENT '笔记ID，关联 xhs_notes(note_id)',
  `model_name` varchar(128) NOT NULL COMMENT '提取标签所用的模型名称',
  `extracted_tags` json NOT NULL COMMENT '抽取的标签集合，JSON 格式，例如 [{"tag": "标签1", "score": 0.95}, {"tag": "标签2", "score": 0.87}]',
  `extraction_result` text COMMENT '模型对笔记内容的整体反馈描述（可选）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_note_id_model` (`note_id`,`model_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='LLM 对笔记标签提取结果表，用于存储模型对笔记内容的标签提取情况';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xhs_authers`
--

DROP TABLE IF EXISTS `xhs_authers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xhs_authers` (
  `auther_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '作者唯一标识',
  `auther_home_page_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作者主页 URL',
  `auther_avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作者头像 URL',
  `auther_nick_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作者昵称',
  `auther_desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '作者简介',
  `auther_interaction` int unsigned DEFAULT '0' COMMENT '互动数',
  `auther_ip_location` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作者所在地',
  `auther_red_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '红书 ID',
  `auther_tags` json DEFAULT NULL COMMENT '作者标签数组（JSON 格式）',
  `auther_fans` int unsigned DEFAULT '0' COMMENT '粉丝数量',
  `auther_follows` int unsigned DEFAULT '0' COMMENT '关注数量',
  `auther_gender` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作者性别',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`auther_user_id`),
  UNIQUE KEY `uk_auther_red_id` (`auther_red_id`),
  CONSTRAINT `xhs_authers_chk_1` CHECK (json_valid(`auther_tags`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小红书作者信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xhs_comment_at_users`
--

DROP TABLE IF EXISTS `xhs_comment_at_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xhs_comment_at_users` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `comment_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联的评论ID，关联 xhs_comments(comment_id)',
  `at_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '被@的用户ID',
  `at_user_nickname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '被@的用户昵称',
  `at_user_home_page_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '被@用户主页 URL',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_comment_id` (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小红书评论@用户信息表，用于存储评论中@的用户数据';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xhs_comments`
--

DROP TABLE IF EXISTS `xhs_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xhs_comments` (
  `comment_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论唯一标识',
  `note_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '所属笔记ID，关联 xhs_notes 或 xhs_note_details',
  `parent_comment_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '父评论ID，顶级评论为 NULL，子评论存储其顶级评论的 comment_id',
  `comment_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '评论者用户ID',
  `comment_user_image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '评论者头像 URL',
  `comment_user_nickname` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '评论者昵称',
  `comment_user_home_page_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '评论者主页 URL',
  `comment_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '评论内容',
  `comment_like_count` int unsigned DEFAULT '0' COMMENT '评论点赞数',
  `comment_sub_comment_count` int unsigned DEFAULT '0' COMMENT '子评论数量',
  `comment_create_time` datetime DEFAULT NULL COMMENT '评论创建时间',
  `comment_liked` tinyint(1) DEFAULT '0' COMMENT '是否点赞（0：未点赞，1：已点赞）',
  `comment_show_tags` json DEFAULT NULL COMMENT '评论显示标签（例如标识是否作者评论等，存 JSON 数组）',
  `comment_sub_comment_cursor` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '子评论分页游标（如接口返回）',
  `comment_sub_comment_has_more` tinyint(1) DEFAULT '0' COMMENT '子评论是否有更多（0：否，1：是）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`comment_id`),
  KEY `idx_note_id` (`note_id`),
  KEY `idx_parent_comment_id` (`parent_comment_id`),
  KEY `idx_comment_user_id` (`comment_user_id`),
  CONSTRAINT `xhs_comments_chk_1` CHECK (json_valid(`comment_show_tags`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小红书评论表，存储笔记下的评论及回复，使用 parent_comment_id 区分层级';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xhs_keyword_group_notes`
--

DROP TABLE IF EXISTS `xhs_keyword_group_notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xhs_keyword_group_notes` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `group_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关键词群ID，关联 xhs_keyword_groups(group_id)',
  `note_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '笔记ID，关联 xhs_notes(note_id)',
  `retrieved_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '该笔记被采集的时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_group_note` (`group_id`,`note_id`),
  KEY `idx_note_id` (`note_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3910 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='关键词群与笔记关联关系表，用于记录某个关键词群查询到的帖子';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xhs_keyword_groups`
--

DROP TABLE IF EXISTS `xhs_keyword_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xhs_keyword_groups` (
  `group_id` int NOT NULL AUTO_INCREMENT COMMENT '关键词群唯一标识',
  `group_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关键词群名称或描述',
  `keywords` json DEFAULT NULL COMMENT '该关键词群包含的关键词列表（JSON 数组）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`group_id`),
  CONSTRAINT `xhs_keyword_groups_chk_1` CHECK (json_valid(`keywords`))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='关键词群表，用于存储关键词群信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xhs_note_details`
--

DROP TABLE IF EXISTS `xhs_note_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xhs_note_details` (
  `note_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '笔记唯一标识，与 xhs_notes 对应',
  `note_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '笔记详情页面 URL',
  `note_last_update_time` datetime DEFAULT NULL COMMENT '笔记最后更新时间',
  `note_create_time` datetime DEFAULT NULL COMMENT '笔记创建时间',
  `note_model_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '笔记模型类型',
  `note_card_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '笔记卡片类型',
  `note_display_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '笔记展示标题',
  `note_desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '笔记描述内容（包含话题及文本描述）',
  `comment_count` int unsigned DEFAULT '0' COMMENT '评论数量',
  `note_liked_count` int unsigned DEFAULT '0' COMMENT '点赞数量',
  `share_count` int unsigned DEFAULT '0' COMMENT '分享数量',
  `collected_count` int unsigned DEFAULT '0' COMMENT '收藏数量',
  `video_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频标识（如存在）',
  `video_h266_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频 H266 URL',
  `video_a1_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频 a1 URL',
  `video_h264_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频 H264 URL',
  `video_h265_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频 H265 URL',
  `note_duration` int unsigned DEFAULT NULL COMMENT '视频时长（秒）',
  `note_image_list` json DEFAULT NULL COMMENT '笔记图片列表（JSON 数组）',
  `note_tags` json DEFAULT NULL COMMENT '笔记标签数组（JSON 数组）',
  `note_liked` tinyint(1) DEFAULT '0' COMMENT '是否已点赞（0:未点赞, 1:已点赞）',
  `collected` tinyint(1) DEFAULT '0' COMMENT '是否已收藏（0:未收藏, 1:已收藏）',
  `auther_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '作者唯一标识，关联 xhs_authers 表',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`note_id`),
  KEY `idx_auther_user_id` (`auther_user_id`),
  CONSTRAINT `xhs_note_details_chk_1` CHECK (json_valid(`note_image_list`)),
  CONSTRAINT `xhs_note_details_chk_2` CHECK (json_valid(`note_tags`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小红书笔记详情表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xhs_notes`
--

DROP TABLE IF EXISTS `xhs_notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xhs_notes` (
  `note_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '笔记唯一标识',
  `note_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '笔记详情页面 URL',
  `note_xsec_token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '笔记鉴权 token',
  `note_cover_url_pre` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '笔记封面预览图 URL',
  `note_cover_url_default` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '笔记默认封面图 URL',
  `note_cover_width` int unsigned DEFAULT NULL COMMENT '封面图片宽度（像素）',
  `note_cover_height` int unsigned DEFAULT NULL COMMENT '封面图片高度（像素）',
  `note_display_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '笔记展示标题',
  `note_model_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '笔记模型类型',
  `note_card_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '笔记卡片类型',
  `note_liked` tinyint(1) DEFAULT '0' COMMENT '是否已点赞（0:未点赞, 1:已点赞）',
  `note_liked_count` int unsigned DEFAULT '0' COMMENT '点赞数量',
  `note_sticky` tinyint(1) DEFAULT '0' COMMENT '是否置顶（0:否, 1:是）',
  `auther_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '作者唯一标识，关联 xhs_authers 表',
  `auther_home_page_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作者主页 URL（冗余字段）',
  `auther_avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作者头像 URL（冗余字段）',
  `auther_nick_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '作者昵称（冗余字段）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`note_id`),
  KEY `idx_auther_user_id` (`auther_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小红书笔记摘要信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xhs_topic_discussions`
--

DROP TABLE IF EXISTS `xhs_topic_discussions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xhs_topic_discussions` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `topic_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '话题名称',
  `topic_type` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '话题类型，例如 official',
  `view_num` bigint unsigned NOT NULL COMMENT '讨论量/浏览数',
  `smart` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否智能（0: False，1: True）',
  `record_date` date NOT NULL COMMENT '记录日期（只保留到日期）',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_topic_date` (`topic_name`,`record_date`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='小红书话题讨论量记录表，每日记录话题的讨论量';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-20 12:10:03
