import random
import threading
import os
import time
import requests
import base64
import eventlet

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

# below to handle properly filling input field
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from appointment.reading import ReadWrite # to read inputed file
from appointment.output import write_result
import pyautogui as pg # this is for mouse move and take action like human pip install pyautogui "print(pg.position())" "pg.moveTo(728, 906, 2)" "pg.click(x=842, y=473)"

from .captchasol import solution

class FacilityBooking:
    # service_obj = Service(ChromeDriverManager().install())
    # service_obj = Service(os.path.join('appointment/chromedriver.exe'))
    # options = Options()

    # options.add_experimental_option("excludeSwitches", ["enable-automation"])  # one
    #     # options.add_experimental_option('useAutomationExtension', False)  # two
    #     # options.add_argument('--disable-blink-features=AutomationControlled')  # three  these three option is called "Removing Navigator.Webdriver Flag"
    #     # options.add_argument('--disable-notifications')  # one this is to stop showing notificationn like "Save password" (working)
    #     # prefs = {"profile.default_content_setting_values.notifications": 2}  # two
    #     # options.add_experimental_option("prefs", prefs)  # three above three lines of code ignoring the "Save password" popup from chrome (called browser notifictaion)
    #     # options.add_argument('--no-sandbox')
    #     # options.add_argument('--disable-dev-shm-usage')

    def __init__(self):
        pass

    def delay(self):
        time.sleep(random.randint(2, 3))

    def wait60sec(self, driver):
        driver.implicitly_wait(60)

    def read_csv(self):
        read = ReadWrite()
        self.user_list = read.data_list
        read.read_data()

    def capsol(self):
        result = solution()
        return result

    def download_img(self, src):
        '''method to download img from hcaptcha and read that'''
        head, data = src.split(',', 1)
        file_ext = head.split(';')[0].split('/')[1]
        plain_data = base64.b64decode(data)
        with open('appointment/new.' + file_ext, 'wb') as f:
            f.write(plain_data)


    def click_on_img_text(self, driver, captcha_text):
        '''this method will click on every img solved from anti captcha'''
        #==== deselect already seleted item========
        # already_seleted_item = driver.find_element(By.XPATH, "//div[@class='kbkey button red_selected sel']").click()
        # time.sleep(1)
        #===== new selet actual true result======
        all_items = driver.find_elements(By.XPATH, "//div[@class='kbkey button red']")
        captcha_text_list = list(captcha_text)
        for text in captcha_text_list:
            text_text = text.strip()
            for item in all_items:
                item_text = item.text.strip()
                if item_text == text_text:
                    item.click()
                    time.sleep(0.5)
                    break;
                continue;



    def capcha_solved(self, driver):
        '''this method will solve the captcha from img download to click on img'''
        # =================download img=============
        self.wait60sec(driver)
        # driver.implicitly_wait(2)
        img_code = driver.find_element(By.XPATH, "//div[@id='inputTextWrapper']/div/img").get_attribute("src").strip()
        self.download_img(img_code)

        # ======================= get anti-captcha response =============
        captcha_text = self.capsol()
        print(captcha_text)


        # ================= click on captcha img button =====
        self.click_on_img_text(driver, captcha_text)


    def non_registered_patron(self, driver, hkid, hkiddigit, telephone, leisurelinkn, password):
        '''this method to fill form as non-registered'''
        # self.wait60sec(driver)
        driver.implicitly_wait(4)
        time.sleep(3)
        #========= switch to frame =============
        myframe = driver.find_element(By.XPATH, "//frame[@name='main']")
        driver.switch_to.frame(myframe)

        if hkid == 'Null':
            #=======check leisure link ============
            driver.find_element(By.XPATH, "//input[@name='patronFlag']").click()
            # input leisure link number
            driver.find_element(By.XPATH, "//input[@name='leisureLinkId']").send_keys(leisurelinkn) #leusirelink number
            driver.find_element(By.XPATH, "//div[@id='tableLayout']/input[@type='password']").send_keys(password) #password input
        else:
            #=========check radio button ==============
            driver.find_element(By.XPATH, "//input[@id='radNonRegId']").click()

            driver.find_element(By.XPATH, "//input[@id='hkId']").send_keys(hkid) #HKID number
            driver.find_element(By.XPATH, "//input[@id='hkIdCheckDigit']").send_keys(hkiddigit) #hkIdCheckDigit
            driver.find_element(By.XPATH, "//input[@id='telephoneNo']").send_keys(telephone) #telephoneNo

        #========= time to solve captcha with five digit again ================
        self.capcha_solved(driver)


        #========== go to the next page by clicking on continue button again ===========
        time.sleep(2)
        driver.find_element(By.XPATH, "//input[@value='Continue']").click()

        # retry solving captcha if there is any
        while True:
            try:
                driver.implicitly_wait(5)
                # error_text = driver.find_element(By.XPATH, "//ol[@class='errormsg']/li").text.strip()
                error_text = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//ol[@class='errormsg']/li" ))) #driver.find_element(By.XPATH, "//ol[@class='errormsg']/li")
                # if 'please enter again' in error_text:
                # if error_text:
                # =========check radio button ==============
                driver.find_element(By.XPATH, "//input[@id='radNonRegId']").click()

                driver.find_element(By.XPATH, "//input[@id='hkId']").send_keys(hkid)  # HKID number
                driver.find_element(By.XPATH, "//input[@id='hkIdCheckDigit']").send_keys(hkiddigit)  # hkIdCheckDigit
                driver.find_element(By.XPATH, "//input[@id='telephoneNo']").send_keys(telephone)  # telephoneNo

                #==== solve captcha again =====
                self.capcha_solved(driver)
                # ========== go to the next page by clicking on continue button again ===========
                time.sleep(2)
                driver.find_element(By.XPATH, "//input[@value='Continue']").click()
            except:
                print('no more captcha on none _r page')
                break;

    def payment(self, driver, account, pin):
        ''' this method will handle payment options'''
        driver.implicitly_wait(3)
        # click on payment method option Point(x=842, y=473)
        iframe_code = driver.find_element(By.XPATH, "//iframe[@class='pay-iframe']")
        # switch to iframe
        driver.switch_to.frame(iframe_code)
        time.sleep(1)
        # click on pps payment button
        driver.find_element(By.XPATH, "//div[@class='btn paymentMethod pps-group']").click()

        # now click on paybutton
        time.sleep(1)
        # driver.find_element(By.XPATH, "//span[@id='btnPayLable']")
        driver.find_element(By.XPATH, "//button[@id='btnPay']").click()


        # In the next page where need enter bank credentials
        # now sweitch to default
        driver.implicitly_wait(10)
        time.sleep(2)
        #driver.switch_to.default_content()
        # input account number
        driver.find_element(By.XPATH, "//input[@name='ACCOUNTNO']").send_keys(account)

        # input pin number here
        driver.find_element(By.XPATH, "//input[@name='PIN']").send_keys(pin)

        # select the TNC check box
        driver.find_element(By.XPATH, "//input[@name='TNC']").click()

        #=============== submit the payment ==============
        time.sleep(10)
        time.sleep(1)
        driver.find_element(By.XPATH, "//a/img[@id='submitBut']").click() # clicked on submit button




    def booking_details(self, driver, dated, facility, type, time_schedule, area, venu1, location1, venu2, location2, venu3, location3,
                        concession, name, email):
        '''filling booking details'''
        time.sleep(2)
        date_list = driver.find_elements(By.XPATH, "//input[@class='calendarNormalDay']")
        for date in date_list:
            choose_date = date.get_attribute('value').strip()
            if choose_date == dated:
                date.click()
                break;
            continue;

        #===== select facility =======
        facility_option = Select(driver.find_element(By.XPATH, "//div[@id='facilityPanel']/select[@class='gwt-ListBox resListBox']"))
        facility_option.select_by_value(facility)

        # select type
        f_type = Select(driver.find_element(By.XPATH, "//div[@id='facilityTypePanel']/select[@class='gwt-ListBox resListBox']"))
        f_type.select_by_value(type)

        #time selection
        f_time = Select(driver.find_element(By.XPATH, "//div[@id='sessionTimePanel']/select[@class='gwt-ListBox resListBox']"))
        f_time.select_by_value(time_schedule)

        # area
        f_area = Select(driver.find_element(By.XPATH, "//div[@id='areaPanel']/select[@class='gwt-ListBox resListBox']"))
        f_area.select_by_value(area)




        # Venue 1 selection
        if venu1 != 'Null':
            f_venu = Select(driver.find_element(By.XPATH, "//div[@id='preference1.venuePanel']/select[@class='gwt-ListBox resListBox']"))
            f_venu.select_by_value(venu1)
            # venu1 location
            venu_location1 = Select(driver.find_element(By.XPATH, "//div[@id='preference1.locationPanel']/select[@class='gwt-ListBox resListBox']"))
            venu_location1.select_by_value(location1)
        else:
            pass

        # Venue 2 selection
        if venu2 != 'Null':
            f2_venu = Select(driver.find_element(By.XPATH, "//div[@id='preference2.venuePanel']/select[@class='gwt-ListBox resListBox']"))
            f2_venu.select_by_value(venu2)
            # venu2 location
            venu_location2 = Select(driver.find_element(By.XPATH, "//div[@id='preference2.locationPanel']/select[@class='gwt-ListBox resListBox']"))
            venu_location2.select_by_value(location2)
        else:
            pass

        # Venue 3 selection
        if venu3 != 'Null':
            f3_venu = Select(driver.find_element(By.XPATH, "//div[@id='preference3.venuePanel']/select[@class='gwt-ListBox resListBox']"))
            f3_venu.select_by_value(venu3)
            # venu3 location
            venu_location3 = Select(driver.find_element(By.XPATH, "//div[@id='preference3.locationPanel']/select[@class='gwt-ListBox resListBox']"))
            venu_location3.select_by_value(location3)
        else:
            pass




        # click on enquery
        driver.find_element(By.XPATH, "//input[@value='Enquiry']").click()

        #click on first time (available session)
        time.sleep(1)
        single_time = driver.find_elements(By.XPATH, "//td[@class='timeslotCellNonPeak']/span[@class='noborder']/input[@type='checkbox']")[0]
        single_time.click()

        #click on Book button
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[@value='Book']").click()

        #============ input contact information ==========
        driver.implicitly_wait(3)
        # clicking on yes or No button for concession
        yes_button = driver.find_element(By.XPATH, "//input[@id='concessYes']")
        no_button = driver.find_element(By.XPATH, "//input[@id='concessNo']")
        if concession == 'Y':
            yes_button.click()
        else:
            no_button.click()


        driver.find_element(By.XPATH, "//input[@name='name']").send_keys(name)
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[@name='emailAddress']").send_keys(email)

        # click on yes button of condition
        driver.find_element(By.XPATH, "//input[@value='Y']").click()
        time.sleep(1)

        # now click on continue button
        driver.find_element(By.XPATH, "//input[@value='Continue']").click()

        #============ pay oneline option page ===========
        #click on continue button to go to payment option
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH, "//input[@value='Continue']").click()



    def booking(self, hkid, hkiddigit, telephone, date, facility, type, time_schedule, area, venu1, location1, venu2, location2, venu3, location3,
                                                            concession, name, email,
                                                            account, pin,
                                                            leisurelinkn, password):
        # driver = webdriver.Chrome(service=self.service_obj, options=self.options)
        driver = uc.Chrome()
        driver.maximize_window()

        self.wait60sec(driver)
        driver.get('https://w2.leisurelink.lcsd.gov.hk/index/index.jsp?lang=en')
        # driver.get('https://w2.leisurelink.lcsd.gov.hk/leisurelink/application/checkCode.do?flowId=1&lang=EN')
        self.wait60sec(driver)
        #===click on facility booking button====
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[@id='LCSD_1']").click()

        #=========switch window ====================
        time.sleep(2)
        # window_handles[1] is a second window
        driver.implicitly_wait(5)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])

        # ==== deselect already seleted item========
        self.wait60sec(driver)
        already_seleted_item = driver.find_element(By.XPATH, "//div[@class='kbkey button red_selected sel']").click()
        time.sleep(1)

        #=========== implement captcha solving code here =========
        self.capcha_solved(driver)

        #============= continue to the next level============
        driver.find_element(By.XPATH, "//input[@class='actionBtnContinue']").click()

        # retry solving captcha if there is any
        while True:
            try:
                print('value 1')
                driver.implicitly_wait(5)
                time.sleep(2)
                error_text = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//ol[@class='errormsg']/li"))) #driver.find_element(By.XPATH, "//ol[@class='errormsg']/li").text.strip()
                # error_text = driver.find_element(By.XPATH, "//ol[@class='errormsg']/li")
                print('value 2')
                # if 'please try again' in error_text:
                # if error_text:
                # ==== deselect already seleted item========
                # self.wait60sec(driver)
                already_seleted_item = driver.find_element(By.XPATH, "//div[@class='kbkey button red_selected sel']").click()
                time.sleep(1)
                # ==== solve captcha again =====
                self.capcha_solved(driver)
                # ========== go to the next page by clicking on continue button again ===========
                time.sleep(2)
                driver.find_element(By.XPATH, "//input[@class='actionBtnContinue']").click()
            except:
                # print(e)
                print('no more captcha')
                break;


        #============ it is time to form fill ==========
        driver.implicitly_wait(5)
        self.non_registered_patron(driver, hkid, hkiddigit, telephone, leisurelinkn, password)


        #=========== enter booking details ===========
        driver.implicitly_wait(5)
        self.booking_details(driver, date, facility, type, time_schedule, area, venu1, location1, venu2, location2, venu3, location3, concession, name, email)

        # handle payment here
        self.payment(driver, account, pin)



        # an output will be written
        data = [hkid, facility]
        write_result(data)

    def run(self):
        self.read_csv()
        for line in self.user_list:
            # print("line")
            # if line["status"] == '1':
            #     print("line completed")
            #     continue
            hkid = line['HKID'].strip()
            hkiddigit = line['HKIDDIGIT'].strip()
            telephone = line['TELEPHONE'].strip()
            date = line['Date'].strip()

            facility = line['Facility'].strip()
            type = line['Type'].strip()
            time_schedule = line['Time'].strip()
            area = line['Area'].strip()
            venu1 = line['Venu1'].strip()
            location1 = line['Location1'].strip()
            venu2 = line['Venu2'].strip()
            location2 = line['Location2'].strip()
            venu3 = line['Venu3'].strip()
            location3 = line['Location3'].strip()
            concession = line['Concession'].strip()
            name = line['Name'].strip()
            email = line['Email'].strip()
            account = line['Account'].strip()
            pin = line['Pin'].strip()
            leisurelinkn = line['Leisurelinkn'].strip()
            password = line['Password'].strip()


            # starting here
            t = threading.Thread(target=self.booking, args=(hkid, hkiddigit, telephone,
                                                            date, facility, type, time_schedule, area, venu1, location1, venu2, location2, venu3, location3,
                                                            concession, name, email,
                                                            account, pin,
                                                            leisurelinkn, password))
            # time.sleep(3)
            t.start()
            time.sleep(2)
            # break;










# =============== run the script =====#
# if __name__ =='__main__':
#     bot = UsaDate()
#     bot.cnnsol()
