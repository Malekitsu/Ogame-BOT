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
email_field.send_keys("e-mail")
password_field = wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='pass']")))
password_field.send_keys("password")
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

#fixing cookies and clickable objects
dezoom=0
for i in range(1,10):
    try:
        driver.find_element(By.XPATH, f'//*[@id="ingamepage"]/div[{i}]/div/div/span[2]/button[2]').click()   
    except:
        dezoom=dezoom+1
        
if dezoom==10:       
    print("Couldn't close cookies")
    pyautogui.keyDown('ctrl')
    pyautogui.press('-')
    pyautogui.press('-')
    pyautogui.press('-')
    pyautogui.keyUp('ctrl')

pyautogui.keyDown('ctrl')
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
y=-5
#AUTOMATIC MINE DEVELOPMENT
def mines():
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[2]/a'))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="planet-33625789"]'))).click()   
    global y
    y=y+5
    print(int(y))
    time.sleep(10)  
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
        
        #energy level
        parent_span_element = driver.find_element(By.CLASS_NAME,"solarPlant")
        child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
        level = int(child_span_element.get_attribute("data-value"))
        
        try:
            times=driver.find_element(By.ID,'buildingCountdown')
            times=times.text
            components = times.split()
            hours = 0
            minutes = 0
            seconds = 0
            for comp in components:
                if comp.endswith('h') or comp.endswith('o'):
                    hours = int(comp[:-1])
                elif comp.endswith('m'):
                    minutes = int(comp[:-1])
                elif comp.endswith('s'):
                    seconds = int(comp[:-1])
            total_seconds = hours * 3600 + minutes * 60 + seconds
        except:
            total_seconds = 0 
        if total_seconds != 0:
            helpcolonies()
        elif energy<0 and level<=20:
            try :
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[4]/span/button'))).click()
                print("Solar Upgraded")
            except:
                pass
        elif min(metalcost,crystalcost,deutcost)==crystalcost:
            try :
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[2]/span/button'))).click()
                print("Crystal Upgraded")
            except:
                pass
        elif min(metalcost,crystalcost,deutcost)==metalcost:
            try :
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[1]/span/button'))).click()
                print("Metal Upgraded")
            except:
                pass
        elif min(metalcost,crystalcost,deutcost)==deutcost:
            try :
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[3]/span/button'))).click()
                print("Deuterium Upgraded")
            except:
                pass
        helpcolonies()
    while driver.current_url !="https://s196-it.ogame.gameforge.com/game/index.php?page=ingame&component=supplies":
        time.sleep(10)
        print("Idle, trying to restart in 10 seconds")
        if driver.current_url =="https://s196-it.ogame.gameforge.com/game/index.php?page=ingame&component=supplies":
            print("Starting in 10 seconds")
            mines()



################ EXPEDITION BOT
#### GO TO FLEET
def expeditions():
    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="planet-33625789"]'))).click() 
    time.sleep(1)
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
        amountToSend=math.floor(NSHIP/(slotAvailable+1))
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
        global expeditionSentNumber
        expeditionSentNumber=expeditionSentNumber+1
        print("Expedition n°",expeditionSentNumber,"have been sent")
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
        times=driver.find_element(By.ID,'shipyardCountdown2')
        times=times.text
        components = times.split()
        hours = 0
        minutes = 0
        seconds = 0
        for comp in components:
            if comp.endswith('o') or comp.endswith('h'):
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
        data_raw = span_element.text.replace(".", "").replace(",",".")
        if data_raw[-1] == "M":
            metal = float(data_raw[:-1]) * 1000000
        else:
            metal = float(data_raw)
        #crystal
        span_element = driver.find_element(By.ID, "resources_crystal")
        data_raw = span_element.text.replace(".", "").replace(",",".")
        if data_raw[-1] == "M":
            crystal = float(data_raw[:-1]) * 1000000
        else:
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
                mines()
            except:
                print("Cargo building went wrong, trying again later")  
            
            expeditions()
    expeditions()
    



