from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from string import Template


import time 

XPATH_TO_GET_TO_LIST_VIEW = [
    {'text': 'CONSULTRA EL CATÁLOGO', 'xpath': '/html/body/div[4]/div/div[1]/div[2]/div/div/div'},
    {'text': 'Consultar', 'xpath': '/html/body/div[4]/div/div[2]/div/div/div/div[2]/div/form/button'}] 

XPATH_OF_SELECT_BUTTON = Template('/html/body/div[3]/div[2]/div[4]/table/tbody/tr[$BUTTON_NUMBER]/td[3]/form/button')
XPATH_OF_RETURN_BUTTON = '/html/body/div[3]/div[2]/div[3]/form/button'
XPATH_REGISTRY_NUMBER = Template('/html/body/div[3]/div[2]/div[4]/table/tbody/tr[$REGISTRY_NUMBER]/td[2]')

NUMBER_OF_ROWS_PER_PAGE = 15

DATA_ROUTES = {'REGISTRO LOCALIZADO FOLIO' :'/html/body/div[3]/div[1]/div/div/h3', 
                         'Nombre o Razón Social': '/html/body/div[3]/div[2]/div[1]/div/div[1]/div/p[2]', 
                         'Entidad/Municipio': '/html/body/div[3]/div[2]/div[1]/div/div[2]/div/p[2]',
                         'Aviso de registo N./ Fecha de aviso de registro': '/html/body/div[3]/div[2]/div[1]/div/div[3]/div/p[2]', 
                         'Ofreciendo los siguientes servicios': '/html/body/div[3]/div[2]/div[2]/div'
                         }                     
                        


def get_driver(): 
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)


def get_to_list_page(driver): 
    for xpath in XPATH_TO_GET_TO_LIST_VIEW: 
        print(f'Getting to {xpath["text"]}')
        driver.find_element(By.XPATH, xpath['xpath']).click()
        time.sleep(2)
    return driver


def click_select_to_obtain_data(driver, row_number): 
    xpath = XPATH_OF_SELECT_BUTTON.substitute(BUTTON_NUMBER=row_number)
    driver.find_element(By.XPATH, xpath).click()
    time.sleep(2)
    return driver


def get_data(driver): 
    data = {}
    data['folio_number'] = driver.find_element(By.XPATH, DATA_ROUTES['REGISTRO LOCALIZADO FOLIO']).text.split('REGISTRO LOCALIZADO FOLIO:')[1]
    data['name'] = driver.find_element(By.XPATH, DATA_ROUTES['Nombre o Razón Social']).text
    data['entidad'] = driver.find_element(By.XPATH, DATA_ROUTES['Entidad/Municipio']).text
    data['aviso_registro'] = driver.find_element(By.XPATH, DATA_ROUTES['Aviso de registo N./ Fecha de aviso de registro']).text
    data['servicios'] = driver.find_element(By.XPATH, DATA_ROUTES['Ofreciendo los siguientes servicios']).text
    driver.find_element(By.XPATH, XPATH_OF_RETURN_BUTTON).click()
    time.sleep(2)
    return data, driver
    

def get_all_clean_data_of_row(driver, row_number): 
    print(f'Getting page {row_number}')
    registry_number = driver.find_element(By.XPATH, XPATH_REGISTRY_NUMBER.substitute(REGISTRY_NUMBER=row_number)).text
    driver = click_select_to_obtain_data(driver, row_number)
    data, driver = get_data(driver)
    data['registry_number'] = registry_number
    return data, driver


if __name__ == '__main__': 
    driver = get_driver()
    driver.get('https://repse.stps.gob.mx/')
    driver = get_to_list_page(driver)
    clean_data = [] 
    for row_number in range(1, NUMBER_OF_ROWS_PER_PAGE + 1):
        try: 
            data, driver = get_all_clean_data_of_row(driver, row_number)
            clean_data.append(data)
        except NoSuchElementException:
            print('Ups... are they after us???')
            time.sleep(2)
            driver = get_driver()
            driver.get('https://repse.stps.gob.mx/')
            driver = get_to_list_page(driver)
