import os
import threading
import time
import cv2
import ocr_jasper
import general_settings
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from pymysql import Connection

global captcha_success
captcha_success = False


def main_func(thread_index: int, place: list, date: str, input_enable: bool):
    """
    主进程
    :param thread_index: 进程序号
    :param place: 预约地址列表
    :param date: 预约时间
    :param input_enable: 是否为最后一个进程
    :return: None
    """
    global captcha_success
    browser = webdriver.Chrome(service=general_settings.path_chrome)  # 使用 Chrome 驱动
    # browser = webdriver.Edge(service=general_settings.path_edge)  # 使用 Edge 驱动
    browser.get(general_settings.booking_url)

    def welcome_page():
        """
        欢迎页面函数
        :return: None
        """
        browser.find_element(By.XPATH, general_settings.welcome_page_xpath).click()
        browser.find_element(By.XPATH, '//*[@id="I128"]/button[1]').click()  # 同意并继续

    def info_get(host: str, port: int, user: str, password: str, database: str, table: str):
        """
        通过 MySQL 数据库获取信息
        :param host: 主机名
        :param port: 端口
        :param user: 账户
        :param password: 密码
        :param database: 信息所在数据库
        :param table: 信息所在表
        :return: 信息的元组
        """
        info_MySQL = Connection(
            host=host,
            port=port,
            user=user,
            password=password
        )  # 连接数据库
        cursor = info_MySQL.cursor()  # 创建游标
        info_MySQL.select_db(database)  # 选择数据库
        cursor.execute(f'SELECT *  FROM {table};')
        result = cursor.fetchall()  # 获取所有信息
        info_mysql = result[thread_index]  # 获取对应进程的信息
        cursor.close()
        info_MySQL.close()
        return info_mysql

    def fill_info(info: tuple):
        """
        填写信息函数
        :param info: 信息元组
        :return: None
        """
        browser.find_element(By.XPATH, '//*[@id="name"]').send_keys(info[1])  # 姓名
        browser.find_element(By.XPATH, '//*[@id="identNo"]').send_keys(info[2])  # 身份证号
        browser.find_element(By.XPATH, '//*[@id="mobile"]').send_keys(info[3])  # 电话号码

    def choose_place(province: str, city: str, country: str, default_bank_index: int):
        """
        选择兑换网点函数
        :param province: 省行名称
        :param city: 分行名称
        :param country: 支行名称
        :param default_bank_index: 默认营业处序号（从 1 开始为第一个营业处）
        :return: None
        """
        select_province = browser.find_element(By.XPATH, '//*[@id="orglevel1"]')  # 选择省行
        Select(select_province).select_by_visible_text(province)

        select_city = browser.find_element(By.XPATH, '//*[@id="orglevel2"]')  # 选择分行
        Select(select_city).select_by_visible_text(city)

        select_country = browser.find_element(By.XPATH, '//*[@id="orglevel3"]')  # 选择支行
        Select(select_country).select_by_visible_text(country)

        select_bank = browser.find_element(By.XPATH, '//*[@id="orglevel4"]')  # 选择营业处
        bank_text = select_bank.text
        bank_arr = bank_text.split("\n")
        default_coin_number = bank_arr[default_bank_index].split(" ")

        # 判断该营业处是否有剩余纪念币
        if int(default_coin_number[1]) >= 20:
            Select(select_bank).select_by_index(default_bank_index)
        else:
            for bank_index in range(1, len(bank_arr)):
                coin_number = bank_arr[bank_index].split(" ")
                if int(coin_number[1]) >= 20:
                    Select(select_bank).select_by_index(bank_index)
                    break
                else:
                    print(f"进程{thread_index} 没有营业厅有纪念币了...")
                    break

    def coin_date(coindate: str):
        """
        选择兑换时间函数
        :param coindate: 按照'年-月-日'输入日期，例如：'2023-01-01'
        :return: None
        """
        js_date = 'document.getElementById("coindate").removeAttribute("readonly");'  # 执行 js 代码去除 readonly 属性
        browser.execute_script(js_date)
        browser.find_element(By.ID, 'coindate').clear()  # 清除输入框
        browser.find_element(By.ID, 'coindate').send_keys(coindate)  # 输入日期

    def pic_captcha_save():
        """
        定位验证码进行截图
        :return: None
        """
        captcha_img = browser.find_element(By.XPATH, '//*[@id="piccaptcha"]')  # 要截图的元素
        x, y = captcha_img.location.values()  # 坐标
        h, w = captcha_img.size.values()  # 宽高
        image_data = browser.get_screenshot_as_png()  # 把截图以二进制形式的数据返回
        screenshot = Image.open(BytesIO(image_data))  # 以新图片打开返回的数据
        result = screenshot.crop((x, y, x + w, y + h))  # 对截图进行裁剪
        result.save(f'./captcha/pic_captcha_thread{thread_index}.png')

    def pic_captcha_recognition():
        """
        使用 ocr_jasper 识别验证码
        :return: None
        """
        ocr_pic = ocr_jasper.OCR(import_onnx_path='./models/model.onnx',charsets_path="./models/charsets.json")
        with open(f'./captcha/pic_captcha_thread{thread_index}.png', 'rb') as f:
            image = f.read()
        captcha_recognized = ocr_pic.classification(image)
        browser.find_element(By.XPATH, '//*[@id="piccode"]').send_keys(captcha_recognized)  # 验证码输入框

    def get_text_captcha():
        """
        短信验证码函数
        :return: None
        """
        browser.find_element(By.XPATH, '//*[@id="sendValidate"]').click()  # 获取短信验证码

    def captcha():
        """
        判断图形验证码是否正确
        :return: None
        """
        global captcha_success
        while True:
            pic_captcha_save()
            time.sleep(1)
            pic_captcha_recognition()
            get_text_captcha()
            time.sleep(0.5)
            is_captcha_error = browser.find_element(By.XPATH, '//*[@id="errorCaptchaNo"]').text
            if len(is_captcha_error) == 7:
                browser.find_element(By.XPATH, '//*[@id="piccaptcha"]').click()  # 重新获取验证码
                browser.find_element(By.XPATH, '//*[@id="piccode"]').clear()
            elif len(is_captcha_error) == 10:
                captcha_success = True
                break

    def text_captcha_save():
        """
        保存验证码的屏幕截图并裁剪验证码
        :return: None
        """
        text_captcha_path = f'./captcha/text_captcha_tmp{thread_index}.png'
        os.system('adb shell screencap -p > ' + text_captcha_path)
        with open(text_captcha_path, 'rb') as f:
            data = f.read()
        text_captcha = data.replace(b'\r\n', b'\n')
        with open(f'./captcha/text_captcha_tmp{thread_index}.png', 'wb') as f:
            f.write(text_captcha)
        raw_image = cv2.imread(f'./captcha/text_captcha_tmp{thread_index}.png')
        cropped_image = raw_image[general_settings.y_0:general_settings.y_1, general_settings.x_0:general_settings.x_1]  
        cv2.imwrite(f'./captcha/text_captcha_{thread_index}.png', cropped_image)

    def text_captcha_recognition():
        """
        验证码识别
        :return: None
        """
        ocr_text = ocr_jasper.OCR(use_gpu=True)
        with open(f'./captcha/text_captcha_{thread_index}.png', 'rb') as f:
            image = f.read()
        captcha_recognized = ocr_text.classification(image)
        browser.find_element(By.XPATH, '//*[@id="phoneCaptchaNo"]').send_keys(captcha_recognized)

    def info_submit():
        """
        提交信息函数
        :return: None
        """
        browser.find_element(By.XPATH, '//*[@id="infosubmit"]').click()  # 提交信息

    try:
        welcome_page()
        info_tuple = info_get(host=general_settings.host,
                              port=general_settings.port,
                              user=general_settings.user,
                              password=general_settings.password,
                              database=general_settings.database,
                              table=general_settings.table)
        fill_info(info=info_tuple)
        choose_place(place[0], place[1], place[2], place[3])
        coin_date(coindate=date)
        captcha()
        time.sleep(3)
        text_captcha_save()
        text_captcha_recognition()
        info_submit()
    except Exception as e:
        print(e)
    if input_enable:
        input()


is_input_enable = False
for current_thread in range(general_settings.threads):
    if current_thread == general_settings.threads - 1:
        is_input_enable = True
    threading.Thread(target=main_func, args=(current_thread,
                                             general_settings.place_arr,
                                             general_settings.coindate,
                                             is_input_enable)).start()
    while True:
        if captcha_success:
            time.sleep(1)
            captcha_success = False
            break
        else:
            time.sleep(0.1)
