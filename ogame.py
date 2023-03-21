from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import re
import math
import pyautogui
# Create a new Chrome browser instance
driver = webdriver.Chrome()

# Navigate to the website where you want to login using Facebook
driver.get("https://lobby.ogame.gameforge.com/it_IT/")

# Locate the Facebook login button and click on it
wait = WebDriverWait(driver, 10)
login = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginRegisterTabs"]/ul/li[1]')))
login.click()

time.sleep(1)
facebook_login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/p/button[2]')))
facebook_login_button.click()

# Switch to the Facebook login window
main_window = driver.current_window_handle
for handle in driver.window_handles:
    if handle != main_window:
        driver.switch_to.window(handle)
        break

# Enter your Facebook login credentials and click on the "Login" button
time.sleep(1)
accept_button = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@title='Consenti cookie essenziali e facoltativi']")))
accept_button.click()
email_field = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='email']")))
email_field.send_keys("youremail")
password_field = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='pass']")))
password_field.send_keys("yourpassword")
time.sleep(1)
login_button = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="loginbutton"]')))
login_button.click()
#torna sulla finestra principale
driver.switch_to.window(main_window)
gioca=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="joinGame"]/button')))
gioca.click()
#cancella l'altra scheda
parent = driver.window_handles[1]
chld = driver.window_handles[0]
driver.switch_to.window(chld)
time.sleep(3)
driver.close()
# Switch back to the main window
driver.switch_to.window(parent)

#let's start the game
wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[2]/a'))).click()
time.sleep(1)
try:
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ingamepage"]/div[6]/div/div/span[2]/button[2]'))).click()
except:
    print("Couldn't close cookies")
 
pyautogui.keyDown('ctrl')
pyautogui.press('-')
pyautogui.press('-')
pyautogui.press('-')
pyautogui.press('-')
pyautogui.keyUp('ctrl')

time.sleep(1)
##button list:
#       metalup=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[1]/span/button')))
#       cristup=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[2]/span/button')))
#       deutup=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[3]/span/button')))
#       solup=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[4]/span/button')))

#commands
#      metalup.click()
#      cristup.click()
#      deutup.click()
#      solup.click()
#upgrade stuff

##############################
###  RESOURCES
#    span_element = driver.find_element(By.ID, "resources_metal")
#    data_raw = span_element.text.replace(".", "")
#    metal = float(data_raw)
#    #crystal
#    span_element = driver.find_element(By.ID, "resources_crystal")
#    data_raw = span_element.text.replace(".", "")
#    crystal = float(data_raw)
#    #deuterium
#    span_element = driver.find_element(By.ID, "resources_deuterium")
#    data_raw = span_element.text.replace(".", "")
#    deuterium = float(data_raw)
#    #energy
#    span_element = driver.find_element(By.ID, "resources_energy")
#    data_raw = span_element.text.replace(".", "")
#    energy = float(data_raw)
###############################   
###Start variables here
expeditionSentNumber=0
y=0
#AUTOMATIC MINE DEVELOPMENT
def mines():
    x=1
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[2]/a'))).click()
    time.sleep(290)
    global y
    y=y+5
    print(int(y))
    while driver.current_url !="https://s196-it.ogame.gameforge.com/game/index.php?page=ingame&component=overview":
        #rand=random.uniform(1,10)
        #time.sleep(rand)
        
        # metal mine level
        parent_span_element = driver.find_element(By.CLASS_NAME,"metalMine")
        child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
        level = int(child_span_element.get_attribute("data-value"))
        metalcost = int(90*1.5**level)
        
        # crystal mine cost
        parent_span_element = driver.find_element(By.CLASS_NAME,"crystalMine")
        child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
        level = int(child_span_element.get_attribute("data-value"))
        crystalcost = int(96*1.6**level)
        
        # deuterium cost
        parent_span_element = driver.find_element(By.CLASS_NAME,"deuteriumSynthesizer")
        child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
        level = int(child_span_element.get_attribute("data-value"))
        deutcost = int(375*1.5**level)

        #current energy
        span_element = driver.find_element(By.ID, "resources_energy")
        data_raw = span_element.text.replace(".", "")
        energy = float(data_raw)
        
        if x==1:
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[2]/a'))).click()
            x=0
            expeditions()          
        elif energy<0:
            try :
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[4]/span/button'))).click()
                print("Solar Upgraded")
            except:
                time.sleep(1)
                x=x+1
        elif min(metalcost,crystalcost,deutcost)==crystalcost:
            try :
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[2]/span/button'))).click()
                print("Crystal Upgraded")
            except:
                time.sleep(1)
                x=x+1
        elif min(metalcost,crystalcost,deutcost)==metalcost:
            try :
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[1]/span/button'))).click()
                print("Metal Upgraded")
            except:
                time.sleep(1)
                x=x+1
        elif min(metalcost,crystalcost,deutcost)==deutcost:
            try :
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[3]/span/button'))).click()
                print("Deuterium Upgraded")
            except:
                time.sleep(1)
                x=x+1
    while driver.current_url !="https://s196-it.ogame.gameforge.com/game/index.php?page=ingame&component=supplies":
        time.sleep(10)
        print("Idle, trying to restart in 10 seconds")
        if driver.current_url =="https://s196-it.ogame.gameforge.com/game/index.php?page=ingame&component=supplies":
            print("Starting in 10 seconds")
            mines()



