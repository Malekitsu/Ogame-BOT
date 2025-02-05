# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 22:03:39 2025
@author: Ruben
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pyautogui

import re
import math


from selenium import webdriver
import undetected_chromedriver as uc

from ogameBot import login, click, upgrade, get_planet_ids, get_resources, close, clickPlanet, get_upgrade_costs
from ogameBot import get_remaining_build_time, get_storage_capacity, mostEfficientUpgrade, getLevel, check_login
from ogameBot import cheapestUpgrade, effectiveCost, getExpeditionCount, getFleet, selectFleet, fleetCoordinates

def human_delay(base=1, spread=2):
    time.sleep(abs(base + random.gauss(0, spread/3)))

def human_click(element):
    human_delay(0.3, 0.7)
    element.click()
    human_delay(0.2, 0.5)

def random_mouse_move():
    if random.random() > 0.7:
        x = random.randint(100, 1800)
        y = random.randint(100, 900)
        pyautogui.moveTo(x, y, duration=random.uniform(0.1, 1.2))
        if random.random() > 0.8:
            pyautogui.click()

def rotate_fingerprint(driver):
    fingerprints = [
        {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "platform": "Win32",
            "languages": ["en-US", "en"],
            "hardwareConcurrency": 8
        },
        {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "platform": "Win32",
            "languages": ["en-GB", "en"],
            "hardwareConcurrency": 4
        }
    ]
    fp = random.choice(fingerprints)
    
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {
        "userAgent": fp['userAgent'],
        "platform": fp['platform'],
        "acceptLanguage": ", ".join(fp['languages'])
    })
    
    driver.execute_script(f"""
        Object.defineProperty(navigator, 'hardwareConcurrency', {{
            value: {fp['hardwareConcurrency']},
            writable: false
        }});
        Object.defineProperty(navigator, 'language', {{
            value: '{fp['languages'][0]}',
            writable: false
        }});
    """)

mail="ruben.toccafondo@gmail.com"
password="Narutorengan9!"

login(mail, password)
click("acceptCookies")
class Planet:
    Metal: int = 0
    Crystal: int = 0
    Deuterium: int = 0
    Energy: int = 0
    
    MetalStorage: int = 0
    CrystalStorage: int = 0
    DeuteriumStorage: int = 0
    
    MetalLevel: int = 0
    CrystalLevel: int = 0
    DeuteriumLevel: int = 0
    SolarLevel: int = 0
    FusionLevel: int = 0
    
    MetalStorageLevel: int = 0
    CrystalStorageLevel: int = 0
    DeuteriumStorageLevel: int = 0
    
    Level: int = 0

Planets={}
for i in range(0,50):
    Planets[i]=Planet()



###Start variables here
expeditionSentNumber=0
y=0

#AUTOMATIC MINE DEVELOPMENT
def mines():
    
    planetList=get_planet_ids()
    for i in range(len(planetList)):
        pl=Planets[i]
        
        clickPlanet(i)
        click("resources")
        
        if get_remaining_build_time()!= 0:
            print("already building")
            continue
            
        resources=get_resources()
        pl.Metal=resources["metal"]
        pl.Crystal=resources["crystal"]
        pl.Deuterium=resources["deuterium"]
        pl.Energy = resources["energy"]
        
        storage=get_storage_capacity()        
        pl.MetalStorage=storage[1]
        pl.CrystalStorage=storage[2]
        pl.DeuteriumStorage=storage[3]
        
        pl.MetalLevel=getLevel("metalMine")
        pl.CrystalLevel=getLevel("crystalMine")
        pl.DeuteriumLevel=getLevel("deuteriumSynthesizer")
        pl.SolarLevel=getLevel("solarPlant")
        pl.FusionLevel=getLevel("fusionPlant")
        pl.MetalStorageLevel=getLevel("metalStorage")
        pl.CrystalStorageLevel=getLevel("crystalStorage")
        pl.DeuteriumStorageLevel=getLevel("deuteriumStorage")
        
        #compare with current resources
        if pl.Metal>pl.MetalStorage*0.95:
            upgrade("metalDeposit")
        elif pl.Crystal>pl.CrystalStorage*0.95:
            upgrade("crystalDeposit")
        elif pl.Deuterium>pl.DeuteriumStorage*0.95:
            upgrade("deuteriumDeposit")
            
        
        costs=get_upgrade_costs()
        solarCost=effectiveCost(costs["solar"][0],costs["solar"][1],costs["solar"][2])
        fusionCost=effectiveCost(costs["fusion"][0],costs["fusion"][1],costs["fusion"][2])
        
        if pl.Energy<0:
            if pl.SolarLevel<=15:
                upgrade("solar")
            elif solarCost<20 and solarCost/2<fusionCost:
                upgrade("fusion")
            elif solarCost<20:
                upgrade("solar")
            else:
                upgrade("fusion")
            continue
        
        #up=mostEfficientUpgrade()
        up=cheapestUpgrade()
        try :
            upgrade(up)
            print(up," Upgraded")
        except:
            print("Not enough resources to upgrade ",up)
    
    return




