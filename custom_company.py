import os
import time

from bs4 import BeautifulSoup
from linkedin_scraper import Company
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CompanyPlus(Company):
    words_for_company_leader = [
        'Geschäftsführer', 'Geschäftsleitung', 'Gruppenleitung', 'CEO', 'COO', 'founder', 'Gründer', 'Inhaber', 'Leitung', 'Director'  # noqa
    ]
    number_of_employees_in_linkedin = None
    leader_name = None
    leader_position = None
    leader_link = None

    def get_employees(self, wait_time=10):
        total = []
        list_css = "list-style-none"
        next_xpath = '//button[@aria-label="Next"]'
        driver = self.driver

        try:
            see_all_employees = driver.find_element_by_xpath('//a[@data-control-name="topcard_see_all_employees"]')
        except:
            pass
        driver.get(os.path.join(self.linkedin_url, "people"))

        _ = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, '//span[@dir="ltr"]')))

        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/4));")
        time.sleep(1)

        results_list = driver.find_element_by_class_name(list_css)
        results_li = results_list.find_elements_by_tag_name("li")
        for res in results_li:
            total.append(self.__parse_employee__(res))

        def is_loaded(previous_results):
            loop = 0
            driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight));")
            results_li = results_list.find_elements_by_tag_name("li")
            while len(results_li) == previous_results and loop <= 5:
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight));")
                results_li = results_list.find_elements_by_tag_name("li")
                loop += 1
            return loop <= 5

        def get_data(previous_results):
            results_li = results_list.find_elements_by_tag_name("li")
            for res in results_li[previous_results:]:
                total.append(self.__parse_employee__(res))

        results_li_len = len(results_li)
        while is_loaded(results_li_len):
            try:
                driver.find_element_by_xpath(next_xpath).click()
            except:
                pass
            _ = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME, list_css)))

            driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*2/3));")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/4));")
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight));")
            time.sleep(1)

            get_data(results_li_len)
            results_li_len = len(total)

        lis = BeautifulSoup(driver.page_source, 'lxml').find_all('li', class_='org-people-profiles-module__profile-item')  # noqa
        for li in lis:
            for word in self.words_for_company_leader:
                if word in li.text:
                    name = '-'
                    position = '-'
                    link = '-'
                    try:
                        name = li.find('div', class_='artdeco-entity-lockup__title ember-view').text.strip()
                    except Exception as e:
                        print(e)
                    try:
                        position = li.find('div', class_='artdeco-entity-lockup__subtitle ember-view').text.strip()
                    except Exception as e:
                        print(e)
                    try:
                        link = 'https://www.linkedin.com' + li.find('a').get('href')
                    except Exception as e:
                        print(e)
                    self.leader_name = name
                    self.leader_position = position
                    self.leader_link = link

        self.number_of_employees_in_linkedin = len(total) if len(total) > len(results_li) else len(results_li)
        return total

    def scrape(self, get_employees=True, close_on_complete=True):
        self.scrape_logged_in(get_employees=get_employees, close_on_complete=close_on_complete)