def helpcolonies():
    
    for i in [33626272,33626296]:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[@id="planet-{i}"]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[2]/a'))).click()
        except:
            print("couldn't select planet")
        try:
            times=driver.find_element(By.ID,'buildingCountdown')
            total_seconds = 1
        except:
            total_seconds = 0 
        if total_seconds == 0:
            # metal mine cost
            parent_span_element = driver.find_element(By.CLASS_NAME,"metalMine")
            child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
            level = int(child_span_element.get_attribute("data-value"))
            totmetalcost = int(90*1.5**level)
            metal_metalneeded = int(60*1.5**level)
            metal_crystalneeded = int(15*1.5**level)
            
            # crystal mine cost
            parent_span_element = driver.find_element(By.CLASS_NAME,"crystalMine")
            child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
            level = int(child_span_element.get_attribute("data-value"))
            totcrystalcost = int(96*1.6**level)
            crystal_metalneeded = int(48*1.6**level)
            crystal_crystalneeded = int(24*1.6**level)
            
            # deuterium cost
            parent_span_element = driver.find_element(By.CLASS_NAME,"deuteriumSynthesizer")
            child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
            level = int(child_span_element.get_attribute("data-value"))
            totdeutcost = int(375*1.5**level)
            deut_metalneeded = int(225*1.5**level)
            deut_crystalneeded = int(75*1.5**level)
            
            #solar cost
            parent_span_element = driver.find_element(By.CLASS_NAME,"solarPlant")
            child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
            solarlevel = int(child_span_element.get_attribute("data-value"))
            solar_metalneeded = int(75*1.5**solarlevel)
            solar_crystalneeded = int(30*1.5**solarlevel)
            
            #current metal
            span_element = driver.find_element(By.ID, "resources_metal")
            data_raw = span_element.text.replace(".", "").replace(",",".")
            if data_raw[-1] == "M":
                metal = float(data_raw[:-1]) * 1000000
            else:
                metal = float(data_raw)
            
            # current crystal
            span_element = driver.find_element(By.ID, "resources_crystal")
            data_raw = span_element.text.replace(".", "").replace(",",".")
            if data_raw[-1] == "M":
                crystal = float(data_raw[:-1]) * 1000000
            else:
                crystal = float(data_raw)
            
            #current energy
            span_element = driver.find_element(By.ID, "resources_energy")
            data_raw = span_element.text.replace(".", "")
            energy = float(data_raw)
            
            if energy<0 and solarlevel<20:
                missingmetal= metal-solar_metalneeded
                missingcrystal= crystal-solar_crystalneeded
                up=4
            elif min(totmetalcost,totcrystalcost,totdeutcost)==totmetalcost:
                missingmetal= metal-metal_metalneeded
                missingcrystal= crystal-metal_crystalneeded
                up=1
            elif min(totmetalcost,totcrystalcost,totdeutcost)==totcrystalcost:
                missingmetal= metal-crystal_metalneeded
                missingcrystal= crystal-crystal_crystalneeded
                up=2
            elif min(totmetalcost,totcrystalcost,totdeutcost)==totdeutcost:
                missingmetal= metal-deut_metalneeded
                missingcrystal= crystal-deut_crystalneeded
                up=3
            
            if missingmetal>=0 and missingcrystal>=0:                
                try :
                    wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[@id="producers"]/li[{up}]/span/button'))).click()
                    print(f"Colony {i} {up} Upgraded")
                except:
                    print("couldn't upgrade")
            else:
                
                #go to main planet
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="planet-33625789"]'))).click()
                time.sleep(1)
                #check if there are enough resources
                span_element = driver.find_element(By.ID, "resources_metal")
                data_raw = span_element.text.replace(".", "").replace(",",".")
                if data_raw[-1] == "M":
                    metal = float(data_raw[:-1]) * 1000000
                else:
                    metal = float(data_raw) 
                span_element = driver.find_element(By.ID, "resources_crystal")
                data_raw = span_element.text.replace(".", "").replace(",",".")
                if data_raw[-1] == "M":
                    crystal = float(data_raw[:-1]) * 1000000
                else:
                    crystal = float(data_raw) 
                    
                missingmetal=metal-deut_metalneeded
                missingcrystal=crystal-deut_crystalneeded
                if missingmetal>0 and missingcrystal>0:
                    #check first research level
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[6]/a'))).click()
                    parent_span_element = driver.find_element(By.CLASS_NAME,"hyperspaceTechnology")
                    child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
                    techlevel = int(child_span_element.get_attribute("data-value"))
                    
                    cargoneeded=math.ceil(missingmetal+missingcrystal)/(25000*(1+0.05*techlevel))
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[9]/a'))).click()
                    
                    print(cargoneeded)
                    #Large Cargo
                    SHIP = driver.find_element(By.CLASS_NAME,"transporterLarge") 
                    SHIP2 = SHIP.find_element(By.CLASS_NAME,"amount") 
                    NSHIP = int(SHIP2.get_attribute("data-value"))
                    
                    print(NSHIP)
                    if NSHIP>cargoneeded:                   
                        ASHIP=driver.find_element(By.XPATH,'//*[@id="civil"]/li[2]/input')
                        ASHIP.click()
                        ASHIP.send_keys(str(cargoneeded))
                        
                        #get coordinates
                        planet_element= driver.find_element(By.XPATH, f'//*[@id="planet-{i}"]')
                        span_element = planet_element.find_element(By.XPATH, ".//span[contains(@class, 'planet-koords')]")
                        coords = span_element.text
                        x, y, z = coords[1:-1].split(':')
                        x=1
                        
                        #send
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="continueToFleet2"]'))).click()
                        coordinate1=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="galaxy"]')))
                        coordinate1.click()
                        coordinate1.send_keys(f"{x}")
                        coordinate2=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="position"]')))
                        coordinate2.click()
                        coordinate2.send_keys(f"{y}")
                        coordinate3=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="position"]')))
                        coordinate3.click()
                        coordinate3.send_keys(f"{z}")
                        time.sleep(1)                   
                        metalamount=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="metal"]')))
                        metalamount.click()
                        metalamount.send_keys(f"{missingmetal}")                   
                        crystalamount=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="metal"]')))
                        crystalamount.click()
                        crystalamount.send_keys(f"{missingcrystal}")                    
                        time.sleep(1)                                                          
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="sendFleet"]'))).click()
    expeditions()                    
                       
mines()
