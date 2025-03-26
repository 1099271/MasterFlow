# MasterFlow 核心代码逻辑说明

## 系统架构概述

MasterFlow 是一个基于 FastAPI 开发的市场营销工作流管理系统，主要用于小红书数据的采集、分析和管理。系统采用了典型的三层架构：

1. **表示层**：API 接口层，处理 HTTP 请求和响应
2. **业务逻辑层**：服务层，实现核心业务逻辑
3. **数据访问层**：数据库操作层，负责数据的存取和查询

整体采用了 Python 异步编程模型，结合 SQLAlchemy ORM 实现高效的数据库操作。

## 核心模块及其功能

### 1. 小红书数据采集模块 (XhsService)

该模块负责从小红书平台采集数据，包括笔记、评论、作者信息等。

#### 主要功能：

- **关键词搜索**：通过关键词搜索相关笔记
- **获取笔记详情**：根据笔记 ID 获取笔记详细内容和图片
- **获取笔记评论**：采集特定笔记下的评论和回复
- **获取作者信息**：获取作者的详细信息和发布的笔记
- **话题讨论量采集**：获取特定话题的讨论量数据

#### 实现逻辑：

```python
# 简化版实现逻辑
class XhsService:
    # 初始化，设置请求头和会话
    def __init__(self):
        self.headers = {...}  # 请求头设置
        self.session = aiohttp.ClientSession()  # 异步HTTP会话
    
    # 搜索小红书笔记
    async def search_notes(self, keyword, page=1):
        # 构建请求，发送搜索API请求
        # 解析响应，保存笔记信息到数据库
        
    # 获取笔记详情
    async def get_note_detail(self, note_id):
        # 请求特定笔记的详情API
        # 解析响应，保存详情到数据库
        
    # 获取笔记评论
    async def get_note_comments(self, note_id, cursor=""):
        # 请求评论API，支持分页
        # 解析响应，保存评论到数据库
        
    # 话题讨论量采集
    async def get_topic_discussions(self, topic_name):
        # 请求话题API
        # 解析并保存话题讨论量数据
```

### 2. 标签分析服务 (TagService)

该模块负责对小红书笔记内容进行标签提取和分析，使用大语言模型和向量嵌入技术。

#### 主要功能：

- **标签提取**：使用大语言模型从笔记内容中提取关键标签
- **标签相似度比较**：比较不同标签组之间的语义相似度
- **标签管理**：管理标准标签库和提取的标签

#### 实现逻辑：

```python
class TagService:
    def __init__(self, model_name='distiluse-v2'):
        # 初始化标签分析器和数据访问对象
        self.analyzer = TagSimilarityAnalyzer(model_name=model_name)
        self.tag_dao = TagDAO()
    
    # 从笔记中提取标签
    def make_tags_from_note(self, note_id: str):
        # 获取笔记内容
        # 调用LLM服务提取标签
        # 存储结果到数据库
        
    # 比较标签相似度并保存
    def compare_and_save_tags(self, note_id, llm_name, collected_tags):
        # 获取标准标签
        # 调用分析器比较相似度
        # 保存比较结果
        
    # 分析标签相似度
    def analyse_tag_similarity(self, note_id=None):
        # 获取标签数据
        # 分析相似度
        # 返回分析结果
```

### 3. 标签相似度分析器 (TagSimilarityAnalyzer)

负责使用向量嵌入模型计算标签之间的语义相似度。

#### 主要功能：

- **标签编码**：将标签转换为向量表示
- **相似度计算**：计算不同标签之间的余弦相似度
- **相似度可视化**：生成相似度矩阵热图

#### 实现逻辑：

```python
class TagSimilarityAnalyzer:
    def __init__(self, model_name='distiluse-v2'):
        # 加载预训练模型
        self.model_name = model_name
        self.model = self._load_model(model_name)
        
    # 比较标签组相似度
    def compare_tags(self, collected_tags, standard_tags, visualize=False):
        # 将标签转换为向量
        # 计算相似度矩阵
        # 计算多种相似度指标
        # 可选：可视化相似度矩阵
        
    # 编码标签为向量表示
    def _encode_tags(self, tags):
        # 根据不同模型要求处理标签文本
        # 返回标签的向量表示
        
    # 计算相似度指标
    def _calculate_scores(self, similarity_matrix):
        # 计算不同的相似度度量：最大匹配、匈牙利算法等
        # 返回综合评分
```

### 4. 大语言模型服务 (LlmService)

负责调用各种大语言模型进行文本分析和处理。

#### 主要功能：

