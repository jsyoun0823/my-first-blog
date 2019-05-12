import pandas as pd
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# DB 파일을 Data Frame으로 저장
conn = sqlite3.connect('book.db')
cur = conn.cursor()
metadata = pd.read_sql("SELECT * FROM bookList", conn, index_col=None)
conn.close()

# 키워드 유사도 찾기
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(metadata['keyword'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)
indices = pd.Series(metadata.index, index=metadata['title'])

# 추천 시스템 구현
def get_recommendations(title, cosine_sim = cosine_sim) :
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    book_indices = [i[0] for i in sim_scores]
    return metadata['title'].iloc[book_indices]

# 책 제목 넣으면 10개 책 추천
print(get_recommendations('약사의 혼잣말 1(카니발 플러스)'))