################ EXPEDITION BOT

def expeditions():
    clickPlanet(0)
    click("fleet")
    expeditions=getExpeditionCount()
    currentExpeditions=expeditions[0]
    totaExpeditions=expeditions[1]
    
    ############# REMOVE LATER
    totaExpeditions=1
    #############
    
    slotAvailable=totaExpeditions-currentExpeditions
    
    
    fleet=getFleet()
    ######## IF SLOT AVAILABLE START
    if slotAvailable>0:
        ###select fleet
        smallCargoNumber=math.floor(fleet["Small Cargo"]/slotAvailable)
        selectFleet(11,smallCargoNumber)
        
        largeCargoNumber=min(math.floor(fleet["Large Cargo"]/(slotAvailable)), 400)
        selectFleet(12,largeCargoNumber)
        
        #1 Probe
        selectFleet(15,1)
        #1 pathfinder if available
        selectFleet(10,1)
        #extra ship
        sent=False
        for l in [9,7,6,5,4,3,2,1]:
            if sent==0:
                if selectFleet(l,1):
                    sent=True
    
    time.sleep(1)            
    click("fleet2")
    time.sleep(1)
    fleetCoordinates(0,0,16)
    click("expedition")
    time.sleep(1)
    sent=click("sendFleet")
    
    if sent:
        global expeditionSentNumber
        expeditionSentNumber=expeditionSentNumber+1
        print("Expedition n°",expeditionSentNumber,"have been sent")



