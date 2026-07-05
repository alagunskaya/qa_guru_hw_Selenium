import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://qa-guru.github.io/one-page-form/text-box.html"


@pytest.fixture
def driver():
    """Фикстура для создания и закрытия драйвера"""
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    driver.maximize_window()
    yield driver
    driver.quit()


class TestTextBoxForm:
    TIMEOUT = 3

    def fill_form(self, driver, name, email, current_address, permanent_address):
        """Заполняет все поля формы"""
        driver.find_element(By.ID, "userName").send_keys(name)
        driver.find_element(By.ID, "userEmail").send_keys(email)
        driver.find_element(By.ID, "currentAddress").send_keys(current_address)
        driver.find_element(By.ID, "permanentAddress").send_keys(permanent_address)

    def submit_form(self, driver):
        """Нажимает кнопку Submit и ждет"""
        driver.find_element(By.ID, "submit").click()
        time.sleep(self.TIMEOUT)

    def get_result_text(self, driver):
        """Получает текст из блока результатов"""
        return driver.find_element(By.ID, "output").text

    def test_positive_valid_data(self, driver):
        """Позитивный тест: валидные данные"""

        self.fill_form(
            driver,
            "Иванов Иван",
            "ivanov@example.com",
            "460000 Оренбург, ул. Советская",
            "460000 Оренбург, ул. Советская"
        )

        self.submit_form(driver)
        result_text = self.get_result_text(driver)

        assert "Иванов Иван" in result_text
        assert "ivanov@example.com" in result_text
        assert "460000 Оренбург, ул. Советская" in result_text

        print("Positive_valid_data: passed")

    def test_positive_minimal_data(self, driver):
        """Позитивный тест: минимальные данные"""

        self.fill_form(driver, "А", "a@b.com", "1", "2")
        self.submit_form(driver)
        result_text = self.get_result_text(driver)

        assert "A" in result_text
        assert "a@b.com" in result_text
        assert "1" in result_text
        assert "2" in result_text

        print("Positive_minimal_data: passed")

    def test_negative_email_without_at(self, driver):
        """Негативный тест: email без @"""
        driver.find_element(By.ID, "userName").send_keys("Иван Иванов")
        driver.find_element(By.ID, "userEmail").send_keys("ivanov.example.com")

        self.submit_form(driver)
        result_text = self.get_result_text(driver)

        assert "ivanov.example.com" not in result_text, \
            f"Ожидался корректный email, но отправлен: '{result_text}'"
        print("Negative_email_without_at: passed")

    def test_negative_empty_form(self, driver):
        """Негативный тест: пустой email"""

        self.submit_form(driver)

        if driver.find_element(By.ID, "output").is_displayed():
            print("Negative test04: failed 'Возможна отправка пустой формы'")
        else:
            print("Negative_empty_form: passed")

    def test_negative_email_special_chars(self, driver):
        """Негативный тест: email с запрещенными спецсимволами"""

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
            time.sleep(self.TIMEOUT)

            driver.find_element(By.ID, "userName").send_keys("Иван Иванов")
            driver.find_element(By.ID, "userEmail").send_keys(invalid_email)

            self.submit_form(driver)
            result_text = self.get_result_text(driver)

            assert invalid_email not in result_text, \
                f"Ожидался корректный email, но отправлен: '{result_text}'"

        print("Negative_email_special_chars: passed")

    def test_security_sql_injection(self, driver):
        """Тест безопасности: SQL-инъекция"""
        sql_payloads = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "1; SELECT * FROM users"
        ]

        for payload in sql_payloads:
            driver.refresh()
            time.sleep(self.TIMEOUT)

            self.fill_form(driver, payload, "ivanov@example.com", payload, payload)

            self.submit_form(driver)
            result_text = self.get_result_text(driver)

            assert "error" not in result_text.lower() or "sql" not in result_text.lower()

        print("test_security_sql_injection: passed")

    def test_security_xss_injection(self, driver):
        """Тест безопасности: XSS-инъекция"""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x.jpg onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "onerror=alert('XSS')",
            "<svg/onload=alert('XSS')>",
        ]

        for payload in xss_payloads:
            driver.refresh()
            time.sleep(self.TIMEOUT)

            self.fill_form(driver, payload, "ivanov@example.com", payload, payload)

            self.submit_form(driver)
            result_text = self.get_result_text(driver)

            assert "<script>" not in result_text or "&lt;script&gt;" in result_text
            assert "onerror" not in result_text.lower() or "alert" not in result_text.lower()

        print("Security_xss_injection: passed")

    def test_negative_email_too_long(self, driver):
        """Негативный тест: слишком длинный email"""

        long_local = "a" * 200
        long_domain = "b" * 10
        long_email = f"{long_local}@{long_domain}.com"

        driver.find_element(By.ID, "userName").send_keys("Иван Иванов")
        driver.find_element(By.ID, "userEmail").send_keys(long_email)

        self.submit_form(driver)
        result_text = self.get_result_text(driver)

        assert long_email not in result_text, \
            f"Слишком длинный email: '{long_email}'"
        print("Negative_email_too_long: passed")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
