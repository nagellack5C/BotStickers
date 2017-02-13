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


chrome_path = "YOURPATH" #replace with your path to Chrome Driver

#preparing URL for Selenium
url_base = "https://www.parazitakusok.ru/catalog/stickers-and-stickerpacks/stickers/?page="
url_page = 1
url_finish = "&view=30"
have_pages = False
max_page = 0

#Function to get the amount of pages in the category
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
#Changes to True when the max page is reached

#Numerates current sticker to put an ID to the DB. Not sure if necessary
sticker_id = 0


while stop_hammertime == False:
    
    print(url_page) #for debug purposes
    
    #Creating the URL with incrementing page number
    url = url_base + str(url_page) + url_finish
    
    driver.get(url)
    
    
    try:
        #Waits for the images in main-content class to be uploaded by Selenium.
        elem = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/ul/li[1]/div[1]/div/a/img"))
        )
        element_located = True
    except:
        #Something goes wrong
        print("Fail!")
    finally:
        if element_located == True:
            
            #gets amount of pages if not done yet
            if have_pages == False:
                get_pages(driver)
                have_pages = True
                
            #retrieves all items (i.e. stickers) from the category page
            sticker_frames = driver.find_elements_by_class_name("new-item")
            
            #gets URLs for the image and author page and sticker name for each item. TBD item URL.
            for frame in sticker_frames:
                picture_html = frame.find_element_by_tag_name("img")
                picture = picture_html.get_attribute("src")
                author_html = frame.find_element_by_class_name("new-product-info-painter")
                author = author_html.find_element(By.TAG_NAME, "a").get_attribute("href")
                name_html = frame.find_element_by_class_name("new-product-info-title")
                name = name_html.text
                listicle=[]
                listicle.append((sticker_id, picture, author, name, 0))
                for i in listicle:
                    print(i)
                #puts the information found into DB
                c.executemany("INSERT INTO stickers (id, img, author, name, rating) VALUES (?,?,?,?,?)", listicle)
                sticker_id += 1
        url_page += 1
        conn.commit() #commits are made for each page parsed to protect from errors in parsing
        if url_page == max_page:
            stop_hammertime = True


conn.commit()
conn.close()
driver.close()