def helpcolonies():
    planetList=get_planet_ids(driver)
    for i in planetList:

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[@id="planet-{i}"]'))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[2]/a'))).click()
        except:
            print("couldn't select planet")
        
        
        
        #solar cost
        parent_span_element = driver.find_element(By.CLASS_NAME,"solarPlant")
        child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
        solarlevel = int(child_span_element.get_attribute("data-value"))
        solar_metalneeded = int(75*1.5**solarlevel)
        solar_crystalneeded = int(30*1.5**solarlevel)
        
        #current energy
        span_element = driver.find_element(By.ID, "resources_energy")
        data_raw = span_element.text.replace(".", "")
        energy = float(data_raw)
        
        
        #satelites builder
        if energy<0 and solarlevel>=20:
            ###check if there are satelites under construction
            satcon=0
            for j in range(1,5):
                for k in range(1,6):        
                    try:
                        td_element = driver.find_element(By.XPATH, f'//*[@id="productionboxshipyardcomponent"]/div/div[2]/table[2]/tbody/tr[{j}]/td[{k}]')
                        img_element = td_element.find_element(By.TAG_NAME, "img")
                        src = img_element.get_attribute("src")
                        if src == "https://gf2.geo.gfsrv.net/cdnd3/5f3ca7e91fc0a9b1ee014c3c01ea41.jpg":
                            satcon=1
                    except:
                        pass

            try:
                td_element = driver.find_element(By.XPATH, '//*[@id="productionboxshipyardcomponent"]/div/div[2]/table[1]/tbody/tr[2]/td/div[1]')
                img_element = td_element.find_element(By.TAG_NAME, "img")
                src = img_element.get_attribute("src")
                if src == "https://gf2.geo.gfsrv.net/cdnda/665c65072887153d44a6684ec276e9.jpg":
                    satcon=1
            except:
                pass
            if satcon==0:
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[6]'))).click()
                    text=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="build_amount"]')))
                    text.click()
                    text.send_keys(10)
                    try:
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="technologydetails"]/div[2]/div/div[3]/div/button/span'))).click()
                        print("satelites built")
                    except:
                        print("couldn't build satelites")
                except:
                    print("satelites not available")    
        #deut sender
        
        span_element = driver.find_element(By.ID, "resources_deuterium")
        data_raw = span_element.text.replace(".", "").replace(",",".")
        if data_raw[-1] == "M":
            deuterium = float(data_raw[:-1]) * 1000000
        else:
            deuterium = float(data_raw)
            
        if deuterium>1500000:
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[9]/a'))).click()
                ASHIP=driver.find_element(By.XPATH,'//*[@id="civil"]/li[2]/input')
                ASHIP.click()
                ASHIP.send_keys(str("200"))
                
                #send
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="continueToFleet2"]'))).click()
                coordinate1=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="galaxy"]')))
                coordinate1.click()
                coordinate1.send_keys("4")
                coordinate2=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="system"]')))
                coordinate2.click()
                coordinate2.send_keys("180")
                coordinate3=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="position"]')))
                coordinate3.click()
                coordinate3.send_keys("8")
                time.sleep(1) 
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="missionButton3"]'))).click()
                metalamount=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="deuterium"]')))
                metalamount.click()
                metalamount.send_keys(f"{deuterium}") 
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="sendFleet"]'))).click()
                print("Sent",deuterium,"deuterium to mother planet")
                time.sleep(1)
            except:
                pass
        
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[2]/a'))).click()
        
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
            totmetalcost = int(((60+22.5)*1.5**level)/((1.35*10*(level+1)*1.1**(level+1))-(1.35*10*level*1.1**level)))
            metal_metalneeded = int(60*1.5**level)
            metal_crystalneeded = int(15*1.5**level)
            
            # crystal mine cost
            parent_span_element = driver.find_element(By.CLASS_NAME,"crystalMine")
            child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
            level = int(child_span_element.get_attribute("data-value"))
            totcrystalcost = int(((48+36)*1.6**level)/((10*(level+1)*1.1**(level+1))-(10*level*1.1**level)))
            crystal_metalneeded = int(48*1.6**level)
            crystal_crystalneeded = int(24*1.6**level)
            
            # deuterium cost
            parent_span_element = driver.find_element(By.CLASS_NAME,"deuteriumSynthesizer")
            child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
            level = int(child_span_element.get_attribute("data-value"))
            totdeutcost = int(((225+107.5)*1.5**level)/((10*(level+1)*1.1**(level+1))-(10*level*1.1**level)))
            deut_metalneeded = int(225*1.5**level)
            deut_crystalneeded = int(75*1.5**level)
            
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
            
            # current deuterium
            span_element = driver.find_element(By.ID, "resources_deuterium")
            data_raw = span_element.text.replace(".", "").replace(",",".")
            if data_raw[-1] == "M":
                deuterium = float(data_raw[:-1]) * 1000000
            else:
                deuterium = float(data_raw)
            
            
            #get deposit levels
            
            # metal deposit storage
            parent_span_element = driver.find_element(By.CLASS_NAME,"metalStorage")
            child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
            level = int(child_span_element.get_attribute("data-value"))
            mstorage = 5000*(2.5*math.exp(20/33*level))
            #mstorage_metalneeded = int(1000*2**(level-1))
            #mstorage_crystalneeded = 0
            
            # crystal deposit storage
            parent_span_element = driver.find_element(By.CLASS_NAME,"crystalStorage")
            child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
            level = int(child_span_element.get_attribute("data-value"))
            cstorage = 5000*(2.5*math.exp(20/33*level))
            #cstorage_metalneeded = int(1000*2**(level-1))
            #cstorage_crystalneeded = int(500*2**(level-1))
            
            # deuterium deposit storage
            parent_span_element = driver.find_element(By.CLASS_NAME,"deuteriumStorage")
            child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
            level = int(child_span_element.get_attribute("data-value"))
            dstorage = 5000*(2.5*math.exp(20/33*level))
            #dstorage_metalneeded = int(1000*2**(level-1))
            #dstorage_crystalneeded = int(1000*2**(level-1))
            
            ###ROBOT AND NANITES BUILDER
            
            if metal>210000 and crystal>64000 and deuterium>102400:
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[4]/a'))).click()
                #get robots
                parent_span_element = driver.find_element(By.CLASS_NAME,"roboticsFactory")
                child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
                level = int(child_span_element.get_attribute("data-value"))
                if level<10:
                    try:
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="technologies"]/ul/li[1]/span/button'))).click()
                        print(f"Colony {i} Robot Upgraded")
                        continue
                    except:
                        pass
                    
                elif metal>1000000 and crystal>500000 and deuterium>100000:
                    parent_span_element = driver.find_element(By.CLASS_NAME,"naniteFactory")
                    child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
                    level = int(child_span_element.get_attribute("data-value"))
                    if 2^level*1000000<metal and level <4:
                        try:
                            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="technologies"]/ul/li[6]/span/button'))).click()
                            print(f"Colony {i} Nanite Upgraded")
                            continue
                        except:
                            pass 
                wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[2]/a'))).click()
            
            
            
            #compare storage with current resources
            if metal>mstorage*0.9:
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[8]/span/button'))).click()
                    print(f"Colony {i} Metal Deposit Upgraded")
                    continue
                except:
                    print("Couldn't build Metal Deposit")
            elif crystal>cstorage*0.9:
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[9]/span/button'))).click()
                    print(f"Colony {i} Crystal Deposit Upgraded")
                    continue
                except:
                    print("Couldn't build Crystal Deposit")
            elif deuterium>dstorage*0.9:
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="producers"]/li[10]/span/button'))).click()
                    print(f"Colony {i} Deuterium Deposit Upgraded")
                    continue
                except:
                    print("Couldn't build Deuterium Deposit")
             
            #mines           
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
                #get coordinates
                planet_element= driver.find_element(By.XPATH, f'//*[@id="planet-{i}"]')
                span_element = planet_element.find_element(By.XPATH, ".//span[contains(@class, 'planet-koords')]")
                coords = span_element.text
                x, y, z = coords[1:-1].split(':')
                #check if a fleet have been sent already
                fleetSent=0
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="eventboxFilled"]'))).click()
                    time.sleep(1)
                    event_rows = driver.find_elements(By.CLASS_NAME, "eventFleet")
                    for row in event_rows:
                        coords_element = row.find_element(By.XPATH, ".//td[@class='destCoords']/a")
                        coords2 = coords_element.text.strip()
                        if coords == coords2:
                            fleetSent=1
                except:
                    pass
                
                if fleetSent==0:
                    #go to main planet
                    mainPlanet=get_planet_ids(driver)[0]
                    wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[@id="planet-{mainPlanet}"]'))).click() 
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
                    
                    missingmetal=int(max(-missingmetal,0))
                    missingcrystal=int(max(-missingcrystal,0))
                    missingmetal1=metal-missingmetal
                    missingcrystal1=crystal-missingcrystal
                    
                    print(missingmetal,missingcrystal)
                    #######SEND AT LEAST 500-200K
                    missingmetal=max(missingmetal,500000)
                    missingcrystal=max(missingcrystal,200000)
                    
                    
                    if missingmetal1>0 and missingcrystal1>0:
                        #check first research level
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[6]/a'))).click()
                        parent_span_element = driver.find_element(By.CLASS_NAME,"hyperspaceTechnology")
                        child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
                        techlevel = int(child_span_element.get_attribute("data-value"))
                        
                        cargoneeded=math.ceil((missingmetal+missingcrystal)/(25000*(1+0.05*techlevel)))
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[9]/a'))).click()
                        
                        #Large Cargo
                        SHIP = driver.find_element(By.CLASS_NAME,"transporterLarge") 
                        SHIP2 = SHIP.find_element(By.CLASS_NAME,"amount") 
                        NSHIP = int(SHIP2.get_attribute("data-value"))
                        
                        if NSHIP>cargoneeded:                   
                            ASHIP=driver.find_element(By.XPATH,'//*[@id="civil"]/li[2]/input')
                            ASHIP.click()
                            ASHIP.send_keys(str(cargoneeded))
                            
                            
                            #send
                            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="continueToFleet2"]'))).click()
                            coordinate1=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="galaxy"]')))
                            coordinate1.click()
                            coordinate1.send_keys(f"{x}")
                            coordinate2=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="system"]')))
                            coordinate2.click()
                            coordinate2.send_keys(f"{y}")
                            coordinate3=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="position"]')))
                            coordinate3.click()
                            coordinate3.send_keys(f"{z}")
                            time.sleep(1) 
                            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="missionButton3"]'))).click()
                            metalamount=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="metal"]')))
                            metalamount.click()
                            metalamount.send_keys(f"{missingmetal}") 
                            crystalamount=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="crystal"]')))
                            crystalamount.click()
                            crystalamount.send_keys(f"{missingcrystal}")                                                                                                   
                            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="sendFleet"]'))).click()
                            time.sleep(1)  
                            print("sent",missingmetal,"Metal and",missingcrystal,"Crystal at",coords)
        
        
    
    
    cargos()  
    

