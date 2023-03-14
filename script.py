from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import chardet

# define your url and amount of time requires to process registration
URL = 'https://vinuni.my.site.com/s/login/SelfRegister'
TIMEOUT = 2

def wait_for_element(driver, element_id : str):
    while len(driver.find_elements(By.ID, element_id)) == 0:
        pass

def send_input(driver, name : str, email : str) -> bool:
    # for some reason if we're not at target URL, go there
    driver.get(URL)

    wait_for_element(driver, "sfdc_nickname_container")

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

def read_students_list(file : str):
    with open(file, 'r', encoding='utf-16') as f:
        students = f.readlines()
        students = [x.strip() for x in students]
        students = [tuple(x.split('\t')[1:]) for x in students]
        return [x for x in students if len(x) == 2]

def main():
    start = time.time()
    students = read_students_list('data/students.txt')
    driver = webdriver.Firefox()
    driver.get(URL)
    fail_count = success_count = 0
    index = 0

    for name, email in students:
        result = send_input(driver, name, email)
        if result:
            success_count += 1
            time.sleep(TIMEOUT)
        else:
            fail_count += 1

        print(f"Index #{index} of {len(students)}\t", name, email, "success" if result else "already registered")
        index += 1
,
    print("Success: {}, Already registered: {}".format(success_count, fail_count))
    end = time.time()
    print(f"Time {round(end - start, 2)}, processed {len(students)} students")
    driver.quit()

if __name__ == '__main__':
    main()
