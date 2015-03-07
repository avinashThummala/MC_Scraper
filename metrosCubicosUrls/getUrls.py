#!/usr/bin/python
# -*- coding: utf-8 -*-

import time, math, shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DUMMY_URL = 'http://www.metroscubicos.com/resultados/#sort=relevance&selected=1'
START_URL = 'http://www.metroscubicos.com/resultados/#sort=relevance&selected='

WAIT_FOR_ELEMENT = 20
WAIT_FOR_CHECK = 2
WAIT_FOR_PAGE_LOAD = 5

HANDLE_MAX_NUM_PAGES_PER_PASS = 1500
NUM_PASSES = 4
NUM_URLS_PER_PAGE=15

TEMPLATE_NAME = 'startUrls.py.template'

def wait_for(condition_function, browser, isFirstTime):

    start_time = time.time()

    while time.time() < start_time + WAIT_FOR_ELEMENT:

        if condition_function():
            return True
        else:
            time.sleep(WAIT_FOR_CHECK)

    if isFirstTime:          

        browser.refresh()
        time.sleep(WAIT_FOR_PAGE_LOAD)

        wait_for(condition_function, browser, False)

    else:

        raise Exception(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )

class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_text = self.browser.find_element_by_xpath('//div[@class=\'total_div\']/span[@class=\'total\']').text

    def page_has_loaded(self):
        
        new_text = self.browser.find_element_by_xpath('//div[@class=\'total_div\']/span[@class=\'total\']').text
        return new_text != self.old_text

    def __exit__(self, *_):
        wait_for(self.page_has_loaded, self.browser, True)

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


def handlePass(numPass, totalElementsCheck, paginationDriver, numLinks):

    fName='part'+str(numPass)+'.py'
    shutil.copy(TEMPLATE_NAME, fName)

    numPrinted=0        

    with open(fName, "a") as myfile:

        myfile.write("[")
        
        while True:

            print('Gathered links: '+str(numLinks))

            wElement = WebDriverWait(paginationDriver, WAIT_FOR_ELEMENT).until(EC.element_to_be_clickable((By.XPATH, '//p[@class=\'pager\'][1]/button[last()]')) )
            lElements = paginationDriver.find_elements_by_xpath('//div[@id=\'new-prop-list\']/div/div[@class=\'property-data-container \']/div[@class=\'desc\']/a')

            numLinks+=NUM_URLS_PER_PAGE

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

            with wait_for_page_load(paginationDriver):
                wElement.click()

        return numLinks                

def handleLastPass(numPass, paginationDriver, numLinks):

    fName='part'+str(numPass)+'.py'
    shutil.copy(TEMPLATE_NAME, fName)

    fPath=''

    with open(fName, "a") as myfile:

        myfile.write("[")        

        while True:

            print('Gathered links: '+str(numLinks))

            wElement = WebDriverWait(paginationDriver, WAIT_FOR_ELEMENT).until(EC.element_to_be_clickable((By.XPATH, '//p[@class=\'pager\'][1]/button[last()]')) )
            lElements = paginationDriver.find_elements_by_xpath('//div[@id=\'new-prop-list\']/div/div[@class=\'property-data-container \']/div[@class=\'desc\']/a')

            if wElement.text == 'Siguiente>>':

            	numLinks+=NUM_URLS_PER_PAGE

                for x in lElements:
                    myfile.write("\'"+x.get_attribute('href')+"\'"+",")

                with wait_for_page_load(paginationDriver):
                    wElement.click()

            else:

            	numLinks+=len(lElements)

                for x in lElements[:-1]:
                    myfile.write("\'"+x.get_attribute('href')+"\'"+",")

                myfile.write("\'"+lElements[-1].get_attribute('href')+"\'")
                myfile.write("]")                 

                break

        return numLinks               

def parse(paginationDriver):

    enterEmailInfo(paginationDriver)

    numPages = getInfo(paginationDriver)

    paginationDriver.refresh()
    time.sleep(WAIT_FOR_PAGE_LOAD)

    numLinks=0       

    for x in range(0, NUM_PASSES-1):

        numLinks = handlePass(x, HANDLE_MAX_NUM_PAGES_PER_PASS*NUM_URLS_PER_PAGE, paginationDriver, numLinks)

        paginationDriver.get(START_URL+str((x+1)*HANDLE_MAX_NUM_PAGES_PER_PASS+1))
        paginationDriver.refresh()

        time.sleep(WAIT_FOR_PAGE_LOAD)   

    numLinks = handleLastPass(NUM_PASSES-1, paginationDriver, numLinks)

    print('Gathered '+str(numLinks)+' in total');

    paginationDriver.close()

def main():

    """
    options = webdriver.ChromeOptions()
    options.add_extension("Block-image_v1.0.crx")

    paginationDriver = webdriver.Chrome(chrome_options = options)
    """

    paginationDriver = webdriver.PhantomJS(service_args=['--load-images=no'])
    paginationDriver.maximize_window()     

    parse(paginationDriver)

if __name__ == "__main__":
    
    main()