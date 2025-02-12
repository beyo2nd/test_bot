import asyncio
from selenium import webdriver
from aiogram.types import FSInputFile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from database import requests as rq
import keyboard
import time
from datetime import datetime
import os

from config_reader import config
from aiogram import Bot, Dispatcher
bot = Bot(config.bot_token.get_secret_value())

# Настройка драйвера для Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


driver.get("https://b24-iu5stq.bitrix24.site/backend_test/")

# Заполнение формы
async def fill_form():
    # Получаем пользователя с InQueue = True
    user = await rq.get_inqueue_user()
    if user:
        name, surname, email, phone_number, birth_date = user.name, user.surname, user.email, user.phone_number, user.birth_date
        name_field = driver.find_element(By.NAME, 'name')
        surname_field = driver.find_element(By.NAME, 'lastname')
        button = driver.find_element(By.CSS_SELECTOR, ".b24-form-btn-block button")
        
        name_field.clear()
        surname_field.clear()
        
        name_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'name')))
        surname_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'lastname')))
        button = driver.find_element(By.CSS_SELECTOR, ".b24-form-btn-block button")

        # Имитируем клик на поле имени
        actions = ActionChains(driver)
        actions.move_to_element(name_field).click().perform()
        # Вводим имя
        time.sleep(0.2)
        keyboard.write(f"{name}")
        actions.move_to_element(surname_field).click().perform()
        time.sleep(0.1)
        keyboard.write(f"{surname}")
        
        # Имитируем клик на кнопку
        button.click()
        time.sleep(0.1)
        
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
        phone_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'phone')))
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Далее')]")))
        
        email_field.clear()
        phone_field.clear()
        
        actions.move_to_element(email_field).click().perform()
        time.sleep(0.2)
        keyboard.write(f"{email}")
        actions.move_to_element(phone_field).click().perform()
        time.sleep(0.1)
        keyboard.write(f"{phone_number[1:-1]}")
        
        button.click()
        time.sleep(0.1)
        
        date_list = list(map(str, birth_date.split(".")))
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Далее')]")))
                                                 
        date_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Дата рождения')]")))
        actions.move_to_element(date_field).click().perform()
        
        year_select = Select(driver.find_element(By.XPATH, "//div[@class='vdpPeriodControls']//div[2]//select"))
        year_select.select_by_value(date_list[2])
        
        month_select = Select(driver.find_element(By.XPATH, "//div[@class='vdpPeriodControl']//select"))
        month_select.select_by_value(str(int(date_list[1])-1))

        day_element = driver.find_element(By.XPATH, f"//div[@class='vdpCellContent' and text()='{date_list[0]}']")
        day_element.click()
        time.sleep(0.2)
        button.click()
        print(f"Пользователь f{user.tg_id ,name, surname, email, phone_number, birth_date} заполнил форму")
        time.sleep(3)

        # Получаем скриншот страницы
        screenshot = driver.get_screenshot_as_png()

        # Папка для сохранения изображений
        screenshot_dir = "img"
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M')}_{user.tg_id}.jpg"
        full_path = os.path.join(screenshot_dir, filename)
        with open(full_path, 'wb') as file:
            file.write(screenshot)

        
        print(f"скриншот сохранён в {full_path}")
        
        driver.quit()
        await rq.set_inqueue_false(user.id)
        await bot.send_photo(user.tg_id, photo = FSInputFile(full_path), caption= "Фото готового запроса")
    else:
        print("Нет пользователей в очереди")

asyncio.run(fill_form())