- **标签提取**：从笔记内容中提取关键标签
- **笔记分析**：分析笔记内容，生成结构化信息
- **结果存储**：保存大模型分析结果

#### 实现逻辑：

```python
class LlmService:
    @staticmethod
    def request_llm(llm_alias, prompt, log_file_prefix=None):
        # 根据不同的模型别名选择不同的模型接口
        # 发送请求，获取模型响应
        # 可选：记录请求和响应日志
        
    @staticmethod
    def store_note_diagnosis(note_id, llm_alias, diagnosis_data):
        # 将分析结果保存到数据库
        # 返回保存状态
```

### 5. 话题服务 (TopicService)

负责小红书话题数据的采集和分析。

#### 主要功能：

- **话题搜索**：搜索特定话题
- **话题讨论量采集**：获取话题的讨论量
- **话题数据分析**：分析话题热度变化趋势

#### 实现逻辑：

```python
class TopicService:
    def __init__(self):
        # 初始化服务
        
    # 采集话题讨论量
    async def collect_topic_discussions(self, topic_names):
        # 循环请求每个话题的数据
        # 解析并保存到数据库
        
    # 获取话题讨论量历史数据
    def get_topic_discussion_history(self, topic_name, days=30):
        # 查询特定时间范围内的话题讨论量数据
        # 返回时间序列数据
```

## 数据流处理逻辑

系统中的数据处理流程如下：

1. **数据采集流程**：
   ```
   关键词/话题/作者 → XhsService采集 → 保存到数据库 → 触发后续分析
   ```

2. **标签分析流程**：
   ```
   笔记内容 → LlmService提取标签 → TagService分析 → 结果保存与展示
   ```

3. **标签比较流程**：
   ```
   提取的标签 + 标准标签 → TagSimilarityAnalyzer比较 → 生成相似度指标 → 结果展示
   ```

4. **话题分析流程**：
   ```
   话题名称 → TopicService采集数据 → 时间序列分析 → 趋势展示
   ```

## 系统关键技术实现

### 1. 异步请求处理

系统大量使用 Python 的异步编程模型，提高并发能力：

```python
# 异步函数示例
async def batch_process(items):
    tasks = []
    for item in items:
        tasks.append(process_item(item))
    return await asyncio.gather(*tasks)

# 使用信号量控制并发
async def process_with_concurrency(items, concurrency=5):
    semaphore = asyncio.Semaphore(concurrency)
    async def process_with_limit(item):
        async with semaphore:
            return await process_item(item)
    
    tasks = [process_with_limit(item) for item in items]
    return await asyncio.gather(*tasks)
```

### 2. 向量嵌入和相似度计算

使用 SentenceTransformers 进行标签的向量表示和相似度计算：

```python
def calculate_similarity(tag_group1, tag_group2):
    # 编码标签
    embeddings1 = model.encode(tag_group1)
    embeddings2 = model.encode(tag_group2)
    
    # 计算余弦相似度
    similarity_matrix = cosine_similarity(embeddings1, embeddings2)
    
    # 应用匈牙利算法找到最佳匹配
    row_ind, col_ind = linear_sum_assignment(-similarity_matrix)
    optimal_score = similarity_matrix[row_ind, col_ind].mean()
    
    return optimal_score
```

### 3. 大语言模型集成

系统支持多种大语言模型，并使用统一的接口进行调用：

```python
def request_llm(llm_alias, prompt):
    if llm_alias == "model1:provider1":
        return call_model1_api(prompt)
    elif llm_alias == "model2:provider2":
        return call_model2_api(prompt)
    else:
        return call_default_model(prompt)
```

## 系统扩展性设计

1. **模型可插拔**：支持不同的向量嵌入模型和大语言模型
2. **数据源可扩展**：除小红书外，可扩展支持其他平台的数据采集
3. **分析算法可定制**：可以添加新的标签分析和比较算法

## 性能优化策略

1. **数据库查询优化**：
   - 使用适当的索引
   - 优化复杂查询
   - 实施数据分页

2. **并发控制**：
   - 使用信号量限制并发请求数
   - 实施重试机制和错误处理

3. **缓存策略**：
   - 对频繁请求的数据实施缓存
   - 使用 Redis 缓存中间结果

## 系统限制与注意事项

1. **API 限制**：
   - 需注意第三方 API 的请求频率限制
   - 实施请求速率控制，避免被封禁

2. **数据一致性**：
   - 确保异步操作中的数据一致性
   - 使用事务处理关键操作

3. **资源消耗**：
   - 向量模型可能消耗大量内存，需注意服务器配置
   - 大语言模型调用成本较高，需优化使用频率 