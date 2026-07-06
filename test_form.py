import time
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://qa-guru.github.io/one-page-form/text-box.html"


def test01():
    """Позитивный тест: валидные данные"""
    driver = webdriver.Chrome()

    try:
        driver.get(BASE_URL)
        driver.maximize_window()
        time.sleep(3)

        driver.find_element(By.ID, "userName").send_keys("Иванов Иван")

        driver.find_element(By.ID, "userEmail").send_keys("ivanov@example.com")

        driver.find_element(By.ID, "currentAddress").send_keys("460000 Оренбург, ул. Советская")

        driver.find_element(By.ID, "permanentAddress").send_keys("460000 Оренбург, ул. Советская")

        driver.find_element(By.ID, "submit").click()
        time.sleep(3)

        result_field = driver.find_element(By.ID, "output")
        result_text = result_field.text

        assert "Иванов Иван" in result_text
        assert "ivanov@example.com" in result_text
        assert "460000 Оренбург, ул. Советская" in result_text

        print("Positive test01: passed")

    finally:
        driver.quit()


def test02():
    """Позитивный тест: минимальные данные"""
    driver = webdriver.Chrome()

    try:
        driver.get(BASE_URL)
        driver.maximize_window()
        time.sleep(3)

        driver.find_element(By.ID, "userName").send_keys("А")

        driver.find_element(By.ID, "userEmail").send_keys("a@b.com")

        driver.find_element(By.ID, "currentAddress").send_keys("1")

        driver.find_element(By.ID, "permanentAddress").send_keys("2")

        driver.find_element(By.ID, "submit").click()
        time.sleep(3)

        result_field = driver.find_element(By.ID, "output")
        result_text = result_field.text

        assert "A" in result_text
        assert "a@b.com" in result_text
        assert "1" in result_text
        assert "2" in result_text

        print("Positive test02: passed")

    finally:
        driver.quit()


def test03():
    """Негативный тест: email без @"""
    driver = webdriver.Chrome()

    try:
        driver.get(BASE_URL)
        driver.maximize_window()

        driver.find_element(By.ID, "userName").send_keys("")

        driver.find_element(By.ID, "userEmail").send_keys("ivanov.example.com")

        driver.find_element(By.ID, "submit").click()
        time.sleep(3)

        result_field = driver.find_element(By.ID, "output")
        result_text = result_field.text

        assert "ivanov.example.com" not in result_text, f"Ожидался корректный email, но отправлен: '{result_text}'"
        print("Negative test03: passed")

    finally:
        driver.quit()


def test04():
    """Негативный тест: пустая форма"""
    driver = webdriver.Chrome()

    try:
        driver.get(BASE_URL)
        driver.maximize_window()
        time.sleep(3)

        driver.find_element(By.ID, "submit").click()
        time.sleep(3)

        if driver.find_element(By.ID, "output").is_displayed():
            print("Negative test04: failed 'Возможна отправка пустой формы'")
        else:
            print("Negative test04: passed")

    finally:
        driver.quit()


def test05():
    """Негативный тест: email с запрещенными спецсимволами"""
    driver = webdriver.Chrome()

    try:
        driver.get(BASE_URL)
        driver.maximize_window()
        time.sleep(3)

        invalid_emails = [
            "ivanov@ example.com",
            "ivanov@%example.com",
            "ivanov@>example.com",
            "ivanov@\"example.com",
            "ivanov@,example.com",
            "ivanov@#example.com"
        ]

        for invalid_email in invalid_emails:
            driver.refresh()
            time.sleep(3)

            driver.find_element(By.ID, "userName").send_keys("Иван Иванов")
            driver.find_element(By.ID, "userEmail").send_keys(invalid_email)

            driver.find_element(By.ID, "submit").click()
            time.sleep(3)

            result_field = driver.find_element(By.ID, "output")
            result_text = result_field.text

            assert invalid_email not in result_text, f"Ожидался корректный email, но отправлен: '{result_text}'"

        print("Negative test05: passed")

    finally:
        driver.quit()


def test06():
    """Тест безопасности: SQL-инъекция"""
    driver = webdriver.Chrome()

    try:
        driver.get(BASE_URL)
        driver.maximize_window()

        sql_payloads = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "1; SELECT * FROM users"
        ]

        for payload in sql_payloads:
            driver.refresh()
            time.sleep(2)

            driver.find_element(By.ID, "userName").send_keys(payload)
            driver.find_element(By.ID, "userEmail").send_keys("ivanov@example.com")
            driver.find_element(By.ID, "currentAddress").send_keys(payload)
            driver.find_element(By.ID, "permanentAddress").send_keys(payload)

            driver.find_element(By.ID, "submit").click()
            time.sleep(2)

            result_text = driver.find_element(By.ID, "output").text
            assert "error" not in result_text.lower() or "sql" not in result_text.lower()

        print("Security test06: passed")

    finally:
        driver.quit()


def test07():
    """Тест безопасности: XSS-инъекция"""
    driver = webdriver.Chrome()

    try:
        driver.get(BASE_URL)
        driver.maximize_window()

        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x.jpg onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "onerror=alert('XSS')",
            "<svg/onload=alert('XSS')>",
        ]

        for payload in xss_payloads:
            driver.refresh()
            time.sleep(5)

            driver.find_element(By.ID, "userName").send_keys(payload)
            driver.find_element(By.ID, "userEmail").send_keys("ivanov@example.com")
            driver.find_element(By.ID, "currentAddress").send_keys(payload)
            driver.find_element(By.ID, "permanentAddress").send_keys(payload)

            driver.find_element(By.ID, "submit").click()
            time.sleep(5)

            result_text = driver.find_element(By.ID, "output").text
            assert "<script>" not in result_text or "&lt;script&gt;" in result_text
            assert "onerror" not in result_text.lower() or "alert" not in result_text.lower()

        print("Security test07: passed")

    finally:
        driver.quit()


def test08():
    driver = webdriver.Chrome()

    try:
        driver.get(BASE_URL)
        driver.maximize_window()
        time.sleep(3)

        long_local = "a" * 200
        long_domain = "b" * 10
        long_email = f"{long_local}@{long_domain}.com"

        driver.find_element(By.ID, "userName").send_keys("Иван Иванов")
        driver.find_element(By.ID, "userEmail").send_keys(long_email)

        driver.find_element(By.ID, "submit").click()
        time.sleep(5)

        result_field = driver.find_element(By.ID, "output")
        result_text = result_field.text

        assert long_email not in result_text, f"Ожидался корректный email, но отправлен: '{result_text}'"
        print("Negative test08: passed")

    finally:
        driver.quit()


print("ЗАПУСК ТЕСТОВ...")
test01()
test02()
test03()
test04()
test05()
test06()
test07()
test08()
print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
