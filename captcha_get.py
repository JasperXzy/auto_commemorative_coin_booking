import time
import os
import requests


url = f'https://eapply.abchina.com/coin/Helper/ValidCode.ashx'
if not os.path.exists('./pic_captcha'):
    os.makedirs('./pic_captcha')

for index in range(5000):
        file = f'./pic_captcha/captcha_{index}.png'
        re = requests.get(url)
        with open(file, 'wb') as f:
            f.write(re.content)
        print(f'captcha_{index} finished...')
        time.sleep(0.1)