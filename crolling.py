from selenium import webdriver
from bs4 import BeautifulSoup as bs
import sqlite3

# diver 가져오기
driver = webdriver.Chrome('chromedriver.exe')
soup = bs(driver.page_source, 'html.parser')
driver.implicitly_wait(3)

# url 넣기
driver.get('https://www.ypbooks.co.kr/search.yp?catesearch=true&collection=books_kor&sortField=DATE&c3=120301')

# sqlite 연동하기
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

"""
# table 만들기
try:
    cur.execute("CREATE TABLE bookList(genre char(10), title char(30), author char(20), info char(50), keyword char(50))")
except:
    print('already exists')
"""

# 크롤링으로 DB에 도서 데이터 저장
sql = "INSERT INTO blog_bookdata(genre, title, author, info, keyword) VALUES('일본소설', ?, ?, ?, ?)"
while(True):
    count = 0
    for j in range(10):
        count = count + 1
        for i in range(10):
            try:
                soup = bs(driver.page_source, 'html.parser')

                title = (soup.select('div > dl.recom > dl > dt > a')[i].get_text()).strip()
                info = " ".join(soup.select('div > dl.recom > dl.info01')[i].get_text().split())
                author, info = info.split("|", maxsplit=1)
                keyword = " ".join(soup.select('div > dl.recom > dl.keyword')[i].get_text().split())

                bookdatas = [(title, author.strip(), info.strip(), keyword)]
                cur.executemany(sql, bookdatas)
                conn.commit()

            except:
                print("error!")
        if count < 10:
            driver.find_elements_by_css_selector("div.pagination > a.nav")[j].click()
        elif count == 10:
            driver.find_element_by_xpath('//*[@id="search_left"]/form/div[21]/a[12]').click()
conn.close()
print('finish!')

