import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.optimize import linear_sum_assignment

class TagSimilarityAnalyzer:
    """标签组相似度分析工具"""
    
    def __init__(self, model_name='distiluse-v2'):
        """
        初始化标签相似度分析器
        
        Args:
            model_name: 使用的预训练模型名称
        """
        self.model_name = model_name
        self.model = self._load_model(model_name)
        
    def _load_model(self, model_name):
        """加载指定的模型"""
        if model_name == 'bge':
            # 对于 BAAI/bge-large-zh-v1.5 模型，我们需要特殊处理
            return SentenceTransformer('BAAI/bge-large-zh-v1.5', device='cuda')
        else:
            return SentenceTransformer('distiluse-base-multilingual-cased-v2')

    def compare_tags(self, collected_tags, standard_tags, visualize=False):
        """
        比较收集的标签与标准标签的相似度
        
        Args:
            collected_tags: 收集的标签列表
            standard_tags: 标准标签列表
            visualize: 是否可视化相似度矩阵
            
        Returns:
            包含各种相似度指标的字典
        """
        if not collected_tags or not standard_tags:
            return {
                "score": 0,
                "message": "标签列表为空",
                "detailed_scores": {},
                "collected_tags": collected_tags or [],
                "standard_tags": standard_tags or [],
                "similarity_matrix": np.array([[0]])
            }
            
        # 将标签转换为向量
        collected_embeddings = self._encode_tags(collected_tags)
        standard_embeddings = self._encode_tags(standard_tags)
        
        # 确保向量是二维数组
        if len(collected_embeddings.shape) == 1:
            collected_embeddings = collected_embeddings.reshape(1, -1)
        if len(standard_embeddings.shape) == 1:
            standard_embeddings = standard_embeddings.reshape(1, -1)
        
        # 计算相似度矩阵
        similarity_matrix = cosine_similarity(collected_embeddings, standard_embeddings)
        
        # 计算多种相似度指标
        scores = self._calculate_scores(similarity_matrix)
        
        # 计算加权总分
        weighted_score = self._calculate_weighted_score(scores)
        
        # 可视化相似度矩阵
        if visualize:
            self._visualize_similarity_matrix(
                similarity_matrix, 
                collected_tags, 
                standard_tags
            )
        
        return {
            "score": weighted_score,
            "detailed_scores": scores,
            "similarity_matrix": similarity_matrix,
            "collected_tags": collected_tags,
            "standard_tags": standard_tags
        }

    def _encode_tags(self, tags):
        """编码标签，处理不同模型的特殊需求"""
        if self.model_name == 'BAAI/bge-large-zh-v1.5':
            # 对于 BAAI/bge-large-zh-v1.5 模型，需要添加特殊前缀
            return self.model.encode([f"给出以下文本的意思：{tag}" for tag in tags])
        else:
            return self.model.encode(tags)

    def _calculate_scores(self, similarity_matrix):
        """计算多种相似度指标"""
        
        # 1. 最大匹配法：每个收集标签与最相似的标准标签匹配
        max_similarity = np.mean(np.max(similarity_matrix, axis=1))
        
        # 2. 匈牙利算法（最优匹配）：整体最优的一对一匹配
        row_ind, col_ind = linear_sum_assignment(-similarity_matrix)
        optimal_matching = similarity_matrix[row_ind, col_ind].mean()
        
        # 3. 阈值匹配：相似度超过阈值(0.7)的标签对数量占比
        threshold_matching = np.mean(similarity_matrix >= 0.7)
        
        # 4. 平均相似度：所有标签对的平均相似度
        average_similarity = np.mean(similarity_matrix)
        
        # 5. 标签覆盖率：有相似标签(>0.5)的标准标签比例
        coverage = np.mean(np.max(similarity_matrix, axis=0) > 0.5)
        
        return {
            "max_similarity": max_similarity,
            "optimal_matching": optimal_matching,
            "threshold_matching": threshold_matching,
            "average_similarity": average_similarity,
            "coverage": coverage
        }
    
    def _calculate_weighted_score(self, scores):
        """计算加权总分"""
        weights = {
            "max_similarity": 0.3,
            "optimal_matching": 0.3,
            "threshold_matching": 0.1,
            "average_similarity": 0.1,
            "coverage": 0.2
        }
        
        return sum(score * weights[metric] for metric, score in scores.items())
    
    def _visualize_similarity_matrix(self, matrix, collected_tags, standard_tags):
        """可视化相似度矩阵"""
        plt.figure(figsize=(12, 8))
        sns.heatmap(matrix, annot=True, fmt=".2f", 
                    xticklabels=standard_tags, 
                    yticklabels=collected_tags)
        plt.title(f"标签相似度矩阵")
        plt.xlabel("标准标签")
        plt.ylabel("收集标签")
        plt.tight_layout()
        plt.show()
        
    def get_interpretation(self, score):
        """根据得分提供解释"""
        if score >= 0.8:
            return "非常相似，高度匹配"
        elif score >= 0.6:
            return "相似度较高，匹配良好"
        elif score >= 0.4:
            return "中等相似度，部分匹配"
        elif score >= 0.2:
            return "相似度较低，匹配较少"
        else:
            return "几乎不相似，几乎不匹配"