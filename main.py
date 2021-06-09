import csv
import os
import sys

import pandas as pd
from linkedin_scraper import actions
from selenium import webdriver

from custom_company import CompanyPlus


class Spider(object):
    """looking for basic information about the company on linked + information about the company leader"""

    def __init__(self, email: str, password: str, name: str, several_mode=False, headless_mode=False): # noqa
        self.email = email
        self.password = password
        self.name = name
        self.result_file = 'results.xlsx'
        self.companies = None
        self.driver = None
        self.several_mode = several_mode
        self.headless_mode = headless_mode
        self.columns = [
            'company_name', 'founded', 'website', 'linkedin_url', 'affiliated_companies', 'company_type',
            'industry', 'about_us', 'company_size', 'number_of_employees_in_linkedin', 'leader_name',
            'leader_position', 'leader_link'
        ]
        self.to_replace = [
            ['gmbh', ''], ['ag', ''], ['sa', ''], [',', ''], ['.', ''], ['(', ''], [')', ''],
            ["'", ''], ['"', ''], ['ü', 'ue'], ['ö', 'oe'], ['ä', 'ae'], ['à', 'a'], ['á', 'a'],
            ['é', 'e'], ['è', 'e'], ['ç', 'c'], ['â', 'a'], ['ñ', 'n']
        ]

    def get_or_create_results_file(self):
        """get or create results file"""
        if not os.path.exists('results.xlsx'):
            with open(self.result_file, "w", newline="", encoding='UTF-8') as f:
                writer = csv.writer(f)
                writer.writerows([self.columns])

    def write_to_file(self, company_data: dict):
        """write data to file"""
        lst = list(company_data.values())
        with open(self.result_file, "a", newline="", encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerows([lst])

    def login(self):
        """login in linkedin"""
        if headless_mode:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.headless = True
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome()
        actions.login(self.driver, self.email, self.password)

    def get_companies(self) -> list:
        """get companies form .xlsx file"""
        data_frame = pd.read_excel(self.name, engine='openpyxl')
        first_column = data_frame.columns[0]
        companies = data_frame[first_column].tolist()  # noqa
        return companies

    def get_company_url(self, company: str) -> str:
        """try to get company url in linkedin from company name"""
        company = company.lower().strip()
        for i in self.to_replace:
            company = company.replace(i[0], i[1])
        company = company.strip()
        company = company.split(sep=' ')
        company = '-'.join(company)
        company = 'https://www.linkedin.com/company/' + company
        company = company.strip()
        print(f'start url: {company}')
        return company

    def start(self):
        """start requests"""
        # get or create results file
        try:
            self.get_or_create_results_file()
        except Exception as e:
            print(f'start (get or create results file error): {e}')

        # login in linkedin
        try:
            self.login()
        except Exception as e:
            print(f'start (login in linkedin error): {e}')

        # get companies:
        try:
            if self.several_mode:
                self.companies = self.get_companies()
            else:
                self.companies = [self.name]
        except Exception as e:
            print(f'start (get companies error): {e}')

        # main part
        if self.companies:
            for company_name in self.companies:

                # get empty data template
                company_data = {column: '' for column in self.columns}

                # get company url
                try:
                    company_url = self.get_company_url(company_name)
                except Exception as e:
                    print(f'start (get company url): {e}')
                    continue

                # get company data
                try:
                    company_data = self.get_data(company_url, company_data, company_name)
                except Exception as e:
                    print(f'start (get company data): {e}')
                    continue

                # write company data to file
                try:
                    self.write_to_file(company_data)
                except Exception as e:
                    print(f'start (write company data to file): {e}')
                    continue

    def get_data(self, company_url: str, company_data: dict, company_name: str) -> dict:
        """get required data"""
        company = None

        try:
            company = CompanyPlus(
                linkedin_url=company_url,
                driver=self.driver,
                scrape=True,
                close_on_complete=False
            )
        except Exception as e:
            print(f'get_data (get company): {e}')

        if company:
            try:
                company_data['company_name'] = company.name if company.name else company_name
            except Exception as e:
                print(f'get_data (company_name): {e}')

            try:
                company_data['founded'] = company.founded if company.founded else ''
            except Exception as e:
                print(f'get_data (founded): {e}')

            try:
                company_data['website'] = company.website if company.website else ''
            except Exception as e:
                print(f'get_data (website): {e}')

            try:
                company_data['linkedin_url'] = company.linkedin_url if company.linkedin_url else ''
            except Exception as e:
                print(f'get_data (linkedin_url): {e}')

            try:
                company_data['affiliated_companies'] = company.affiliated_companies if company.affiliated_companies else '' # noqa
            except Exception as e:
                print(f'get_data (affiliated_companies): {e}')

            try:
                company_data['company_type'] = company.company_type if company.company_type else ''
            except Exception as e:
                print(f'get_data (company_type): {e}')

            try:
                company_data['industry'] = company.industry if company.industry else ''
            except Exception as e:
                print(f'get_data (industry): {e}')

            try:
                company_data['about_us'] = company.about_us if company.about_us else ''
            except Exception as e:
                print(f'get_data (about_us): {e}')

            try:
                company_data['company_size'] = company.company_size if company.company_size else ''
            except Exception as e:
                print(f'get_data (company_size): {e}')

            try:
                company_data['number_of_employees_in_linkedin'] = company.number_of_employees_in_linkedin if company.number_of_employees_in_linkedin else '' # noqa
            except Exception as e:
                print(f'get_data (number_of_employees_in_linkedin): {e}')

            try:
                company_data['leader_name'] = company.leader_name if company.leader_name else ''
            except Exception as e:
                print(f'get_data (leader_name): {e}')

            try:
                company_data['leader_position'] = company.leader_position if company.leader_position else ''
            except Exception as e:
                print(f'get_data (leader_position): {e}')

            try:
                company_data['leader_link'] = company.leader_link if company.leader_link else ''
            except Exception as e:
                print(f'get_data (leader_link): {e}')

        else:
            company_data['company_name'] = company_name

        print(f'results for {company_name}: {company_data}')
        return company_data


if __name__ == '__main__':

    # get email in command line
    email = sys.argv[1]
    # email = 'mark.calendso@gmail.com'
    # email = 'rens2588@gmail.com'

    # get password in command line
    password = sys.argv[2]
    # password = '1311711mark'
    # password = '52970130mark'

    # get file or company name in command line
    name = sys.argv[3]
    # name = 'Test-companies.xlsx'
    # name = 'Marketing monkeys'

    # get mode (one company or several). Default: several_mode = False
    several_mode = True if sys.argv[4] == 'True' else False
    # several_mode = False

    # get mode (one headless or not). Default: headless = False
    headless_mode = True if sys.argv[5] == 'True' else False
    # headless_mode = True

    # create object
    spider = Spider(email, password, name, several_mode, headless_mode)

    # start_request, get data and write to .xlsx
    spider.start()
