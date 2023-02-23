from requests_html import HTMLSession
from bs4 import BeautifulSoup
import sqlite3

connection = sqlite3.connect()
cursor = connection.cursor()


URL = "https://hh.kz/search/vacancy?area=160&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post&hhtmFrom=vacancy_search_list"
session = HTMLSession()
request = session.get(URL)

parsed_content = BeautifulSoup(request.content, "html5lib")


jobs_unprocessed = parsed_content.find_all("div", class_="serp-item")
for jobs in jobs_unprocessed:
    title = jobs.find("a", class_="serp-item__title").text.strip()
    short_info = jobs.find("div",class_="g-user-content").find("div", class_="bloko-text").text.strip()
    cursor.execute("INSERT INTO jobs (?,?)", (title, short_info))
    connection.commit()

connection.close()
