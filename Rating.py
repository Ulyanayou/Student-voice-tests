import pytest
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('URL')
username = os.getenv('USERNAME_ADMIN')
password = os.getenv('PASSWORD_ADMIN')

@pytest.fixture
def test_true_login(setup_browser):
    driver = setup_browser

    driver.get(url)

    login_field = driver.find_element('id', 'username')
    login_field.send_keys(username)

    password_field = driver.find_element('id', 'password')
    password_field.send_keys(password)

    login_button = driver.find_element('xpath', "//button[text()='Войти']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  
    login_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('xpath', "//h1[@class='admin-users__main-container-title']"))
    )

    assert driver.current_url == url + 'admin-users'
    return driver

# Поиск рейтинга института
def test_rating(test_true_login):
    driver = test_true_login

    report_button = driver.find_element('class name', 'btn-report')
    report_button.click()
    time.sleep(2)

    select_element = driver.find_element('xpath', "//select[@class='admin-report__select']")
    select = Select(select_element)

    select.select_by_value("77")

    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(('class name', "admin-report__select"))
    )

    select_elements = driver.find_elements('class name', "admin-report__select")

    if len(select_elements) > 1:
        second_select = select_elements[1] 
        select = Select(second_select)
        
        select.select_by_visible_text("Преподаватель")

    select_element = driver.find_element("class name", "admin-report__select")
    if len(select_elements) > 1:
        third_select = select_elements[2] 
        select = Select(third_select)
        
        select.select_by_visible_text("Иностранный язык")

    search_report_button = driver.find_element('xpath', "//button[@class='admin-report__action-btn admin-report__action-btn--search']")
    search_report_button.click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('xpath', "//h2[@class='admin-report__section-title']"))
    )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('xpath', "//span[@class='admin-report__rating-number']"))
    )

    try:
        h2_element = driver.find_element('xpath', "//h2[@class='admin-report__section-title']")
        span_element = driver.find_element('xpath', "//span[@class='admin-report__rating-number']")
        
        assert True
    except:
        assert False