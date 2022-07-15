import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml
import yfinance as yf
from colorama import Fore
import tqdm

# Wikipedia largest companies in the world url
wikipedia_largest_company = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

# Create a GET request to the wikipedia largest companies in the world page
wikipedia_response = requests.get(wikipedia_largest_company)

# Parse wikipedia page
wikipedia_soup = BeautifulSoup(wikipedia_response.text, 'lxml')

# Creating list with all tables
tables = wikipedia_soup.find_all('table')

#  Looking for the table with the classes 'wikitable' and 'sortable'
table = wikipedia_soup.find_all('table', class_='wikitable sortable')[0]

i = 1

# Creating an empty list that will be filled with Company Rank, Company Name, and Company Revenue
companies = []

# Looping through all rows in the table and extracting the Company Rank, Company Name, and Company Revenue

while i <= 10:
    rows = table.find_all("tr")[i]

    company_rank = rows.find_all("td")[0].text.strip()
    company_name = rows.find_all("td")[1].find_all("a")[0].text.strip()
    company_industry = rows.find_all("td")[2].text.strip()
    company_revenue = rows.find_all("td")[3].text.strip().replace(',', '')
    company_revenue_growth = rows.find_all("td")[4].text.strip().replace('%', '')
    company_employee_number = rows.find_all("td")[5].text.strip().replace(',', '')
    company_headquarters = rows.find_all("td")[6].find_all("a")[0].text.strip()

    company = {
        "Rank": int(company_rank),
        "Name": company_name,
        "Industry": company_industry,
        "Revenue": int(company_revenue),
        "Revenue growth": float(company_revenue_growth),
        "Employee number": int(company_employee_number),
        "Headquarters": company_headquarters
    }

    companies.append(company)

    i += 1

print("Please type one of the following to sort the companies by:")

print()
for key, value in company.items():
    print(key)

sorting_metric = input(
    Fore.RED + "Enter a sorting metric: " + Fore.RESET).lower()


# Creating key for Sort function
def sorter(e):
    return e[sorting_metric.capitalize()]


if sorting_metric == 'rank':
    companies.sort(key=sorter, reverse=False)

elif sorting_metric == 'revenue' or sorting_metric == 'revenue growth' or sorting_metric == 'employee number':
    companies.sort(key=sorter, reverse=True)

else:
    companies.sort(key=sorter, reverse=False)

print(pd.DataFrame(companies))