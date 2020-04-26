from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import lxml.html

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.linkedin.com/')

driver.find_element_by_xpath('//a[text()="Sign in"]').click()
time.sleep(1)

username_input = driver.find_element_by_name('session_key')
username_input.send_keys('LINKEDIN_LOGIN')

password_input = driver.find_element_by_name('session_password')
password_input.send_keys('LINKEDIN_PASSWORD')
# click on the sign in button
# we're finding Sign in text button as it seems this element is seldom to be changed
driver.find_element_by_xpath('//button[text()="Sign in"]').click()

driver.get('https://www.google.com/')

search_input = driver.find_element_by_name('q')
import sys
val=sys.argv[1]
# let google find any linkedin user with keyword "python developer" and "San Francisco"
search_input.send_keys('site:linkedin.com/company/ AND "'+ val +'"')

search_input.send_keys(Keys.RETURN)

# grab all linkedin profiles from first page at Google
profiles = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
profiles = [profile.get_attribute('href') for profile in profiles]

# visit each profile in linkedin and grab detail we want to get
for profile in profiles:
    driver.get(profile)

    try:
        for company in re.findall( r'\/company\/[0-9]+', driver.page_source):
            driver.get('https://www.linkedin.com'+company)
            if val.lower() in driver.title.lower():
                print(company.replace('/company/',''))
                driver.quit()
                exit(1)
    except Exception as e:
        print(e)
        exit(0)

