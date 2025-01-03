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

# Создание пользователя преподавателя
@pytest.mark.parametrize("surname, firstname, lastname", [
    ("Иванов", "Иван", "Иванович"),
    ("Петров", "Петр", "Петрович")
])
def test_true_create_user_teacher(test_true_login, surname, firstname, lastname):
    driver = test_true_login

    create_button = driver.find_element('xpath', "//a[@class='admin-users__add-user']")
    create_button.click()

    create_user_field_surname = driver.find_element('id', 'surName')
    create_user_field_surname.send_keys(surname)

    create_user_field_firstname = driver.find_element('id', 'firstName')
    create_user_field_firstname.send_keys(firstname)

    create_user_field_lastname = driver.find_element('id', 'LastName')
    create_user_field_lastname.send_keys(lastname)

    select_element = driver.find_element('id', 'role')
    select = Select(select_element)
    select.select_by_value('teacher')

    select_element = driver.find_element('id', 'institute')
    select = Select(select_element)
    select.select_by_value('77')

    create_user_field_login = driver.find_element('id', 'login')
    create_user_field_login.send_keys(f"{surname}_{firstname}_{lastname}")

    
    create_user_field_password = driver.find_element('xpath', "//button[text()='Генерировать']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  
    create_user_field_password.click()

    create_user_field_button = driver.find_element('xpath', "//button[text()='Применить']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    create_user_field_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('xpath', "//h1[@class='admin-users__main-container-title']"))
    )

    assert driver.current_url == url + 'admin-users'

# Создание пользователя администратора
@pytest.mark.parametrize("surname, firstname, lastname", [
    ("Иванов", "Петр", "Иванович")
])
def test_true_create_user_admin(test_true_login, surname, firstname, lastname):
    driver = test_true_login

    create_button = driver.find_element('xpath', "//a[@class='admin-users__add-user']")
    create_button.click()

    create_user_field_surname = driver.find_element('id', 'surName')
    create_user_field_surname.send_keys(surname)

    create_user_field_firstname = driver.find_element('id', 'firstName')
    create_user_field_firstname.send_keys(firstname)

    create_user_field_lastname = driver.find_element('id', 'LastName')
    create_user_field_lastname.send_keys(lastname)

    select_element = driver.find_element('id', 'role')
    select = Select(select_element)
    select.select_by_value('admin')

    select_element = driver.find_element('id', 'institute')
    select = Select(select_element)
    select.select_by_value('77')

    create_user_field_login = driver.find_element('id', 'login')
    create_user_field_login.send_keys(f"{surname}_{firstname}_{lastname}")

    
    create_user_field_password = driver.find_element('xpath', "//button[text()='Генерировать']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  
    create_user_field_password.click()

    create_user_field_button = driver.find_element('xpath', "//button[text()='Применить']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    create_user_field_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('xpath', "//h1[@class='admin-users__main-container-title']"))
    )

    assert driver.current_url == url + 'admin-users'

# Пользователь не должен создаваться с полями, заполненными цифрами и спец. символами
@pytest.mark.parametrize("surname, firstname, lastname", [
    ("1234", "1234", "1234"),
    ("@#&$", "@#$&", "@#$&"),
    ("+ @#8$", "@#$ _", "76№")
])
def test_false_create_user_teacher(test_true_login, surname, firstname, lastname):
    driver = test_true_login

    create_button = driver.find_element('xpath', "//a[@class='admin-users__add-user']")
    create_button.click()

    create_user_field_surname = driver.find_element('id', 'surName')
    create_user_field_surname.send_keys(surname)

    create_user_field_firstname = driver.find_element('id', 'firstName')
    create_user_field_firstname.send_keys(firstname)

    create_user_field_lastname = driver.find_element('id', 'LastName')
    create_user_field_lastname.send_keys(lastname)

    select_element = driver.find_element('id', 'role')
    select = Select(select_element)
    select.select_by_value('teacher')

    select_element = driver.find_element('id', 'institute')
    select = Select(select_element)
    select.select_by_value('77')

    create_user_field_login = driver.find_element('id', 'login')
    create_user_field_login.send_keys(f"{surname}_{firstname}_{lastname}")
    
    create_user_field_password = driver.find_element('xpath', "//button[text()='Генерировать']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  
    create_user_field_password.click()

    create_user_field_button = driver.find_element('xpath', "//button[text()='Применить']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    create_user_field_button.click()
    time.sleep(1)

    assert driver.current_url == url + 'admin-user-create'

