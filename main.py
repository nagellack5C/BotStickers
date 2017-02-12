import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3

conn = sqlite3.connect("example.db")
c = conn.cursor()
c.execute('''CREATE TABLE stickers (id int, img text, author text, name text, rating int)''')


chrome_path = "C:/Users/fatsu/Documents/newsite/chromedriver.exe"
phantomjs_path = "C:/Users/fatsu/AppData/Roaming/npm/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs.exe"
testtxt_path = "C:/Users/fatsu/Documents/newsite/test.txt"

url_base = "https://www.parazitakusok.ru/catalog/stickers-and-stickerpacks/stickers/?page="
url_page = 1
url_finish = "&view=30"
have_pages = False
max_page = 0

def get_pages(driver):
    global max_page
    for li in driver.find_element_by_class_name("navigation").find_elements_by_tag_name("li"):
        if li.get_attribute("class") != "disabled":
            page = int(li.find_element_by_tag_name("a").get_attribute("data-pagi"))
            if page > max_page:
                max_page = page
    print(max_page)

driver = webdriver.Chrome(chrome_path, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])

stop_hammertime = False
sticker_id = 0
stickers = {}

while stop_hammertime == False:
    url = url_base + str(url_page) + url_finish
    print(url)
    driver.get(url)
    #driver.implicitly_wait(10)
    try:
        elem = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/ul/li[1]/div[1]/div/a/img"))
        )
        kek = True
    except:
        print("huesosina")
    finally:
        if kek == True:
            if have_pages == False:
                get_pages(driver)
                have_pages = True
            sticker_frames = driver.find_elements_by_class_name("new-item")
            for frame in sticker_frames:
                picture_html = frame.find_element_by_tag_name("img")
                picture = picture_html.get_attribute("src")
                author_html = frame.find_element_by_class_name("new-product-info-painter")
                author = author_html.find_element(By.TAG_NAME, "a").get_attribute("href")
                name_html = frame.find_element_by_class_name("new-product-info-title")
                name = name_html.text
                #print(picture, author, name)
                stickers[str(sticker_id)] = [picture, author, name]
                listicle=[]
                listicle.append((sticker_id, picture, author, name, 0))
                for i in listicle:
                    print(i)
                c.executemany("INSERT INTO stickers (id, img, author, name, rating) VALUES (?,?,?,?,?)", listicle)
                sticker_id += 1

        #for i in stickers:
            #print(i, stickers[i])
        url_page += 1
        #stop_hammertime = True
        conn.commit()
        if url_page == max_page:
            stop_hammertime = True


conn.commit()
conn.close()
driver.close()