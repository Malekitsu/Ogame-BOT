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
from datetime import datetime

import re
import math


from selenium import webdriver
import undetected_chromedriver as uc

from ogameBot import login, click, upgrade, get_planet_ids, get_resources, close, clickPlanet, get_upgrade_costs
from ogameBot import get_remaining_build_time, get_storage_capacity, mostEfficientUpgrade, getLevel, check_login
from ogameBot import cheapestUpgrade, effectiveCost, getExpeditionCount, getFleet, selectFleet, fleetCoordinates
from ogameBot import get_planet_coordinates, sendResources

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
    
    MetalNeeded: int = 0
    CrystalNeeded: int = 0
    DeuteriumNeeded: int = 0
    LasteHelpSent: int = 0
    
Planets={}
for i in range(0,50):
    Planets[i]=Planet()



###Start variables here
expeditionSentNumber=0
y=0
hyperspaceTechnology=0

def canUpgrade(pl,costs):
    if pl.Metal>costs[0] and pl.Crystal>costs[1] and pl.Deuterium>costs[2]:
        return True
    return False

def requestResources(pl,costs):
    pl.MetalNeeded=max(costs[0]-pl.Metal,0)
    pl.CrystalNeeded=max(costs[1]-pl.Crystal,0)
    pl.DeuteriumNeeded=max(costs[2]-pl.Deuterium,0)
    
def up(pl,costs,construction):
    if canUpgrade(pl,costs[construction]):
        upgrade(construction)
    else:
        requestResources(pl,costs[construction])
    
    
#AUTOMATIC MINE DEVELOPMENT
def mines():
    
    planetList=get_planet_ids()
    for i in range(len(planetList)):
        pl=Planets[i]
        
        clickPlanet(i)
        click("resources")
        
        if get_remaining_build_time()!= 0:
            print("already building") 
            pl.MetalNeeded=0
            pl.CrystalNeeded=0
            pl.DeuteriumNeeded=0
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
        
        
        pl.MetalNeeded=0
        pl.CrystalNeeded=0
        pl.DeuteriumNeeded=0
        
        costs=get_upgrade_costs()
        
        #compare with current resources
        if pl.Metal>pl.MetalStorage*0.95:
            up(pl,costs,"metalDeposit")
        elif pl.Crystal>pl.CrystalStorage*0.95:
            up(pl,costs,"crystalDeposit")
        elif pl.Deuterium>pl.DeuteriumStorage*0.95:
            up(pl,costs,"deuteriumDeposit")
        
        if get_remaining_build_time()!= 0:
            continue
        
        solarCost=effectiveCost(costs["solar"][0],costs["solar"][1],costs["solar"][2])
        fusionCost=effectiveCost(costs["fusion"][0],costs["fusion"][1],costs["fusion"][2])
        
        if pl.Energy<0:
            if pl.SolarLevel<=15:
                up(pl,costs,"solar")
            elif solarCost<20 and solarCost/2<fusionCost:
                up(pl,costs,"fusion")
            elif solarCost<20:
                up(pl,costs,"solar")
            else:
                up(pl,costs,"fusion")
            continue
        
        best=mostEfficientUpgrade()
        #best=cheapestUpgrade()
        
        up(pl,costs,best)
    
    return




################ EXPEDITION BOT

def expeditions():
    clickPlanet(0)
    click("fleet")
    expeditions=getExpeditionCount()
    currentExpeditions=expeditions[0]
    totaExpeditions=expeditions[1]
    
    slotAvailable=totaExpeditions-currentExpeditions
    
    fleet=getFleet()
    ######## IF SLOT AVAILABLE START
    for i in range(slotAvailable):
        ###select fleet
        time.sleep(3)
        smallCargoNumber=math.floor(fleet["Small Cargo"]/(slotAvailable))
        selectFleet(11,smallCargoNumber)
        
        largeCargoNumber=math.floor(fleet["Large Cargo"]/(slotAvailable+4))
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
        global expeditionSentNumber
        system=252+math.floor(expeditionSentNumber/8)%5
        fleetCoordinates(0,system,16)
        click("expedition")
        time.sleep(1)
        sent=click("sendFleet")
        
        if sent:
            expeditionSentNumber=expeditionSentNumber+1
            print("Expedition n°",expeditionSentNumber,"have been sent")



def helpcolonies():
    global hyperspaceTechnology
    clickPlanet(0)
    pl=Planets[0]
    
    resources=get_resources()
    pl.Metal=resources["metal"]
    pl.Crystal=resources["crystal"]
    pl.Deuterium=resources["deuterium"]
    pl.Energy = resources["energy"]
    
    
    planetList=get_planet_ids()
    for i in range(len(planetList)-1):
        plToHelp=Planets[i+1]
        
        metal=math.ceil(plToHelp.MetalNeeded)
        crystal=math.ceil(plToHelp.CrystalNeeded)
        deut=math.ceil(plToHelp.DeuteriumNeeded)
        
        if metal+crystal+deut>50000 and time.time()-plToHelp.LasteHelpSent>1500:
            if pl.Metal>metal and pl.Crystal>crystal and pl.Deuterium>deut:                 
                #check first research level
                if hyperspaceTechnology==0:
                    click("research")
                    #parent_span_element = driver.find_element(By.CLASS_NAME,"hyperspaceTechnology")
                    #child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
                    #techlevel = int(child_span_element.get_attribute("data-value"))
                    hyperspaceTechnology=8
                    click("fleet")
                
                fleet=getFleet()
                cargoneeded=math.ceil((metal+crystal+deut)/(25000*(1+0.05*hyperspaceTechnology)))
                if cargoneeded<=fleet["Large Cargo"]:
                    selectFleet(12,cargoneeded)
                    
                    time.sleep(1)            
                    click("fleet2")
                    time.sleep(1)
                    coord=get_planet_coordinates()
                    
                    fleetCoordinates(coord[i+1][0],coord[i+1][1],coord[i+1][2])
                    time.sleep(1)
                    click("transport")
                    time.sleep(1)
                    sendResources(metal,crystal,deut)
                    click("sendFleet")
                    
                    plToHelp.MetalNeeded=0
                    plToHelp.CrystallNeeded=0
                    plToHelp.DeuteriumNeeded=0
                    plToHelp.LasteHelpSent=time.time()
                    
                    print("sent",metal,"Metal, ",crystal,"Crystal and ", deut, " Deuterium at",coord[i+1][0],coord[i+1][1],coord[i+1][2])


def loop():      
    global y            
    try:        
        check_login()
        mines()
        expeditions()
        helpcolonies()
        
        y=y+1
        restsec=int(random.random()*60 +60*10)
        restmin=int(restsec/60)
        print("Cycle n°",y,"starting in",restmin," minutes and ",restsec%60," seconds")
        time.sleep(restsec)
        
        loop()
    except:
        print("error, restarting")
        time.sleep(10)
        loop()
       
