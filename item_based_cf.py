import math
import numpy as np
from collections import defaultdict


# 유저별 관심사항
users_interests = [
    ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
    ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
    ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
    ["R", "Python", "statistics", "regression", "probability"],
    ["machine learning", "regression", "decision trees", "libsvm"],
    ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
    ["statistics", "probability", "mathematics", "theory"],
    ["machine learning", "scikit-learn", "Mahout", "neural networks"],
    ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
    ["Hadoop", "Java", "MapReduce", "Big Data"],
    ["statistics", "R", "statsmodels"],
    ["C++", "deep learning", "artificial intelligence", "probability"],
    ["pandas", "R", "Python"],
    ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
    ["libsvm", "regression", "support vector machines"]
]

# 코사인 유사도를 구하는 함수,
# 유사도가 높을수록 1 낮을수록 0
def cosine_similarity(v, w):
    return np.dot(v, w) / math.sqrt(np.dot(v, v) * np.dot(w, w))

# user_interests를 가지고 전체 관심사 목록을 만든 후
# 각 관심사에 인덱스 번호 부여,
# list에 넣고 정렬
unique_interests = sorted(list({interest
                                for user_interests in users_interests
                                for interest in user_interests}))

# 위에서 만든 list로 각 사용자의 관심사 벡터를 생성
def make_user_interest_vector(user_interests):
    """given a list of interests, produce a vector whose ith element is 1
    if unique_interests[i] is in the list, 0 otherwise"""

    # 사용자가 해당 관심사 가지고있으면 1, 없으면 0
    return [1 if interest in user_interests else 0
            for interest in unique_interests]

user_interest_vectors = [make_user_interest_vector(user_interests)
                        for user_interests in users_interests]

user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
                    for interest_vector_j in user_interest_vectors]
                    for interest_vector_i in user_interest_vectors]

# (코사인 유사도를 구하기 위해서)
# 사용자-관심사 행렬의 전치행렬
interest_user_matrix = [[user_interest_vector[j]
                         for user_interest_vector in user_interest_vectors]
                        for j, _ in enumerate(unique_interests)]

# 코사인 유사도를 적용하는 함수
# 동일한 사용자들의 집합이 두 관심사에 관심이 있으면 이 관심사들의 유사도는 1, 아니면 0
interest_similarities = [[cosine_similarity(user_vector_i, user_vector_j)
                           for user_vector_j in interest_user_matrix]
                          for user_vector_i in interest_user_matrix]

# 가장 유사한 관심사를 구한 후 정렬
def most_similar_interests_to(interest_id):
    similarities = interest_similarities[interest_id]
    pairs = [(unique_interests[other_interest_id], similarity)
             for other_interest_id, similarity in enumerate(similarities)
             if interest_id != other_interest_id and similarity > 0]

    return sorted(pairs,
                  key=lambda pair: pair[-1],
                  reverse=True)

print("사용자 0의 관심사와 유사도 :")
print(most_similar_interests_to(0))

# 사용자의 관심사와 유사한 관심사들의 유사도를 모두 더함
def item_based_suggestions(user_id:int, include_current_interests:bool=False):
    # 비슷한 관심사를 더함
    suggestions = defaultdict(float)
    user_interest_vector = user_interest_vectors[user_id]
    for interest_id, is_interested in enumerate(user_interest_vector):
        if is_interested == 1:
            similar_interests = most_similar_interests_to(interest_id)
            for interest, similarity in similar_interests:
                suggestions[interest] += similarity

    # 가중치를 기준으로 내림차순으로 정렬
    suggestions = sorted(suggestions.items(),
                         key=lambda pair:pair[-1],
                         reverse=True)

    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight)
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]]

print("사용자 0에게 주어지는 추천 목록 : ")
print(item_based_suggestions(0, False))