from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains as AC
import sqlite3

# driver = webdriver.Firefox()
# action = AC(driver)
# options = webdriver.FirefoxOptions()
# # options.page_load_strategy = 'eager'
# options.add_argument('--disable-cache')
# wait = WebDriverWait(driver, 20, 0.1)

log_locator = ('id', 'index_email')


def auth(login, password):
    try:
        log = wait.until(EC.presence_of_element_located(log_locator))  # Поле для ввода логина
        log.clear()
        log.send_keys(login)
        log.send_keys(Keys.ENTER)  # Ввели логин и переходим на следующую страницу для ввода пароля
    except TimeoutException:
        print(f'Ошибка авторизации логина, {TimeoutException}')
    time.sleep(5)
    if len(driver.find_elements('xpath', '//span[@class="vkuiButton__in"]')) < 1:
        return False  # Проверяем, можно ли войти по паролю
    alternative_auth = wait.until(EC.element_to_be_clickable(driver.find_element('xpath', '//span['
                                                                                          '@class="vkuiButton__in"]')))
    # Находим кнопку для выбора способа входа
    alternative_auth.click()
    time.sleep(3)
    if len(driver.find_elements('xpath', '//div[@data-test-id="verificationMethod_password"]')) < 1:
        return False
    psw_button = wait.until(EC.element_to_be_clickable(driver.find_element('xpath', '//div[@data-test-id'
                                                                                    '="verificationMethod_password"]')))
    # Ждём, когда станет активной кнопка "пароль"
    psw_button.click()  # Переходим на страницу ввода пароля
    psw = driver.find_element('xpath', '//input[@name="password"]')
    psw.send_keys(password)
    psw.send_keys(Keys.ENTER)
    time.sleep(3)
    return True


def page_scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Прокрутка вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Пауза, пока загрузится страница.
        time.sleep(1)
        # Вычисляем новую высоту прокрутки и сравниваем с последней высотой прокрутки.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


db = sqlite3.connect('repost.sqlite3')
cur = db.cursor()
cur.execute("SELECT bot_tel FROM input WHERE candidate = 'Кондратьев'")
tel_result = list(cur.fetchall())
db.close()
print(tel_result)
for i in range(len(tel_result)):
    db = sqlite3.connect('repost.sqlite3')
    cur = db.cursor()
    cur.execute("SELECT bot_tel, bot_pass, chat_link FROM input WHERE bot_tel = '%s'" % tel_result[i])
    table_result = set(cur.fetchall())
    print(table_result, sep='$\n')
    print(len(table_result))
    db.close()
