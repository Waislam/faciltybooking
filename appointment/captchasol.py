#pip3 install anticaptchaofficial
import os
import time

# below two lines to load .env file
from dotenv import load_dotenv
load_dotenv()

from anticaptchaofficial.imagecaptcha import *


api_key = os.environ.get('API_KEY')
#os.getenv('USERNAME')


def solution():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)

    captcha_text = solver.solve_and_return_solution(os.path.join('appointment/new.jpg'))
    while True:
        try:
            if captcha_text != 0:
                # print (captcha_text)
                return captcha_text
                break;
        except:
            print ("task finished with error "+solver.error_code)
            time.sleep(3)

