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

# Редактирование профиля преподавателя (поля активность и видимость отзывов)
def test_edit_user(test_true_login):
    driver = test_true_login 
    search = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/form/input')
    search.send_keys('Иванов Иван Иванович')
    search_button = driver.find_element('xpath', '//*[@id="root"]/main/div/div[1]/form/button')
    search_button.click()

    user_edit = driver.find_element('xpath', '//*[@id="root"]/main/div/ul/li[1]/div[2]/a[2]')
    user_edit.click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(('xpath', '//*[@id="isActive"]'))
    )
    is_active = driver.find_element('xpath', '//*[@id="isActive"]')
    driver.execute_script("arguments[0].click();", is_active)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(('xpath', '//*[@id="visibleReviews"]'))
    )
    visible_reviews = driver.find_element('xpath', '//*[@id="visibleReviews"]')
    driver.execute_script("arguments[0].click();", visible_reviews)

    apply_edit_button = driver.find_element('xpath', "//button[text()='Применить']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    apply_edit_button.click()

