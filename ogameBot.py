# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 13:16:02 2025

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


class OGameBot:
    def __init__(self):
        """Initialize the bot and create an undetected Chrome driver."""
        self.driver = self.create_undetected_driver()
        self.wait = WebDriverWait(self.driver, 3)

        # Dictionary for button clicks
        self.xpathList = {
            "resources": '//*[@id="menuTable"]/li[2]/a',
            "fleet": '//*[@id="menuTable"]/li[9]/a',
            "galaxy": '//*[@id="menuTable"]/li[10]/a',
            "research": '//*[@id="menuTable"]/li[6]/a',
            "shipyard": '//*[@id="menuTable"]/li[7]/a',
            "defense": '//*[@id="menuTable"]/li[8]/a',
            "lifeform": '//*[@id="menuTable"]/li[3]/a',
            "overview": '//*[@id="menuTable"]/li[1]/a',
            "logout": '//*[@id="logout"]'
        }

        # Upgrade buttons
        self.upgradeButtons = {
            "metal": '//*[@id="producers"]/li[1]/span/button',
            "crystal": '//*[@id="producers"]/li[2]/span/button',
            "deuterium": '//*[@id="producers"]/li[3]/span/button',
            "solar": '//*[@id="producers"]/li[4]/span/button',
            "metalDeposit": '//*[@id="producers"]/li[8]/span/button',
            "crystalDeposit": '//*[@id="producers"]/li[9]/span/button',
            "deuteriumDeposit": '//*[@id="producers"]/li[10]/span/button',
        }

    def create_undetected_driver(self):
        """Creates and returns an undetected Chrome driver."""
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        return uc.Chrome(options=options, version_main=132)

    def login(self, mail, password):
        """Logs into OGame using the provided credentials."""
        self.driver.get("https://lobby.ogame.gameforge.com/it_IT/")
        time.sleep(1)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginRegisterTabs"]/ul/li[1]'))).click()

        mail_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div[2]/div/input')))
        mail_input.click()
        mail_input.send_keys(mail)

        psw_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div[3]/div/input')))
        psw_input.click()
        psw_input.send_keys(password)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/p/button[1]'))).click()
        time.sleep(1)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="joinGame"]/button/span'))).click()

        gioca = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="joinGame"]/button')))
        gioca.click()

        # Close other window and switch back
        parent = self.driver.window_handles[1]
        chld = self.driver.window_handles[0]
        self.driver.switch_to.window(chld)
        time.sleep(1)
        self.driver.close()
        self.driver.switch_to.window(parent)

        print("Login successful!")

    def check_login(self):
        """Checks if login is required and relogs if necessary."""
        if self.driver.current_url == "https://lobby.ogame.gameforge.com/it_IT/hub":
            try:
                gioca = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="joinGame"]/button')))
                gioca.click()

                parent = self.driver.window_handles[1]
                chld = self.driver.window_handles[0]
                self.driver.switch_to.window(chld)
                time.sleep(1)
                self.driver.close()
                self.driver.switch_to.window(parent)

                self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="menuTable"]/li[2]/a'))).click()
                print("Re-logged in successfully!")
            except:
                print("Failed to re-login.")

    def click(self, button):
        """Clicks a button given its name."""
        if button in self.xpathList:
            path = self.xpathList[button]
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, path))).click()
                print(f"Clicked on {button}")
            except:
                print(button, " not clickable")
        else:
            print(f"Button '{button}' not found in xpathList")
    
    def upgrade(self, button):
        """Clicks the upgrade button for a specific building."""
        if button in self.upgradeButtons:
            path = self.upgradeButtons[button]
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, path))).click()
                print(f"Upgraded {button}")
            except:
                print(button, " not clickable")
        else:
            print(f"Upgrade button '{button}' not found")

    def get_planet_ids(self):
        """Finds all planet IDs in the player's empire."""
        planet_elements = self.driver.find_elements(By.CSS_SELECTOR, '[id^="planet-"]')
        planet_ids = [int(re.search(r'planet-(\d+)', el.get_attribute("id")).group(1)) for el in planet_elements]
        return planet_ids

    def clickPlanet(self, number):
        planetList = self.get_planet_ids()
    
        if number >= len(planetList):
            print(f"Invalid planet index: {number}, only {len(planetList)} planets available.")
            return
        
        selectedPlanet = planetList[number]  # Get planet by index
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="planet-{selectedPlanet}"]'))).click()
        print(f"Clicked on Planet {selectedPlanet}")
    
    def get_resources(self):
        """Extracts available resources (metal, crystal, deuterium, energy)."""
        resources = {}

        resources["metal"] = int(self.driver.find_element(By.ID, "resources_metal").get_attribute("data-raw"))
        resources["crystal"] = int(self.driver.find_element(By.ID, "resources_crystal").get_attribute("data-raw"))
        resources["deuterium"] = int(self.driver.find_element(By.ID, "resources_deuterium").get_attribute("data-raw"))
        resources["energy"] = int(self.driver.find_element(By.ID, "resources_energy").get_attribute("data-raw"))

        print(f"Resources: {resources}")
        return resources

    def close(self):
        """Closes the browser."""
        self.driver.quit()
    
    def get_upgrade_costs(self):
        costs = {}
    
        # Metal Mine cost
        metal_mine = self.driver.find_element(By.CLASS_NAME, "metalMine")
        level = int(metal_mine.find_element(By.CLASS_NAME, "level").get_attribute("data-value"))
        #costs["metal_mine"] = int(((60+22.5) * 1.5**level) / ((1.35*10*(level+1)*1.1**(level+1)) - (1.35*10*level*1.1**level)))
        costs["metal"] = [60*1.5**(level-1),15*1.5**(level-1),0]
                                  
        # Crystal Mine cost
        crystal_mine = self.driver.find_element(By.CLASS_NAME, "crystalMine")
        level = int(crystal_mine.find_element(By.CLASS_NAME, "level").get_attribute("data-value"))
        #costs["crystal_mine"] = int(((48+36) * 1.6**level) / ((10*(level+1)*1.1**(level+1)) - (10*level*1.1**level)))
        costs["crystal"] = [48*1.5**(level-1),24*1.6**(level-1),0]
                                    
        # Deuterium Synthesizer cost
        deut_synth = self.driver.find_element(By.CLASS_NAME, "deuteriumSynthesizer")
        level = int(deut_synth.find_element(By.CLASS_NAME, "level").get_attribute("data-value"))
        #costs["deuterium_synthesizer"] = int(((225+107.5) * 1.5**level) / ((10*(level+1)*1.1**(level+1)) - (10*level*1.1**level)))
        costs["deuterium"] = [225*1.5**(level-1),75*1.5**(level-1),0]
                                             
        # Solar Plant cost
        solar_plant = self.driver.find_element(By.CLASS_NAME, "solarPlant")
        level = int(solar_plant.find_element(By.CLASS_NAME, "level").get_attribute("data-value"))
        costs["solar"] = [75*1.5**(level-1),25*1.5**(level-1),0,0]
        
        # metal deposit storage
        parent_span_element = self.driver.find_element(By.CLASS_NAME,"metalStorage")
        child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
        level = int(child_span_element.get_attribute("data-value"))
        costs["metalStorage"] = [1000*2**(level-1),0,0]
        
        # crystal deposit storage
        parent_span_element = self.driver.find_element(By.CLASS_NAME,"crystalStorage")
        child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
        level = int(child_span_element.get_attribute("data-value"))
        costs["metalStorage"] = [1000*2**(level-1),500*2**(level-1),0]
        
        # deuterium deposit storage
        parent_span_element = self.driver.find_element(By.CLASS_NAME,"deuteriumStorage")
        child_span_element = parent_span_element.find_element(By.CLASS_NAME,"level")
        level = int(child_span_element.get_attribute("data-value"))
        costs["metalStorage"] = [1000*2**(level-1),1000*2**(level-1),0]
        
        return costs
    
    def getLevel(self,obj):
        try:
            item = self.driver.find_element(By.CLASS_NAME, obj)
            level = int(item.find_element(By.CLASS_NAME, "level").get_attribute("data-value"))
            return level
        except:
            print("Object not found")
            return 0
        
    def mostEfficientUpgrade(self):
    
        # Metal Mine cost
        metal_mine = self.driver.find_element(By.CLASS_NAME, "metalMine")
        level = int(metal_mine.find_element(By.CLASS_NAME, "level").get_attribute("data-value"))
        metalEfficiency = int(((60+22.5) * 1.5**level) / ((1.35*10*(level+1)*1.1**(level+1)) - (1.35*10*level*1.1**level)))
                                  
        # Crystal Mine cost
        crystal_mine = self.driver.find_element(By.CLASS_NAME, "crystalMine")
        level = int(crystal_mine.find_element(By.CLASS_NAME, "level").get_attribute("data-value"))
        crystalEfficiency = int(((48+36) * 1.6**level) / ((10*(level+1)*1.1**(level+1)) - (10*level*1.1**level)))
                                    
        # Deuterium Synthesizer cost
        deut_synth = self.driver.find_element(By.CLASS_NAME, "deuteriumSynthesizer")
        level = int(deut_synth.find_element(By.CLASS_NAME, "level").get_attribute("data-value"))
        deuteriumEfficiency = int(((225+107.5) * 1.5**level) / ((10*(level+1)*1.1**(level+1)) - (10*level*1.1**level)))
        
        cheapest=min(metalEfficiency,crystalEfficiency,deuteriumEfficiency)
        if cheapest==metalEfficiency:
            return "metal"
        elif cheapest==crystalEfficiency:
            return "crystal"
        elif cheapest==deuteriumEfficiency:
            return "deuterium"
            
    
    def get_remaining_build_time(self):
        try:
            # Locate the countdown timer element
            timer_element = self.driver.find_element(By.CSS_SELECTOR, 'time.countdown.buildingCountdown')
            timer_text = timer_element.text  # Extract the time as text
    
            # Initialize time values
            hours, minutes, seconds = 0, 0, 0
            components = timer_text.split()
    
            # Parse the time
            for comp in components:
                if comp.endswith('h') or comp.endswith('o'):  # 'h' for hours, 'o' for Italian
                    hours = int(comp[:-1])
                elif comp.endswith('m'):  # 'm' for minutes
                    minutes = int(comp[:-1])
                elif comp.endswith('s'):  # 's' for seconds
                    seconds = int(comp[:-1])
    
            total_seconds = hours * 3600 + minutes * 60 + seconds
        except:
            total_seconds = 0  # No active upgrade
    
        return total_seconds

    def get_storage_capacity(self):
        storage_capacity={}
        try:
            metal_box = self.driver.find_element(By.ID, "metal_box")
            tooltip_data = metal_box.get_attribute("data-tooltip-title")
            match = re.search(r"Storage capacity.*?>\s*([\d,]+)", tooltip_data)
            storage_capacity[1] = int(match.group(1).replace(",", ""))  # Remove commas and convert to int
        
            
            crystal_box = self.driver.find_element(By.ID, "crystal_box")
            tooltip_data = crystal_box.get_attribute("data-tooltip-title")
            match = re.search(r"Storage capacity.*?>\s*([\d,]+)", tooltip_data)
            storage_capacity[2] = int(match.group(1).replace(",", ""))  # Remove commas and convert to int
            
            
            deuterium_box = self.driver.find_element(By.ID, "deuterium_box")
            tooltip_data = deuterium_box.get_attribute("data-tooltip-title")
            match = re.search(r"Storage capacity.*?>\s*([\d,]+)", tooltip_data)
            storage_capacity[3] = int(match.group(1).replace(",", ""))  # Remove commas and convert to int
            
            return storage_capacity
            
        except:
            print("Error retrieving storage capacity")
            return None

    
# 🌟 Create a global instance of the bot
bot = OGameBot()

# 🌟 Define wrapper functions to call bot methods without explicitly using bot.
def login(mail, password):
    return bot.login(mail, password)

def check_login():
    return bot.check_login()

def click(button):
    return bot.click(button)

def upgrade(button):
    return bot.upgrade(button)

def get_planet_ids():
    return bot.get_planet_ids()

def clickPlanet(number):
    return bot.clickPlanet(number)

def get_resources():
    return bot.get_resources()

def close():
    return bot.close()

def get_upgrade_costs():
    return bot.get_upgrade_costs()

def get_remaining_build_time():
    return bot.get_remaining_build_time()

def get_storage_capacity():
    return bot.get_storage_capacity()

def mostEfficientUpgrade():
    return bot.mostEfficientUpgrade()

def getLevel(obj):
    return bot.getLevel(obj)