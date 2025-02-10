from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains as AC
import sqlite3

driver = webdriver.Firefox()
action = AC(driver)
options = webdriver.FirefoxOptions()
# options.page_load_strategy = 'eager'
options.add_argument('--disable-cache')
wait = WebDriverWait(driver, 20, 0.1)

login = 'login'
password = 'password'
post = 'https://vk.com/123456'
chats = ['Test 1', 'Test 2', 'Test 3', 'Test 12']

log_locator = ('id', 'index_email')
share_button_locator = ('xpath', '//div[@class="PostBottomAction PostBottomAction--withBg share _share"]')
chat_search_locator = ('xpath', '//input[@placeholder="Введите имя получателя или название чата"]')
send_chat_locator = ('xpath', '//div[@class="summary_tab3"]//nobr')


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


driver.get('https://vk.com')
time.sleep(5)
auth(login, password)
time.sleep(15)
driver.get('https://vk.com/123456')
time.sleep(5)
page_scroll()
for i in range(len(chats)):
    time.sleep(5)
    page_scroll()
    wait.until(EC.element_to_be_clickable(share_button_locator)).click()
    time.sleep(2)
    wait.until(EC.element_located_to_be_selected(chat_search_locator))
    chats_search = driver.find_element(*chat_search_locator)
    chats_search.clear()
    chats_search.send_keys(chats[i])  # Вписываем название чата
    time.sleep(1)
    chats_search.send_keys(Keys.ENTER)  # Закрепляем чат в строке куда отправляем сообщение
    time.sleep(1)
    wait.until(EC.element_located_to_be_selected(send_chat_locator))
    selected_chat = driver.find_element(*send_chat_locator)
    if selected_chat.text != chats[i]:
        print(chats[i], 'NO FOUND')  # Ненаход чата
        action.send_keys(Keys.ESCAPE)
        action.perform()
        continue
    else:
        print(chats[i], 'FOUND')  # Молодцы - чат совпал
        driver.find_element('xpath', '//span[@class="FlatButton__content"]').click()
    time.sleep(5)
    time.sleep(1)
    alert = len(driver.find_elements('xpath', '//div[@id="like_share_mail"]'))
    print(alert)
    if alert != 0:
        print(chats[i], 'SEND ERROR')  # Значит, нас исключили из чата
        action.send_keys(Keys.ESCAPE)
        action.perform()
        continue
    else:
        # driver.switch_to.default_content()
        driver.find_element('xpath', '//span[@class="FlatButton__content"]').click()
        print(chats[i], 'SEND')
