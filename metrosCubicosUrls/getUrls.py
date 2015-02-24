#!/usr/bin/python
# -*- coding: utf-8 -*-

import time, math, shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DUMMY_URL = 'http://www.metroscubicos.com/resultados/'
START_URL = 'http://www.metroscubicos.com/resultados/#sort=relevance&selected='

WAIT_FOR_ELEMENT = 20
WAIT_FOR_CHECK = 2
WAIT_FOR_PAGE_LOAD = 5

HANDLE_MAX_NUM_PAGES_PER_PASS = 1500
NUM_PASSES = 4
NUM_URLS_PER_PAGE=15

TEMPLATE_NAME = 'startUrls.py.template'

def wait_for(condition_function):

    start_time = time.time()

    while time.time() < start_time + WAIT_FOR_ELEMENT:

        if condition_function():
            return True
        else:
            time.sleep(WAIT_FOR_CHECK)

    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_text = self.browser.find_element_by_xpath('//div[@class=\'total_div\']/span[@class=\'total\']').text

    def page_has_loaded(self):
        
        pElement = WebDriverWait( self.browser, WAIT_FOR_ELEMENT ).until(EC.visibility_of_element_located((By.XPATH, '//div[@class=\'total_div\']/span[@class=\'total\']')) )
        return pElement.text != self.old_text

    def __exit__(self, *_):
        wait_for(self.page_has_loaded)

def enterEmailInfo(paginationDriver):

    paginationDriver.get(DUMMY_URL)

    mElement = WebDriverWait(paginationDriver, WAIT_FOR_ELEMENT*15).until(EC.visibility_of_element_located((By.ID, "ouibounce-modal")) )

    tEmail = paginationDriver.find_element_by_xpath("//form[@id=\'bounce-form\']/input[@name=\'email\']")
    tEmail.send_keys('dhthummala@gmail.com')

    sButton = paginationDriver.find_element_by_xpath("//form[@id=\'bounce-form\']/input[@type=\'button\']")
    sButton.click()                   

def getInfo(paginationDriver):

    global NUM_PASSES    

    numElements = int(paginationDriver.find_element_by_xpath('//span[@class=\'total_p\']').text.strip().split(" ")[0])
    numPages = math.ceil(numElements/NUM_URLS_PER_PAGE)
    NUM_PASSES = int(math.ceil(numPages/HANDLE_MAX_NUM_PAGES_PER_PASS))

    return int(numPages)


def handlePass(numPass, totalElementsCheck, paginationDriver):

    fName='part'+str(numPass)+'.py'
    shutil.copy(TEMPLATE_NAME, fName)

    numPrinted=0        

    with open(fName, "a") as myfile:

        myfile.write("[")
        
        while True:           

            lElements = paginationDriver.find_elements_by_xpath('//div[@id=\'new-prop-list\']/div/div[@class=\'property-data-container \']/div[@class=\'desc\']/a')

            if (numPrinted+NUM_URLS_PER_PAGE)==totalElementsCheck:            

                for x in lElements[:-1]:
                    myfile.write("\'"+x.get_attribute('href')+"\'"+",")

                myfile.write("\'"+lElements[-1].get_attribute('href')+"\'")
                myfile.write("]")                    

                break                    

            else:

                for x in lElements:
                    myfile.write("\'"+x.get_attribute('href')+"\'"+",")

                numPrinted+=NUM_URLS_PER_PAGE                    

            wElement = paginationDriver.find_element_by_xpath('//p[@class=\'pager\'][1]/button[last()]')        

            with wait_for_page_load(paginationDriver):
                wElement.click()

def handleLastPass(numPass, paginationDriver):

    fName='part'+str(numPass)+'.py'
    shutil.copy(TEMPLATE_NAME, fName)

    fPath=''

    with open(fName, "a") as myfile:

        myfile.write("[")        

        while True:

            wElement = paginationDriver.find_element_by_xpath('//p[@class=\'pager\'][1]/button[last()]')
            lElements = paginationDriver.find_elements_by_xpath('//div[@id=\'new-prop-list\']/div/div[@class=\'property-data-container \']/div[@class=\'desc\']/a')

            if wElement.text == 'Siguiente>>':

                for x in lElements:
                    myfile.write("\'"+x.get_attribute('href')+"\'"+",")

                with wait_for_page_load(paginationDriver):
                    wElement.click()

            else:

                for x in lElements[:-1]:
                    myfile.write("\'"+x.get_attribute('href')+"\'"+",")

                myfile.write("\'"+lElements[-1].get_attribute('href')+"\'")
                myfile.write("]")                 

                break

def parse(paginationDriver):

    enterEmailInfo(paginationDriver)

    numPages = getInfo(paginationDriver)

    paginationDriver.refresh()
    time.sleep(WAIT_FOR_PAGE_LOAD)       

    for x in range(0, NUM_PASSES):

        handlePass(x, HANDLE_MAX_NUM_PAGES_PER_PASS*NUM_URLS_PER_PAGE, paginationDriver)

        paginationDriver.get(START_URL+str((x+1)*HANDLE_MAX_NUM_PAGES_PER_PASS+1))
        paginationDriver.refresh()

        time.sleep(WAIT_FOR_PAGE_LOAD)   

    handleLastPass(NUM_PASSES, paginationDriver)        

    paginationDriver.close()    

def main():

    options = webdriver.ChromeOptions()
    options.add_extension("Block-image_v1.0.crx")

    paginationDriver = webdriver.Chrome(chrome_options = options)

    parse(paginationDriver)

if __name__ == "__main__":
    
    main()