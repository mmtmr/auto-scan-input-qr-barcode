import json
import cv2, time, os, json, re
from pyzbar import pyzbar
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains

def load_config():
    global config
    with open('config.json', encoding='utf-8') as json_data_file:
        config = json.load(json_data_file)

def send_message_image(discord_webhook_url,img_path):
    discord_message=config["discord_message"]
    webhook = DiscordWebhook(url=discord_webhook_url)

    #Embed image
    with open(img_path, "rb") as f:
        webhook.add_file(file=f.read(), filename='image.png')  
    
    embed=DiscordEmbed(title='QR Code/Barcode Input')
    embed.set_image(url="attachment://image.png")

    split_img_path=img_path.split("-")
    embed.add_embed_field(name='Message', value=discord_message)
    embed.add_embed_field(name='Date', value=split_img_path[-3].split("\\")[-1])
    embed.add_embed_field(name='Time', value=split_img_path[-2])
    embed.add_embed_field(name='Result', value=split_img_path[-1][0:-4])

    webhook.add_embed(embed)

    # with open(img_path, "rb") as f:
    #     webhook.add_file(file=f.read(), filename=img_path)
    
    response = webhook.execute()
    print("Response sent")
    return

def send_message(discord_webhook_url,result):
    discord_message=config["discord_message"]
    webhook = DiscordWebhook(url=discord_webhook_url)
    embed=DiscordEmbed(title='QR Code/Barcode Input')

    #Embed image
    embed.add_embed_field(name='Message', value=discord_message)
    embed.add_embed_field(name='Date', value=datetime.now().strftime("%Y%m%d"))
    embed.add_embed_field(name='Time', value=datetime.now().strftime("%H%M%S"))
    embed.add_embed_field(name='Result', value=result)

    webhook.add_embed(embed)

    # with open(img_path, "rb") as f:
    #     webhook.add_file(file=f.read(), filename=img_path)
    
    response = webhook.execute()
    print("Response sent")
    return



def read_qrcode(last_code,frame):
    regex_format=config['regex_format']
    qrcode = pyzbar.decode(frame)
    if qrcode==[]:
        qrcode_info=-1
    else:
        qrcode_info = qrcode[0].data.decode('utf-8')
        
        if(re.match(regex_format,qrcode_info)):
            if(config['avoid_duplicate']):
                if qrcode_info==last_code:
                    qrcode_info=-1
        else:
            qrcode_info=-1
      
    if qrcode_info!=-1:
        print("QR code of",qrcode_info,"detected")
    return qrcode_info,frame



def input_qrcode (qrcode):
    delay_start_ie=config['delay_start_ie']
    website=config['website']
    input_class_name=config['input_class_name']
    auth_data=config['auth_data']
    print(auth_data)
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    if auth_data!="":
        options.add_argument(auth_data)
    driver = webdriver.Chrome(executable_path="./bin/chromedriver", chrome_options=options)
    wait = WebDriverWait(driver, delay_start_ie)
    time.sleep(1)
    driver.get(website)
    time.sleep(5)
    wait.until(presence_of_element_located((By.CLASS_NAME, input_class_name)))
    driver.find_element_by_class_name(input_class_name).click()
    actions = ActionChains(driver)
    actions.send_keys(qrcode)
    actions.perform()
    return driver



def screenshot_qrcode(driver,qrcode,path):

    #Path name
    now = datetime.now()
    dt = now.strftime("%Y%m%d-%H%M%S")
    img_name=dt+'-'+qrcode+'.png'
    img_name.replace(" ", "")
    
    if(path==""):
        dir = os.path.dirname(__file__)
        img_path=dir+img_name   
    else:
        img_path=path+'\\'+img_name
    
    #Screenshot
    time.sleep(5)
    img = driver.save_screenshot(img_path)
    
    print("Save image")
    return img_path



def main():

    #To detect the camera by its position
    camera_position = config['camera_position']
   
    i=camera_position-1
    camera = cv2.VideoCapture(i)
    ret, frame = camera.read()
    
    #If camera is not found, the program will use the first camera found.
    if ret == False:
        i=0
        while ret == False:       
            camera = cv2.VideoCapture(i)
            ret, frame = camera.read()
            i=i+1
    print("Camera detected at Slot",i+1)
    
    #To read the QR code/Barcode
    website=config['website']
    screenshot_path=config['screenshot_path']
    discord_webhook_url=config['discord_webhook_url']
    delay_start_ie=config['delay_start_ie']
    delay_kill_ie=config['delay_kill_ie']
    last_code=-1
    
    while ret:
        ret, frame = camera.read()
        qrcode_info,frame = read_qrcode(last_code,frame)
        
        if qrcode_info!=-1:
            #Internet explorer will restart every time to input
            if website!="":
                driver=input_qrcode(qrcode_info)
                if config["screenshot"]:
                    img_path=screenshot_qrcode(driver,qrcode_info,screenshot_path)
                    driver.close(); 
                    time.sleep(delay_kill_ie)
                    if discord_webhook_url!="":
                        send_message_image(discord_webhook_url,img_path)
                else:
                    driver.close(); 
                    time.sleep(delay_kill_ie)
                    if discord_webhook_url!="":
                        send_message(discord_webhook_url,qrcode_info)
                last_code=qrcode_info
                qrcode_info=-1
                           
            else:
                file = open("result.txt","a+")#append mode
                file.write(qrcode_info+"\n")
                file.close()
                if discord_webhook_url!="":
                    send_message(discord_webhook_url,qrcode_info)
                last_code=qrcode_info
                qrcode_info=-1
            
    camera.release()

if __name__ == "__main__":
    load_config()
    main()
