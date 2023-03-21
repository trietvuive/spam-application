from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import chardet
import tkinter as tk

# define your url and amount of time requires to process registration
URL = 'https://vinuni.my.site.com/s/login/SelfRegister'
TIMEOUT = 2
CSV_FILE = 'data/students.txt'

class RegistrationAutomation():
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get(URL)
        self.fail_count = self.success_count = 0
        self.index = 0
        self.students = self.read_students_list(CSV_FILE)

    def process_next_student(self) -> bool:
        if self.index >= len(self.students):
            return False

        name, email = self.students[self.index]
        result = self.send_input(self.driver, name, email)
        if result:
            self.success_count += 1
        else:
            self.fail_count += 1
        
        self.index += 1

        return result

    def __len__(self):
        return len(self.students)

    def wait_for_element(self, driver, element_id : str):
        while len(driver.find_elements(By.ID, element_id)) == 0:
            pass

    def read_students_list(self, file : str):
        with open(file, 'r', encoding='utf-16') as f:
            students = f.readlines()
            students = [x.strip() for x in students]
            students = [tuple(x.split('\t')[1:]) for x in students]
            return [x for x in students if len(x) == 2]
    

    def send_input(self, driver, name : str, email : str) -> bool:
        # for some reason if we're not at target URL, go there
        driver.get(URL)

        self.wait_for_element(driver, "sfdc_nickname_container")

        name_field = driver.find_element(By.XPATH, "//div[@id='sfdc_nickname_container']/input")
        name_field.send_keys(name)

        email_field = driver.find_element(By.XPATH, "//div[@id='sfdc_email_container']/input")
        email_field.send_keys(email)

        submit_button = driver.find_element(By.XPATH, "//div[@class='sfdc']/button")
        submit_button.click()

        # wait until error message pop up or page redirect, basically
        while len(driver.find_elements(By.ID, "error")) == 0 and driver.current_url == URL:
            pass

        if len(driver.find_elements(By.ID, "error")) > 0:
            return False
        return True
