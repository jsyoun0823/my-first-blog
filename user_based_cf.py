import math
import numpy as np
from collections import defaultdict


# 유저별 관심사항을 리스트로 나타낸 것
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
# 사용자들 간의 유사도 측정
user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
                    for interest_vector_j in user_interest_vectors]
                    for interest_vector_i in user_interest_vectors]

# 유사도가 0인 사람들을 뺀 나머지를 유사도 기준으로 내림차순으로 정렬
def most_similar_users_to(user_id):
    pairs = [(other_user_id, similarity) # find other
        for other_user_id, similarity in # users with
            enumerate(user_similarities[user_id]) # nonzero
        if user_id != other_user_id and similarity > 0] # similarity

    return sorted(pairs, # sort them
            key=lambda pair: pair[-1], # most similar
            reverse=True) # first

print("사용자 0의 유사도가 높은 사용자와 유사도 : ")
print(most_similar_users_to(0))

# 다른 사용자들과의 유사도를 모두 더함
def user_based_suggestions(user_id, include_current_interests=False):
    # 유사도를 다 더함
    suggestions = defaultdict(float)
    for other_user_id, similarity in most_similar_users_to(user_id):
        for interest in users_interests[other_user_id]:
            suggestions[interest] += similarity

    # list로 변환해서 정렬
    suggestions = sorted(suggestions.items(),
                         key = lambda pair: pair[-1],
                         reverse = True)

    # 이미 관심사로 표시된 것들은 제외
    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight)
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]]

print("사용자 0에게 주어지는 추천 목록 : ")
print(user_based_suggestions(0))