################ EXPEDITION BOT
#### GO TO FLEET
def expeditions():
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[9]/a'))).click()
    ######## GET THE EXPEDITIONS
    span_element = driver.find_element(By.XPATH,'//*[@id="slots"]/div[2]/span')
    text = span_element.text
    match = re.search(r"\d+/\d+", text)  # find the first occurrence of a number sequence of the form "x/y"
    numbers = match.group().split("/")  # extract the numbers as a list
    currentExpedition = int(numbers[0])  # convert the first number to an integer and store it in variable x
    totalExpedition = int(numbers[1])  # convert the second number to an integer and store it in variable y
    slotAvailable=totalExpedition-currentExpedition    
    ######## IF SLOT AVAILABLE START
    while slotAvailable>0:
        ###select fleet
        #Small Cargo
        SHIP = driver.find_element(By.CLASS_NAME,"transporterSmall") 
        SHIP2 = SHIP.find_element(By.CLASS_NAME,"amount") 
        NSHIP = int(SHIP2.get_attribute("data-value"))
        amountToSend=math.floor(NSHIP/slotAvailable)
        ASHIP=driver.find_element(By.XPATH,'//*[@id="civil"]/li[1]/input')
        ASHIP.click()
        ASHIP.send_keys(str(amountToSend))
        #Large Cargo
        SHIP = driver.find_element(By.CLASS_NAME,"transporterLarge") 
        SHIP2 = SHIP.find_element(By.CLASS_NAME,"amount") 
        NSHIP = int(SHIP2.get_attribute("data-value"))
        amountToSend=math.floor(NSHIP/slotAvailable)
        ASHIP=driver.find_element(By.XPATH,'//*[@id="civil"]/li[2]/input')
        ASHIP.click()
        ASHIP.send_keys(str(amountToSend))
        #1 Probe
        ASHIP=driver.find_element(By.XPATH,'//*[@id="civil"]/li[5]/input')
        ASHIP.click()
        ASHIP.send_keys("1")
        #1 pathfinder if available
        try:
            ASHIP=driver.find_element(By.XPATH,'//*[@id="military"]/li[10]/input')
            ASHIP.click()
            ASHIP.send_keys("1")
        except:
            print("No Pathfinders")
        ###continue
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="continueToFleet2"]'))).click()
        coordinate3=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="position"]')))
        coordinate3.click()
        coordinate3.send_keys("16")
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="missionButton15"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="sendFleet"]'))).click()
        time.sleep(2)
        #global expeditionSentNumber
        #expeditionSentNumber=expeditionSentNumber+1
        #print("Expedition number",expeditionSentNumber,"started")
        ######## GET THE EXPEDITIONS AGAIN TO CHECK FOR LOOP
        span_element = driver.find_element(By.XPATH,'//*[@id="slots"]/div[2]/span')
        text = span_element.text
        match = re.search(r"\d+/\d+", text)  # find the first occurrence of a number sequence of the form "x/y"
        numbers = match.group().split("/")  # extract the numbers as a list
        currentExpedition = int(numbers[0])  # convert the first number to an integer and store it in variable x
        totalExpedition = int(numbers[1])  # convert the second number to an integer and store it in variable y
        slotAvailable=totalExpedition-currentExpedition
        time.sleep(1)
    cargos()
    
    
#wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="planet-33624434"]/a'

###CREATE NEW CARGOS
def cargos():
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[7]/a'))).click()
    try:
        time=driver.find_element(By.ID,'shipyardCountdown2')
        time=time.text
        components = time.split()
        hours = 0
        minutes = 0
        seconds = 0
        for comp in components:
            if comp.endswith('h'):
                hours = int(comp[:-1])
            elif comp.endswith('m'):
                minutes = int(comp[:-1])
            elif comp.endswith('s'):
                seconds = int(comp[:-1])
        total_seconds = hours * 3600 + minutes * 60 + seconds
    except:
        total_seconds = 0
    if total_seconds<1800:           
        span_element = driver.find_element(By.ID, "resources_metal")
        data_raw = span_element.text.replace(".", "")
        metal = float(data_raw)
        #crystal
        span_element = driver.find_element(By.ID, "resources_crystal")
        data_raw = span_element.text.replace(".", "")
        crystal = float(data_raw)
        if metal>6020 and crystal>6020:     
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="technologies_civil"]/ul/li[2]'))).click()
            amount=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="build_amount"]')))
            amount.click()
            amount.send_keys(5)
            try:
                amount=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="technologydetails"]/div[2]/div/div[3]/button')))
                amount.click()
                print("Cargo Builded")
            except:
                print("Cargo building went wrong, trying again later")  
            
            mines()
    else:
        print("Queue is more than 30 minutes")
    mines()
    


#planet1     planet1=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="planet-33624434"]/a'))).click()

#test change planet
#planet1
def minesmanager():
    try:
        planet2=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="planet-33625789"]'))).click()
    except:
        mines()
    x=0
    # metal mine level
    parent_span_element = driver.find_element(By.CLASS_NAME,"metalMine")
    child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
    level = int(child_span_element.get_attribute("data-value"))
    metalcost = int(90*1.5**level)
    
    # crystal mine cost
    parent_span_element = driver.find_element(By.CLASS_NAME,"crystalMine")
    child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
    level = int(child_span_element.get_attribute("data-value"))
    crystalcost = int(96*1.6**level)
    
    # deuterium cost
    parent_span_element = driver.find_element(By.CLASS_NAME,"deuteriumSynthesizer")
    child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
    level = int(child_span_element.get_attribute("data-value"))
    deutcost = int(375*1.5**level)

    #current energy
    span_element = driver.find_element(By.ID, "resources_energy")
    data_raw = span_element.text.replace(".", "")
    energy = float(data_raw)
    try:
        time=driver.find_element(By.ID,'buildingCountdown')
        time=time.text
        components = time.split()
        hours = 0
        minutes = 0
        seconds = 0
        for comp in components:
            if comp.endswith('h'):
                hours = int(comp[:-1])
            elif comp.endswith('m'):
                minutes = int(comp[:-1])
            elif comp.endswith('s'):
                seconds = int(comp[:-1])
        total_seconds = hours * 3600 + minutes * 60 + seconds
    except:
        total_seconds = 0   
    if x==1 or total_seconds!=0:
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[2]/a'))).click()
        x=0
        planet1=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="planet-33624434"]/a'))).click()
        time.sleep(1)
        expeditions()         
    elif energy<0:
        try :
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[4]/span/button'))).click()
            print("Solar Upgraded")
        except:
            time.sleep(1)
            x=x+1
    elif min(metalcost,crystalcost,deutcost)==crystalcost:
        try :
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[2]/span/button'))).click()
            print("Crystal Upgraded")
        except:
            time.sleep(1)
            x=x+1
    elif min(metalcost,crystalcost,deutcost)==metalcost:
        try :
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[1]/span/button'))).click()
            print("Metal Upgraded")
        except:
            time.sleep(1)
            x=x+1
    elif min(metalcost,crystalcost,deutcost)==deutcost:
        try :
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[3]/span/button'))).click()
            print("Deuterium Upgraded")
        except:
            time.sleep(1)
            x=x+1    
       
mines()