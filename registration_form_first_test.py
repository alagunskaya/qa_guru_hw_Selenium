import time
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

@pytest.fixture
def driver():
    """Фикстура для инициализации и завершения драйвера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(3)
    yield driver
    driver.quit()


def test_fill_entire_form(driver, timeout=10):
    """Тест заполнения всей формы регистрации студента"""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, timeout)

    # Проверка заголовков формы
    form_title = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/h1")))
    assert form_title.text == "Practice Form"

    time.sleep(5)

    form_sub_title = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/div/p")))
    assert form_sub_title.text == "Student Registration Form"

    # Закрытие баннера
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Level up your automation')]")))
    close_banner_btn = wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="fixedban"]/div/div/button""")))
    close_banner_btn.click()
    wait.until(EC.invisibility_of_element(close_banner_btn))

    # Name
    first_name = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
    first_name.send_keys("Ivanov")
    last_name = driver.find_element(By.ID, "lastName")
    last_name.send_keys("Ivan")

    # Gender
    email = driver.find_element(By.ID, "userEmail")
    email.send_keys("ivan.ivanov@example.com")

    # Male
    gender_male_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='gender-radio-1']")))
    gender_male_label.click()

    # Mobile (10 Digits)
    mobile_number = driver.find_element(By.ID, "userNumber")
    mobile_number.send_keys("9951111111")

    # Date of Birth
    date_input = driver.find_element(By.ID, "dateOfBirthInput")
    date_input.click()
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "react-datepicker__month-container")))

    month_select = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__month-select")))
    month_select.click()
    month_select.find_element(By.XPATH, "//option[@value='11']").click()

    year_select = driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")
    year_select.click()
    year_select.find_element(By.XPATH, "//option[@value='1989']").click()

    day_element = driver.find_element(By.CSS_SELECTOR,".react-datepicker__day--020:not(.react-datepicker__day--outside-month)")
    day_element.click()

    # Subjects
    subjects_input = wait.until(EC.element_to_be_clickable((By.ID, "subjectsInput")))
    subjects_input.send_keys("Maths")
    subjects_input.send_keys(Keys.ENTER)

    # Hobbies
    hobby_sports = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='hobbies-checkbox-2']")))
    hobby_sports.click()
    hobby_music = driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']")
    hobby_music.click()

    # Picture
    temp_file_path = os.path.abspath("test_image.jpg")
    with open(temp_file_path, "w") as f:
        f.write("fake image data")

    upload_input = driver.find_element(By.ID, "uploadPicture")
    upload_input.send_keys(temp_file_path)

    # Current Address
    current_address = driver.find_element(By.ID, "currentAddress")
    current_address.send_keys("Moscow")

    # Скролл и скрытие футера
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("document.getElementsByTagName('footer')[0].style.display='none';")

    # State and City
    state_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "state")))
    state_dropdown.click()
    state_option = wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="stateCity-wrapper"]/div[1]""")))
    state_option.click()

    city_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "city")))
    city_dropdown.click()
    city_option = wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="stateCity-wrapper"]/div[1]""")))
    city_option.click()

    # Отправка формы
    submit_button = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].click();", submit_button)

    # Проверка результатов
    modal_title = wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
    assert modal_title.text == "Thanks for submitting the form"

    time.sleep(5)

    result_table = driver.find_element(By.CLASS_NAME, "table-responsive")
    assert "Ivanov Ivan" in result_table.text
    assert "ivan.ivanov@example.com" in result_table.text
    assert "Male" in result_table.text
    assert "995111111" in result_table.text
    assert "20 Dec 1989" in result_table.text
    assert "Maths" in result_table.text
    assert "Reading, Music" in result_table.text
    assert "test_image.jpg" in result_table.text
    assert "Moscow" in result_table.text
    assert "NCR Delhi" in result_table.text

    # Удаление временного файла
    if os.path.exists("test_image.jpg"):
        os.remove("test_image.jpg")