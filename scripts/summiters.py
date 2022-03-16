import pandas as pd
import requests 
from bs4 import BeautifulSoup
import fake_useragent
import re

# Step 1 (Summiters parsing)
def get_members_data(url, peak_id):
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    form_data = {
        'Peak_ID': peak_id,
        'Pk_Year1': '',
        'Pk_Year2': '',
        'Season': 0,
        'Pk_Citz1': '',
        'Pk_Citz2': '',
        'Host': 0,
        'Group': 0,
        'Oxygen': 0,
        'Order': 1
    }
    response = requests.post(url, headers = header, data = form_data)
    return BeautifulSoup(response.text, 'lxml')

peaks = pd.read_csv(r'C:\Users\vlad\Desktop\himalayan_db\peaks_data\peak_ids.csv')

for peak in peaks['peak_id']:
    # All Table Rows Are Stored Here
    table_rows = []
    # All Ascents  
    peak_ascents = []

    try:
        html = get_members_data('https://www.himalayandatabase.com/scripts/peaksmtr.php', peak)
        asc_count = html.find_all('table')[3].text
        asc_count = int(re.findall(r'Ascent Count = \d*', asc_count)[0].split('=')[1].strip())
        print(f'Found {asc_count} ascents for {peak}')
    except:
        print(f'Not Found Any Ascents on {peak}')
        continue
    
    # Troubles were found during parsing. The following solution was created to overcome the table parsing 
    str_idx = 0
    end_idx = 11
    td_elements = html.find('table', id = 'Peaks').find_all('td')
    # Create table rows as lists of 10 elements (columns)
    while str_idx != len(td_elements):
        table_rows.append(td_elements[str_idx:end_idx])
        str_idx, end_idx = end_idx, end_idx + 11

    if len(table_rows) == asc_count:
        print('Rows and Ascents Match!')
    else:
        print('Rows and Ascents Don\'t Match!')

    for row in table_rows:
        ascent = {
            'peak': row[0].text,
            'name': row[1].text,
            'yr_season': row[2].text,
            'date': row[3].text,
            'time': row[4].text,
            'citizenship': row[5].text,
            'gender': row[6].text,
            'age': row[7].text,
            'is_o2_used': row[8].text,
            'died_on_descent': row[9].text,
            'host_country': row[10].text
        }
        peak_ascents.append(ascent)
    
    df = pd.DataFrame(peak_ascents)
    df.to_csv(f'C:/Users/vlad/Desktop/himalayan_db/climbers_data/{peak}_summiters.csv', index=False)
    print(f'Successfully Parsed {peak}')