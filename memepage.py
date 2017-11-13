from selenium import webdriver
from selenium.webdriver.common.by import By
from pykeyboard import PyKeyboard
import urllib.request
from bs4 import BeautifulSoup
from random import randint
from PIL import Image
import time
import os
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)
    args = parser.parser_args()

    memes = getmemesfromifunny()

    mobile_emulation = { "deviceName": "Nexus 5" }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    k = PyKeyboard()

    login(driver, args.username, args.password)
    time.sleep(5)

    with open("captions.txt", "r") as f:
        captions = f.readlines()

    post(driver, k, memes[randint(0, len(memes)-1)], captions[randint(0, len(captions)-1)]%"@tlamemes")
    #for file in memes:
        #post(driver, k, file, captions[randint(0, len(captions)-1)]%"@tlamemes")
        #print(file)
        #time.sleep(100)

def login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login")
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_class_name("_qv64e").click()

def post(driver, k, filename, caption):
    print("Trying to post %s, %s" % (filename, caption))
    driver.find_element_by_class_name("coreSpriteFeedCreation").click()
    time.sleep(1)
    k.tap_key(k.left_key)
    #k.tap_key(k.up_key, n=8, interval=0.1)
    k.tap_key(k.enter_key)
    k.press_keys([k.control_key, 'f'])
    k.type_string(filename)
    k.tap_key(k.enter_key)
    time.sleep(1)
    k.tap_key(k.enter_key)
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text()="Next"]').click()
    time.sleep(1)
    driver.find_element_by_class_name("_qlp0q").send_keys(caption)
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text()="Share"]').click()

def getmemesfromifunny():
    filenamelist = []

    path = os.path.dirname(os.path.abspath(__file__))

    response = urllib.request.urlopen("https://ifunny.co/")
    html = response.read()
    soup = BeautifulSoup(html,'html.parser')

    for media_div in soup.find_all("div", class_="post__media"):
        try:
            if(media_div.find(attrs={"data-type":"video"})):
                continue
            link = media_div.find("img", class_="media__image")

        #for link in soup.find_all("img", class_="media__image"):
            filename = 'meme'+str(randint(10000,99999))+'.jpeg'
            urllib.request.urlretrieve(link.get('src'),path+'/photos/'+filename) #downloads photo into the photos folder in current directory
            #crop out the ifunny watermark and resize the photo
            meme = Image.open(path+'/photos/'+filename)
            width = meme.size[0]
            height = meme.size[1]
            meme = meme.crop((
                0,
                0,
                width,
                height-20,
            ))
            meme = meme.resize((1080,1035))
            
            meme.save(path+'/photos/'+filename)
            filenamelist.append(filename)
            print(filename)
        except Exception as e:
            pass
    print("memes retrieved")
    return filenamelist

if __name__ == '__main__':
    main()