###CREATE NEW CARGOS
def cargos():
    mainPlanet=get_planet_ids(driver)[0]
    wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[@id="planet-{mainPlanet}"]'))).click() 
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
            amount.send_keys(100)
            try:
                amount=wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="technologydetails"]/div[2]/div/div[3]/button')))
                amount.click()
                print("Cargo Builded")
            except:
                pass
            
    lifeform()
    



def lifeform():
    lifeform=1
    if lifeform==1:
        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="menuTable"]/li[3]/a'))).click()
        planetList=get_planet_ids(driver)
        for i in planetList:
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH,f'//*[@id="planet-{i}"]'))).click()
            except:
                continue
            
            #get race
            div_element = driver.find_element(By.XPATH,"//div[contains(@class, 'lifeform')]")
            class_attribute = div_element.get_attribute('class')
            match = re.search(r'lifeform(\d+)', class_attribute)
            civilization = int(match.group(1))
            
            try:
                times=driver.find_element(By.ID,'buildingCountdown')
                total_seconds = 1
            except:
                total_seconds = 0 
            if total_seconds == 0:
                targetlevel1=51
                targetlevel2=52
                
                #lifeform 1 level
                parent_span_element = driver.find_element(By.CLASS_NAME,f"lifeformTech1{civilization}101")
                child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
                level1 = int(child_span_element.get_attribute("data-value"))
                
                #lifeform 2 level
                parent_span_element = driver.find_element(By.CLASS_NAME,f"lifeformTech1{civilization}102")
                child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
                level2 = int(child_span_element.get_attribute("data-value"))
                
                
                if level1<targetlevel1 and level1<level2:
                    try:
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="technologies"]/ul/li[1]/span/button'))).click()
                        continue
                    except:
                        pass
                if level2<targetlevel2:
                    try:
                        wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="technologies"]/ul/li[2]/span/button'))).click()
                        continue
                    except:
                        pass
                    
    mines()

def loop():                  
    try:        
        check_login()
        mines()
        expeditions()
        #helpcolonies()
        #lifeform()
        
        global y
        y=y+1
        restsec=int(random.random()*600+300)
        restmin=int(restsec/60)
        print("Cycle n°",y,"starting in",restmin," minutes and ",restsec%60," seconds")
        time.sleep(restsec)
        
        loop()
    except:
        print("error, restarting")
        loop()
       

    



