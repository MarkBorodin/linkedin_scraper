# Linkedin scraper

Collects data about the company on linkedin

### Data to be collected:
'company_name', 'founded', 'website', 'linkedin_url', 'affiliated_companies', 'company_type',
'industry', 'about_us', 'company_size', 'number_of_employees_in_linkedin', 'leader_name',
'leader_position', 'leader_link'


## INSTALL_APP

### Setup

clone repository:
```
git clone https://github.com/MarkBorodin/linkedin_scraper.git
```

move to folder "linkedin_scraper":
```
cd linkedin_scraper
```

### Install the required libraries

to install the required libraries, run on command line:
```
pip install -r requirements.txt
```

## RUN_APP

### run the program:

```
python main.py "email "password" "name" several_mode headless_mode
```

email - your email from linkedin

password - your password from linkedin

name - file name with company names (company names must be in the first column of the file)

several_mode - single or serial mode. If False is single mode, you need to enter the company name. 
For example "Marketing monkeys". If True - serial mode. You need to enter the name of the .xlsx file in the torus 
are the names of the companies (they should be in the first column)

headless_mode - visual or headless mode. If true - headless mode. If False - visual mode

for example:
```
python main.py "some_email@gmail.com" "some_password" "file_name.xlsx" True False
```

the data will be written to the results.xlsx file


## Finish
