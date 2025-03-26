# 小红书标签分析系统：SQL查询与可视化解读指南

## 目录

1. [模型性能分析可视化](#1-模型性能分析可视化)
2. [标签内容分析可视化](#2-标签内容分析可视化)
3. [笔记内容与标签关联分析可视化](#3-笔记内容与标签关联分析可视化)
4. [关键词群与标签分析可视化](#4-关键词群与标签分析可视化)
5. [标签系统优化分析可视化](#5-标签系统优化分析可视化)
6. [标签差异评估可视化](#6-标签差异评估可视化)
7. [标签分析结果摘要可视化](#7-标签分析结果摘要可视化)

## 1. 模型性能分析可视化

### 1.1 LLM模型标签提取性能雷达图

#### SQL查询逻辑
```sql
SELECT 
    llm_name,
    tag_type,
    ROUND(AVG(weighted_score), 3) AS avg_weighted_score,
    ROUND(AVG(max_similarity), 3) AS avg_max_similarity,
    ROUND(AVG(optimal_matching), 3) AS avg_optimal_matching,
    ROUND(AVG(coverage), 3) AS avg_coverage,
    ROUND(AVG(threshold_matching), 3) AS avg_threshold_matching,
    COUNT(*) AS sample_count
FROM tag_comparison_results
GROUP BY llm_name, tag_type
ORDER BY tag_type, avg_weighted_score DESC;
```

**查询解释：**
- 此查询按LLM模型名称和标签类型分组，计算了五个关键性能指标的平均值
- 指标包括：加权得分、最大相似度、最佳匹配度、覆盖率和阈值匹配度
- `sample_count`统计了每个组合的样本数量，用于判断结果的可靠性

#### 可视化逻辑
雷达图以五个维度表示模型性能，每个维度对应一个评估指标。图形中的每条闭合曲线代表一个LLM模型，面积越大表示整体性能越好。

#### 如何阅读图表
1. **比较封闭区域大小**：面积更大的模型在总体上表现更好
2. **观察形状差异**：
   - 如果某个模型在特定维度上突出，则表明其在该指标上具有优势
   - 形状更加平衡的模型在各方面表现更均衡
3. **检查顶点值**：每个顶点显示该模型在特定指标上的具体得分
4. **查看标题**：标题显示当前分析的标签类型（如地理标签、文化标签）

#### 可能的结论
- 某个模型可能在整体表现上优于其他模型
- 一些模型可能在特定指标上表现突出，如覆盖率高但精确度低
- 某些模型可能在特定类型的标签上表现更好（如Deepseek可能在地理标签上更准确，而Qwen在文化标签上更好）
- 识别出性能较差的维度，为未来模型优化提供方向

### 1.2 Embedding模型性能柱状图

#### SQL查询逻辑
```sql
SELECT 
    compare_model_name,
    tag_type,
    ROUND(AVG(weighted_score), 3) AS avg_weighted_score,
    ROUND(AVG(max_similarity), 3) AS avg_max_similarity,
    ROUND(AVG(optimal_matching), 3) AS avg_optimal_matching,
    ROUND(AVG(coverage), 3) AS avg_coverage,
    COUNT(*) AS sample_count
FROM tag_comparison_results
WHERE compare_model_name IS NOT NULL
GROUP BY compare_model_name, tag_type
ORDER BY tag_type, avg_weighted_score DESC;
```

**查询解释：**
- 此查询专注于Embedding模型（如BGE、DistilUSE-v2）的性能比较
- 按Embedding模型名称和标签类型分组计算平均指标值
- 只包含`compare_model_name`不为NULL的记录，确保有真实的嵌入模型数据

#### 可视化逻辑
分组柱状图用于比较不同Embedding模型在每个指标上的表现。每组柱子代表一个模型，不同颜色代表不同标签类型。

#### 如何阅读图表
1. **比较柱高**：更高的柱子表示该模型在该指标上表现更好
2. **对比不同颜色**：不同颜色代表不同标签类型，可比较模型在各标签类型上的表现差异
3. **查看数值标签**：柱子上方的数值显示具体分数
4. **考虑样本规模**：结合`sample_count`评估结果可靠性（通常样本量越大结果越可靠）

#### 可能的结论
- 识别在语义理解上表现最佳的Embedding模型（例如BGE在地理标签上可能优于DistilUSE-v2）
- 发现特定模型在某些指标上的优势（如最大相似度高但覆盖率低）
- 了解不同标签类型对模型性能的影响（如文化标签可能比地理标签更难准确嵌入）
- 确定可能的模型优化方向（例如，针对覆盖率低的模型增强其检索能力）

### 1.3 LLM与Embedding模型组合热力图

#### SQL查询逻辑
```sql
SELECT 
    llm_name,
    compare_model_name,
    tag_type,
    ROUND(AVG(weighted_score), 3) AS avg_weighted_score
FROM tag_comparison_results
WHERE compare_model_name IS NOT NULL
GROUP BY llm_name, compare_model_name, tag_type
ORDER BY tag_type, avg_weighted_score DESC;
```

**查询解释：**
- 此查询分析LLM模型和Embedding模型的组合效果
- 对每种组合计算平均加权得分
- 结果按标签类型和加权得分降序排列，便于识别最佳组合

#### 可视化逻辑
热力图使用颜色深浅表示不同模型组合的性能。行代表LLM模型，列代表Embedding模型，颜色越深表示组合效果越好。

#### 如何阅读图表
1. **观察颜色深浅**：深色单元格表示更高的加权得分，代表更好的组合效果
2. **比较行差异**：比较同一Embedding模型与不同LLM模型组合的效果
3. **比较列差异**：比较同一LLM模型与不同Embedding模型组合的效果
4. **查看数值标签**：每个单元格中的数值显示具体的加权得分
5. **注意标签类型**：每个热力图对应一种标签类型，不同标签类型可能有不同的最佳组合

#### 可能的结论
- 确定特定标签类型的最佳模型组合（如Deepseek+BGE可能在地理标签上效果最佳）
- 发现某些LLM和Embedding模型之间的协同效应
- 识别表现不佳的组合，以避免在实际应用中使用
- 优化资源分配，为不同类型的标签任务选择不同的模型组合

### 1.4 低匹配度案例散点图

#### SQL查询逻辑
```sql
SELECT 
    note_id,
    llm_name,
    compare_model_name,
    tag_type,
    weighted_score,
    max_similarity,
    optimal_matching,
    coverage
FROM tag_comparison_results
WHERE weighted_score < 0.6  -- 调整阈值以找出问题案例
ORDER BY weighted_score ASC
LIMIT 50;
```

**查询解释：**
- 此查询筛选出加权得分低于0.6的记录，这些记录代表标签提取效果不佳的案例
- 包含多个关键指标，便于诊断问题所在
- 结果按加权得分升序排列，首先显示最差的案例
- 限制返回50条记录，避免结果过多

#### 可视化逻辑
散点图用于展示低匹配度案例的特征分布。X轴为加权得分，Y轴为覆盖率，点的大小表示最佳匹配度，颜色代表LLM模型，形状代表标签类型。

#### 如何阅读图表
1. **关注点的位置**：左下角的点表示得分和覆盖率都低的案例，这些是最需要关注的问题案例
2. **观察点的大小**：较小的点表示最佳匹配度低，可能是标签质量问题
3. **区分不同颜色**：判断是否特定模型产生了更多的问题案例
4. **区分不同形状**：判断是否特定标签类型更容易出现问题
5. **使用悬停功能**：查看详细信息，包括笔记ID和具体指标值

#### 可能的结论
- 识别出系统性问题（如某个特定模型或标签类型导致的批量低分）
- 发现模式（例如，低覆盖率和低加权分数之间的关联）
- 确定需要人工审查的案例
- 为标签提取系统改进提供具体方向（如提高某些模型的覆盖率）

## 2. 标签内容分析可视化

### 2.1 标签词云图

#### SQL查询逻辑
```sql
WITH RECURSIVE extracted_collected_tags AS (
    SELECT 
        id,
        note_id,
        llm_name,
        tag_type,
        JSON_EXTRACT(collected_tags, '$[*]') AS tags
    FROM tag_comparison_results
),
tag_unnest AS (
    SELECT 
        id,
        note_id,
        llm_name,
        tag_type,
        JSON_UNQUOTE(JSON_EXTRACT(tags, CONCAT('$[', numbers.n, ']'))) AS tag_name
    FROM extracted_collected_tags
    JOIN (
        SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL
        SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL
        SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ) AS numbers
    WHERE JSON_EXTRACT(tags, CONCAT('$[', numbers.n, ']')) IS NOT NULL
)
SELECT 
    tag_type,
    tag_name,
    COUNT(*) AS frequency,
    COUNT(DISTINCT note_id) AS unique_notes
FROM tag_unnest
GROUP BY tag_type, tag_name
HAVING COUNT(*) > 1
ORDER BY tag_type, frequency DESC
LIMIT 100;
```

**查询解释：**
- 此查询使用递归CTE和数字表展开JSON数组，提取所有标签
- `extracted_collected_tags`从`collected_tags`列提取JSON数组
- `tag_unnest`使用数字表联接展开数组为单行记录
- 最后统计每个标签的频率和出现在多少个唯一笔记中
- 只保留出现频率大于1的标签，按标签类型和频率降序排序

#### 可视化逻辑
词云图根据标签出现频率调整文字大小，更频繁出现的标签显示得更大。每种标签类型生成一个独立词云。

#### 如何阅读图表
1. **观察最大词语**：体积最大的词代表最流行的标签
2. **注意颜色变化**：不同颜色可能表示不同频率范围
3. **词云密度**：整体密度反映标签多样性，密集表示标签分布广泛
4. **比较不同词云**：比较不同标签类型的词云，了解不同类型标签的分布特征

#### 可能的结论
- 识别每种标签类型中最常见的标签（如地理标签中的"上海"、"北京"）
- 发现标签分布模式（如地理标签集中于大城市，文化标签多样化）
- 确定内容趋势和热点（如特定景点、文化元素的流行度）
- 为内容策略提供方向（如针对热门地点开发相关营销内容）

### 2.2 标签质量分布堆叠柱状图

#### SQL查询逻辑
```sql
SELECT 
    compare_model_name,
    tag_type,
    CASE 
        WHEN weighted_score < 0.5 THEN '低质量(<0.5)'
        WHEN weighted_score < 0.7 THEN '中等(0.5-0.7)'
        WHEN weighted_score < 0.9 THEN '良好(0.7-0.9)'
        ELSE '优秀(≥0.9)'
    END AS quality_band,
    COUNT(*) AS count
FROM tag_comparison_results
WHERE compare_model_name IS NOT NULL
GROUP BY compare_model_name, tag_type, quality_band
ORDER BY compare_model_name, tag_type;
```

**查询解释：**
- 此查询将加权得分划分为四个质量等级：低质量、中等、良好和优秀
- 按Embedding模型名称、标签类型和质量等级分组计算记录数量
- 只包含有Embedding模型的记录
- 结果按模型名称和标签类型排序

#### 可视化逻辑
堆叠柱状图显示不同Embedding模型的标签质量分布。每个柱子代表一个模型，不同颜色的堆叠段代表不同质量等级的标签数量。

#### 如何阅读图表
1. **比较柱高**：总高度表示该模型处理的标签总量
2. **观察颜色比例**：
   - 绿色段（良好/优秀）比例高表示高质量标签占比大
   - 红色段（低质量）比例高表示问题较多
3. **比较不同模型**：相同标签类型下不同模型的质量分布差异
4. **观察不同标签类型**：同一模型在不同标签类型上的表现差异

#### 可能的结论
- 确定哪个Embedding模型产生的高质量标签比例最高
- 发现某些模型在特定标签类型上表现突出
- 识别低质量标签占比高的模型，可能需要调整或替换
- 了解不同标签类型的整体质量分布，判断哪类标签更容易准确提取

## 3. 笔记内容与标签关联分析可视化

### 3.1 标签质量与内容倾向分组柱状图

#### SQL查询逻辑
```sql
SELECT 
    tcr.llm_name,
    tcr.tag_type,
    lnd.content_tendency,
    ROUND(AVG(tcr.weighted_score), 3) AS avg_weighted_score,
    COUNT(*) AS count
FROM tag_comparison_results tcr
JOIN llm_note_diagnosis lnd ON tcr.note_id = lnd.note_id
WHERE lnd.content_tendency IS NOT NULL
GROUP BY tcr.llm_name, tcr.tag_type, lnd.content_tendency
ORDER BY tcr.llm_name, tcr.tag_type, lnd.content_tendency;
```

**查询解释：**
- 此查询将标签比较结果与笔记诊断数据关联，分析内容倾向与标签质量的关系
- 通过`note_id`连接两个表，确保分析同一笔记
- 按LLM模型名称、标签类型和内容倾向（正面/中性/负面）分组
- 计算每组的平均加权得分和记录数
- 排除内容倾向为NULL的记录

#### 可视化逻辑
分组柱状图比较不同内容倾向下标签提取的质量。X轴为内容倾向（正面/中性/负面），Y轴为平均加权得分，不同颜色代表不同LLM模型。

#### 如何阅读图表
1. **比较柱高**：更高的柱子表示该组合的标签质量更好
2. **对比同一内容倾向**：比较不同模型在相同内容倾向上的表现
3. **观察趋势**：判断内容倾向是否影响标签提取质量（如正面内容是否更易于准确提取标签）
4. **查看样本量标注**：每个柱子上方的"n=XX"表示样本数量，样本量越大结果越可靠
5. **比较不同标签类型**：切换不同图表比较内容倾向对不同标签类型的影响

#### 可能的结论
- 发现特定内容倾向对标签提取质量的影响（例如，负面内容的标签提取可能更困难）
- 识别在不同情感内容上表现最佳的模型（如某模型可能在处理负面内容时更准确）
- 了解模型偏差（如某些模型可能对正面内容的标签提取质量更高）
- 优化特定内容倾向的标签提取策略

### 3.2 标签质量与用户到访状态箱型图

#### SQL查询逻辑
```sql
SELECT 
    tcr.note_id,
    tcr.llm_name,
    tcr.tag_type,
    tcr.weighted_score,
    lnd.has_visited
FROM tag_comparison_results tcr
JOIN llm_note_diagnosis lnd ON tcr.note_id = lnd.note_id
WHERE lnd.has_visited IS NOT NULL;
```

**查询解释：**
- 此查询连接标签比较结果与笔记诊断数据，分析用户是否到访与标签质量的关系
- 按笔记ID级别保留详细数据，便于箱型图分析分布
- 包含LLM模型名称、标签类型、加权得分和到访状态
- 仅包含有明确到访状态（是/否）的记录

#### 可视化逻辑
箱型图显示不同到访状态下标签质量的分布情况。每个箱子代表一组数据（已到访/未到访），展示中位数、四分位数和异常值。

#### 如何阅读图表
1. **比较箱体位置**：更高的箱体表示该组的标签质量整体更高
2. **观察箱体高度**：箱体越短，数据分布越集中；越长，分布越分散
3. **注意中位线**：箱体中间的线表示中位数，反映典型表现
4. **检查异常点**：箱体外的点表示异常值，可能需要特别关注
5. **比较不同分组**：对比已到访和未到访组的差异

#### 可能的结论
- 判断用户到访状态是否影响标签提取质量（如实际到访的笔记可能包含更准确的地理标签）
- 发现标签质量分布模式（如已到访笔记的标签质量可能更一致）
- 识别可能需要特别关注的异常案例（如标签质量特别低的已到访笔记）
- 优化针对不同到访状态的标签提取策略

### 3.3 标签质量与笔记互动指标散点图矩阵

#### SQL查询逻辑
```sql
SELECT 
    tcr.note_id,
    tcr.llm_name,
    tcr.tag_type,
    tcr.weighted_score,
    nd.note_liked_count AS likes,
    nd.collected_count AS collects,
    nd.comment_count AS comments
FROM tag_comparison_results tcr
JOIN xhs_note_details nd ON tcr.note_id = nd.note_id
LIMIT 1000;  # 限制数量，避免图形过于复杂
```

**查询解释：**
- 此查询连接标签比较结果与笔记详情数据，分析笔记互动指标与标签质量的关系
- 提取三个关键互动指标：点赞数、收藏数和评论数
- 限制返回1000条记录，避免可视化过于复杂
- 按笔记ID级别保留原始数据，便于散点图分析相关性

#### 可视化逻辑
散点图矩阵展示标签质量与各互动指标之间的关系，以及互动指标之间的相互关系。每个小图表示两个变量之间的散点关系。

#### 如何阅读图表
1. **观察点分布趋势**：向右上方集中表示正相关，向左上方集中表示负相关
2. **注意密度**：点密集处表示常见值范围
3. **识别离群值**：远离主要分布的点可能是特殊案例
4. **比较不同矩阵**：对比不同LLM模型和标签类型的散点图矩阵
5. **关注对数转换**：因为使用了对数转换处理极端值，请注意解释时考虑这一点

#### 可能的结论
- 发现标签质量与互动指标的相关性（如高质量标签是否与高互动率相关）
- 识别互动指标之间的关系（如点赞和收藏是否高度相关）
- 发现可能的用户行为模式（如高评论但低点赞的内容特点）
- 判断标签质量是否可以作为预测内容受欢迎度的因素

## 4. 关键词群与标签分析可视化

### 4.1 关键词群标签质量柱状图

#### SQL查询逻辑
```sql
SELECT 
    kg.group_name,
    tcr.llm_name,
    tcr.tag_type,
    ROUND(AVG(tcr.weighted_score), 3) AS avg_weighted_score,
    COUNT(DISTINCT tcr.note_id) AS note_count
FROM tag_comparison_results tcr
JOIN xhs_keyword_group_notes kgn ON tcr.note_id = kgn.note_id
JOIN xhs_keyword_groups kg ON kgn.group_id = kg.group_id
GROUP BY kg.group_name, tcr.llm_name, tcr.tag_type
ORDER BY kg.group_name, tcr.llm_name, tcr.tag_type;
```

**查询解释：**
- 此查询分析不同关键词群中的标签提取质量
- 通过三表联接，将标签比较结果与关键词群及其关联笔记连接起来
- 按关键词群名称、LLM模型名称和标签类型分组
- 计算每个组合的平均加权得分和唯一笔记数量

#### 可视化逻辑
分组柱状图比较不同关键词群中标签提取的质量。X轴为关键词群名称，Y轴为平均加权得分，不同颜色代表不同LLM模型。

#### 如何阅读图表
1. **比较柱高**：更高的柱子表示该关键词群的标签质量更好
2. **对比同一关键词群**：比较不同模型在同一关键词群上的表现差异
3. **观察整体趋势**：判断哪些关键词群整体标签质量更高
4. **查看样本量标注**：每个柱子上的"n=XX"表示样本数量，用于评估结果可靠性
5. **注意x轴标签**：有些关键词群名称可能较长，需要注意完整内容

#### 可能的结论
- 识别标签提取质量最高的关键词群（如旅游地点相关内容可能标签质量更高）
- 发现在特定关键词群上表现最佳的模型
- 判断内容类型与标签准确性的关系
- 优化针对不同内容主题的标签提取策略
- 确定可能需要改进的关键词群（标签质量普遍较低的群体）

### 4.2 关键词群标签频次热力图

#### SQL查询逻辑
```sql
WITH RECURSIVE extracted_tags AS (
    SELECT 
        tcr.note_id,
        tcr.tag_type,
        kg.group_name,
        JSON_EXTRACT(tcr.collected_tags, '$[*]') AS extracted_tags
    FROM tag_comparison_results tcr
    JOIN xhs_keyword_group_notes kgn ON tcr.note_id = kgn.note_id
    JOIN xhs_keyword_groups kg ON kgn.group_id = kg.group_id
),
tag_unnest AS (
    SELECT 
        note_id,
        tag_type,
        group_name,
        JSON_UNQUOTE(
            JSON_EXTRACT(extracted_tags, CONCAT('$[', numbers.n, ']'))
        ) AS tag_name
    FROM extracted_tags
    JOIN (
        SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL
        SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL
        SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ) AS numbers
    WHERE JSON_EXTRACT(extracted_tags, CONCAT('$[', numbers.n, ']')) IS NOT NULL
)
SELECT 
    group_name,
    tag_type,
    tag_name,
    COUNT(*) AS frequency,
    COUNT(DISTINCT note_id) AS unique_notes
FROM tag_unnest
GROUP BY group_name, tag_type, tag_name
HAVING COUNT(*) > 1
ORDER BY group_name, tag_type, frequency DESC
LIMIT 300;
```

**查询解释：**
- 此查询分析不同关键词群中出现的标签及其频率
- 使用递归CTE展开JSON数组中的标签
- 连接关键词群和相关笔记表，确保分析不同关键词群的标签分布
- 统计每个关键词群和标签类型组合中各标签的出现频率
- 只保留出现频率大于1的标签，按频率降序排序

#### 可视化逻辑
热力图展示关键词群与标签之间的关联强度。行代表不同的关键词群，列代表不同的标签，颜色深浅表示标签在该关键词群中出现的频率。

#### 如何阅读图表
1. **观察颜色深浅**：深色单元格表示该标签在对应关键词群中出现频率高
2. **识别横向模式**：某一行中的多个深色单元格表示该关键词群关联多种标签
3. **识别纵向模式**：某一列中的多个深色单元格表示该标签在多个关键词群中常见
4. **查看具体数值**：每个单元格中的数字表示具体频次
5. **关注空白区域**：表示该关键词群与该标签无关联

#### 可能的结论
- 识别每个关键词群的特征标签（高频率标签）
- 发现跨群体常见标签（多行都深色的列）
- 了解关键词群之间的内容重叠度
- 为内容分类和推荐系统提供洞察
- 优化关键词群设置，避免过度重叠或缺少覆盖

## 5. 标签系统优化分析可视化

### 5.1 缺失标准标签直方图

#### SQL查询逻辑
```sql
WITH RECURSIVE extracted_tags AS (
    SELECT 
        tag_type,
        JSON_EXTRACT(collected_tags, '$[*]') AS tags
    FROM tag_comparison_results
),
tag_unnest AS (
    SELECT 
        tag_type,
        JSON_UNQUOTE(
            JSON_EXTRACT(tags, CONCAT('$[', numbers.n, ']'))
        ) AS tag_name
    FROM extracted_tags
    JOIN (
        SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL
        SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL
        SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ) AS numbers
    WHERE JSON_EXTRACT(tags, CONCAT('$[', numbers.n, ']')) IS NOT NULL
)
SELECT 
    tu.tag_type,
    tu.tag_name,
    COUNT(*) AS frequency
FROM tag_unnest tu
LEFT JOIN tag_standards ts ON tu.tag_name = ts.tag_name AND tu.tag_type = ts.tag_type
WHERE ts.id IS NULL -- 标签不存在于标准表中
GROUP BY tu.tag_type, tu.tag_name
HAVING COUNT(*) > 3  -- 频率阈值
ORDER BY tu.tag_type, frequency DESC
LIMIT 100;
```

**查询解释：**
- 此查询分析当前提取的标签中，哪些不在标准标签库中但出现频率较高
- 使用递归CTE展开JSON数组中的标签
- 通过左连接标准标签表并过滤`id IS NULL`，找出不在标准库中的标签
- 设置频率阈值（>3）筛选常见标签
- 按标签类型和频率降序排序，优先展示最常见的缺失标签

#### 可视化逻辑
直方图展示每个缺失的标准标签出现的频率。X轴为标签名称，Y轴为出现频率，颜色深浅也表示频率。

#### 如何阅读图表
1. **观察柱高**：越高的柱子代表该缺失标签出现越频繁
2. **比较颜色深浅**：深色表示高频出现的标签
3. **查看X轴标签**：阅读具体的缺失标签名称
4. **注意类型标题**：确认当前查看的是哪类标签（地理、文化等）

#### 可能的结论
- 识别应优先添加到标准库的高频标签
- 发现标准库覆盖的不足之处（如某些新兴地点或文化元素未包含）
- 评估现有标准库与实际内容的匹配度
- 为标准标签库更新提供具体建议
- 识别潜在的趋势或新兴主题（频繁出现但未标准化的标签）

### 5.2 地理标签与用户位置匹配桑基图

#### SQL查询逻辑
```sql
WITH RECURSIVE geo_tags AS (
    SELECT 
        tcr.note_id,
        tcr.llm_name,
        lnd.user_location,
        JSON_EXTRACT(tcr.collected_tags, '$[*]') AS extracted_geo_tags
    FROM tag_comparison_results tcr
    JOIN llm_note_diagnosis lnd ON tcr.note_id = lnd.note_id
    WHERE tcr.tag_type = 'geo' AND lnd.user_location IS NOT NULL
),
tag_unnest AS (
    SELECT 
        note_id,
        llm_name,
        user_location,
        JSON_UNQUOTE(
            JSON_EXTRACT(extracted_geo_tags, CONCAT('$[', numbers.n, ']'))
        ) AS geo_tag
    FROM geo_tags
    JOIN (
        SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL
        SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL
        SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
    ) AS numbers
    WHERE JSON_EXTRACT(extracted_geo_tags, CONCAT('$[', numbers.n, ']')) IS NOT NULL
)
SELECT 
    llm_name,
    user_location,
    geo_tag,
    COUNT(DISTINCT note_id) AS note_count
FROM tag_unnest
GROUP BY llm_name, user_location, geo_tag
HAVING COUNT(DISTINCT note_id) > 1
ORDER BY llm_name, note_count DESC
LIMIT 100;
```

**查询解释：**
- 此查询分析地理标签与用户实际地理位置的关联
- 仅选择标签类型为'geo'且用户位置不为空的记录
- 展开JSON数组中的地理标签
- 按LLM模型名称、用户位置和地理标签分组
- 计算每个组合的唯一笔记数量
- 只保留出现在多个笔记中的组合（>1）

#### 可视化逻辑
桑基图展示用户位置与提取的地理标签之间的流向关系。左侧节点代表用户位置，右侧节点代表提取的地理标签，连线粗细表示关联强度。

#### 如何阅读图表
1. **观察连线粗细**：更粗的连线表示更强的关联
2. **识别主要流向**：从某一用户位置出发的多条线表示该位置用户提及多个地点
3. **注意自环**：如果用户位置与地理标签匹配，会形成位置到相同位置的连线
4. **比较不同模型**：查看不同LLM模型的桑基图，比较提取准确性差异
5. **探索意外连接**：有些用户位置与地理标签的连接可能出乎意料，值得深入分析

#### 可能的结论
- 判断用户是否主要关注自己所在地区的内容
- 识别特定地区用户关注的热门外地地点
- 评估地理标签提取与用户实际位置的一致性
- 发现潜在的旅游模式或兴趣地点
- 优化基于地理位置的内容推荐策略

## 6. 标签差异评估可视化

### 6.1 模型标签提取差异蝴蝶图

#### SQL查询逻辑
```sql
WITH model_scores AS (
    SELECT 
        note_id,
        tag_type,
        llm_name,
        weighted_score
    FROM tag_comparison_results
    WHERE tag_type IN ('geo', 'cultural')  -- 选择主要标签类型
)
SELECT 
    m1.note_id,
    m1.tag_type,
    m1.llm_name AS model1,
    m2.llm_name AS model2,
    m1.weighted_score AS score1,
    m2.weighted_score AS score2,
    (m1.weighted_score - m2.weighted_score) AS score_diff
FROM model_scores m1
JOIN model_scores m2 
    ON m1.note_id = m2.note_id 
    AND m1.tag_type = m2.tag_type 
    AND m1.llm_name < m2.llm_name
ORDER BY ABS(score_diff) DESC
LIMIT 100;
```

**查询解释：**
- 此查询比较相同笔记上不同LLM模型的标签提取得分差异
- 通过自连接创建模型对比，`m1.llm_name < m2.llm_name`确保每对模型只比较一次
- 计算得分差异（score_diff = score1 - score2）
- 结果按差异绝对值降序排列，首先展示差异最大的案例
- 限制返回100条记录，避免结果过多

#### 可视化逻辑
蝴蝶图（散点图）比较两个模型在相同笔记上的得分差异。X轴为第一个模型得分，Y轴为第二个模型得分，点的颜色表示差异大小和方向。

#### 如何阅读图表
1. **观察对角线分布**：沿对角线分布的点表示两个模型表现相似
2. **对角线上方区域**：此区域的点表示模型2（Y轴）得分高于模型1（X轴）
3. **对角线下方区域**：此区域的点表示模型1（X轴）得分高于模型2（Y轴）
4. **颜色区分**：
   - 蓝色点表示模型1得分高于模型2
   - 红色点表示模型2得分高于模型1
   - 颜色深浅表示差异大小
5. **查看平均差异**：图表底部注释显示平均差异值，反映整体趋势

#### 可能的结论
- 判断哪个模型在特定标签类型上整体表现更好
- 识别模型表现高度不一致的案例（远离对角线的点）
- 发现可能的模型偏好或擅长领域
- 评估模型间的整体性能差距（平均差异）
- 为模型选择和优化提供依据

### 6.2 Embedding模型标签理解差异箱型图

#### SQL查询逻辑
```sql
SELECT 
    t1.note_id,
    t1.tag_type,
    t1.llm_name,
    t1.compare_model_name AS embed_model1,
    t2.compare_model_name AS embed_model2,
    t1.weighted_score AS score1,
    t2.weighted_score AS score2,
    (t1.weighted_score - t2.weighted_score) AS score_diff
FROM tag_comparison_results t1
JOIN tag_comparison_results t2 
    ON t1.note_id = t2.note_id 
    AND t1.tag_type = t2.tag_type 
    AND t1.llm_name = t2.llm_name
    AND t1.compare_model_name < t2.compare_model_name
ORDER BY ABS(score_diff) DESC
LIMIT 100;
```

**查询解释：**
- 此查询比较相同LLM模型下不同Embedding模型的性能差异
- 条件确保比较的是相同笔记、相同标签类型和相同LLM模型下的不同Embedding模型
- `t1.compare_model_name < t2.compare_model_name`确保每对Embedding模型只比较一次
- 计算得分差异并按差异绝对值降序排列
- 限制返回100条记录，避免结果过多

#### 可视化逻辑
并排箱型图比较两个Embedding模型在相同条件下的得分分布。每个箱型图显示一个模型的得分分布，包括中位数、四分位数和异常值。

#### 如何阅读图表
1. **比较箱体位置**：更高的箱体表示该Embedding模型整体表现更好
2. **观察箱体高度**：箱体越短，得分分布越集中；越长，分布越分散
3. **检查中位线**：箱体中间的横线代表中位数，反映典型表现
4. **观察异常点**：箱体外的点表示异常值，可能是特别好或特别差的案例
5. **比较子图**：每个LLM模型和标签类型组合有一组子图，可对比不同条件下的表现

#### 可能的结论
- 判断在特定LLM模型和标签类型下哪种Embedding模型整体表现更好
- 评估Embedding模型的稳定性（分布集中度）
- 识别需要进一步调查的异常案例
- 为不同任务选择最适合的Embedding模型
- 判断Embedding模型与LLM模型之间的兼容性

## 7. 标签分析结果摘要可视化

#### SQL查询逻辑
```sql
SELECT 
    'LLM模型性能' AS analysis_type,
    COUNT(DISTINCT llm_name) AS model_count,
    ROUND(AVG(weighted_score), 3) AS avg_overall_score,
    MIN(weighted_score) AS min_score,
    MAX(weighted_score) AS max_score
FROM tag_comparison_results
UNION ALL
SELECT 
    'Embedding模型性能' AS analysis_type,
    COUNT(DISTINCT compare_model_name) AS model_count,
    ROUND(AVG(weighted_score), 3) AS avg_overall_score,
    MIN(weighted_score) AS min_score,
    MAX(weighted_score) AS max_score
FROM tag_comparison_results
WHERE compare_model_name IS NOT NULL
UNION ALL
SELECT 
    CONCAT('标签类型: ', tag_type) AS analysis_type,
    COUNT(DISTINCT note_id) AS note_count,
    ROUND(AVG(weighted_score), 3) AS avg_overall_score,
    MIN(weighted_score) AS min_score,
    MAX(weighted_score) AS max_score
FROM tag_comparison_results
GROUP BY tag_type;
```

**查询解释：**
- 此查询创建一个总结报告，包含三部分：LLM模型整体性能、Embedding模型整体性能和按标签类型的性能
- 每部分计算相关记录的数量、平均加权得分、最小得分和最大得分
- 使用`UNION ALL`组合结果
- 对于LLM模型，统计不同模型的数量；对于标签类型，统计不同笔记的数量

#### 可视化逻辑
条形图展示不同分析类型的平均加权得分，带有误差线表示得分范围（最小值到最大值）。每个条形代表一个分析类型，高度表示平均得分。

#### 如何阅读图表
1. **比较条形高度**：更高的条形表示该类别平均得分更高
2. **观察误差线**：较长的误差线表示得分范围较大，说明存在较大变化
3. **查看样本量标注**：条形中的"n=XX"表示各类别的样本数量
4. **比较不同类别**：对比不同模型类型和标签类型的整体表现

#### 可能的结论
- 确定整体表现最好的模型类型（LLM or Embedding）
- 识别得分最高的标签类型（如地理标签可能比文化标签更准确）
- 判断得分分布的一致性（通过误差线长短）
- 了解系统整体表现水平（通过平均得分）
- 制定进一步优化的方向（改进表现较差的模型或标签类型）

## 综合应用建议

1. **系统性分析流程**
   - 先从摘要结果了解整体情况
   - 深入研究模型性能对比
   - 分析标签内容分布和特点
   - 探索标签与笔记特征的关联
   - 最后确定优化方向和策略

2. **优先改进方向识别**
   - 关注得分最低的模型或标签类型
   - 分析低质量标签的共同特征
   - 识别标准库中的缺失标签
   - 优化对特定内容类型的标签提取

3. **实际应用调整**
   - 根据不同标签类型选择最适合的模型组合
   - 针对不同内容倾向采用不同的标签提取策略
   - 持续更新标准标签库，增加高频率出现的标签
   - 定期重新评估模型性能，跟踪改进效果

4. **自定义分析扩展**
   - 根据业务需求调整SQL查询参数
   - 为特定项目创建定制化图表
   - 将分析结果整合到监控仪表板
   - 设置定期分析任务，跟踪长期趋势

通过对这些可视化图表的综合分析，您将能够全面了解标签系统的性能，识别关键问题和优化机会，最终提高小红书品牌调研的准确性和有效性。