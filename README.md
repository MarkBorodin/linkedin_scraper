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
git clone 
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
python main.py "email "password" "file_name" 
```

email - your email from linkedin
password - your password from linkedin
file_name - file name with company names (company names must be in the first column of the file)

for example:
```
python main.py "some_email@gmail.com" "some_password" "file_name.xlsx"
```

the data will be written to the results.xlsx file


## Finish
