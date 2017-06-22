from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from pykeyboard import PyKeyboard
import urllib.request
from bs4 import BeautifulSoup
import random
from PIL import Image

#set up mobile emulation
mobile_emulation = {"deviceName": "Google Nexus 5"}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome(desired_capabilities = chrome_options.to_capabilities())
#set up an actionchain for general keypresses
actions = ActionChains(driver)

#set up keyboard for uploading files
k = PyKeyboard()
filenamelist = []
photocount = 1
maxfollows = 50 
followdelay = 10
userlist = ["hopperclodder"]
famoususerlist = ["memes","daquan","whalemart","taylorswift","instagram",
"selenagomez","arianagrande"]

def login(username, password): #minimum time: 2 seconds, assumes you are not logged in already
    driver.delete_all_cookies()
    driver.get("https://www.instagram.com") #go to instagram.com
    loginlink = driver.find_element_by_class_name("_fcn8k") #go to the login page from the signup page
    loginlink.click()
    usernamebox = driver.find_element_by_name("username")
    usernamebox.send_keys(username)
    passwordbox = driver.find_element_by_name("password")
    passwordbox.send_keys(password,Keys.ENTER)
    #wait for login to take effect
    time.sleep(1)
    #skip past the "download app" page
    driver.get("https://www.instagram.com/")
    time.sleep(1)
    print("logged into "+username)


def postphoto(filename, caption): #minimum time 7.5 seconds, assumes you are logged in
    time.sleep(1)
    #click post photo button
    camera_icon = driver.find_element_by_xpath("//div[@class='_o5rm6 coreSpriteCameraInactive']")
    #camera_icon.send_keys("~/Desktop/python/ifunny/images/image2.jpeg")
    camera_icon.click()

    #navigate in the native file browser using pykeyboard simulated inputs
    time.sleep(1) #wait for window to pop up
    k.tap_key(k.left_key) #tap left arrow key to go to side menu
    k.tap_key(k.up_key) #tap up arrow key to get to search
    k.type_string(filename) #search for the file name
    k.tap_key(k.enter_key) #press enter to search
    k.tap_key(k.down_key,n=2,interval=0.5) #tap the down key twice to select the image
    k.tap_key(k.enter_key) #press enter to open the image
    
    time.sleep(1) #wait for the photo to load
    next_button = driver.find_element_by_class_name("_cb8v1")
    next_button.click()
    
    time.sleep(0.5) #wait for the next page to load
    #type the caption 
    caption_textbox = driver.find_element_by_class_name("_8od8r")
    caption_textbox.click()
    caption_textbox.send_keys(caption)
    #post the photo
    post_button = driver.find_element_by_class_name("_cb8v1")
    post_button.click()
    
    time.sleep(5) #delay to let page load

def getmemesfromifunny():
    global photocount
    global filenamelist
    filenamelist = []

    filename_seed = random.randint(1000,9999)
    url = "https://ifunny.co/"

    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html,'html.parser')

    for link in soup.find_all("img", class_="media__image"):
        filename = 'image'+str(filename_seed+photocount)+'.jpeg'
        filenamelist.append(filename)
        urllib.request.urlretrieve(link.get('src'),'./photos/'+filename) #downloads photo into the photos folder in current directory
        #crop out the ifunny watermark and resize the photo
        meme = Image.open('./photos/'+filename)
        width = meme.size[0]
        height = meme.size[1]
        meme = meme.crop((
            0,
            0,
            width,
            height-20,
        ))
        meme = meme.resize((1080,1035))
        
        meme.save('./photos/'+filename)
        photocount = photocount+1
    print("memes retrieved")

def followpeople(popularuser):
     ##navigate to a popular user
    driver.get("https://www.instagram.com/"+popularuser)
    ##click on the followers list of user
    ##find all follow buttons in the list of followers
    global followdelay

    try:
        followpage = driver.find_elements_by_xpath("//*[contains(text(), 'followers')]")
        followpage[0].click()


        actions = ActionChains(driver)


        time.sleep(1)
        print("attempting to follow people from: "+popularuser)
        followbuttons = driver.find_elements_by_xpath("//*[contains(text(),'Follow')]")
        followcount = 1
        for button in followbuttons:
            button.click()
            driver.execute_script("window.scrollTo(0, "+str(51.37*followcount)+");")

            followcount += 1
            if (followcount == 20):
                break

            time.sleep(followdelay)
            followdelay = random.randint(5,15)
    except Exception as inst:
        print("error")
                
    
    
def unfollowall(loggedinuser,unfollowedcount):
    driver.get("https://www.instagram.com/"+loggedinuser)

    followingpage = driver.find_element_by_xpath("//button[text(), 'following']")
    followingpage[0].click()

    time.sleep(1)

    unfollowbuttons = driver.find_elements_by_xpath("//*[contains(text(),'Following')]")
    for button in unfollowbuttons:
        button.click()
        driver.execute_script("window.scrollTo(0, "+str(51.37*unfollowedcount)+");")
        unfollowedcount += 1
        time.sleep(followdelay)

    if(unfollowedcount == 100):
        print("unfollowed 100 people")
    else:
        unfollowall(loggedinuser,unfollowedcount)


    

#begin control code
login("username","password")
#getmemesfromifunny()
#for file in filenamelist:
#    postphoto(file,"follow @hopperclodder for more                                              .                                                   .                                                    .                                        .                                   #followme #follow #funnymemes #funny #jokes #lol #comic #comedy #haha #joke #petty #savage #famous #branding #funnyvideo #funnypictures #instafunny #funnypicture #hahaha #funnyvideos #viral #hilarious #promo #advertising #advertise #promote #nochill #lmao #memes #xbox")

#    print("posted "+file)
#    time.sleep(random.randint(2,10))


getmemesfromifunny()
for file in filenamelist:
    postphoto(file,"follow @hopperclodder for more                                              .                                                   .                                                    .                                        .                                   #followme #follow #funnymemes #funny #jokes #lol #comic #comedy #haha #joke #petty #savage #famous #branding #funnyvideo #funnypictures #instafunny #funnypicture #hahaha #funnyvideos #viral #hilarious #promo #advertising #advertise #promote #nochill #lmao #memes #xbox")
    
    print("posted "+file)
    time.sleep(random.randint(5,10))


