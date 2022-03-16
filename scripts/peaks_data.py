import requests
from bs4 import BeautifulSoup
import fake_useragent
import pandas as pd

def get_peak_data(url, peak_id):
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    form_data = {
        'PeakList': peak_id
    }
    response = requests.post(url, headers = header, data = form_data)
    return BeautifulSoup(response.text, 'lxml')

nan_check = lambda x: 1 if x is not None else 0

# All Peaks IDs 
peaks = pd.read_csv(r'C:\Users\vlad\Desktop\himalayan_db\peaks_data\peak_ids.csv')
peaks_data = []

for peak in peaks['peak_id']:
    try:
        print(f'Parse {peak}')
        html = get_peak_data('https://www.himalayandatabase.com/scripts/getpeakrecrdwc.php', peak)
        main_info = html.select_one('fieldset.field_set')
    except:
        print(f'Peak {peak} NOT PARSED!')
        continue

    try:
        current_peak = {
            'peak_name': main_info.find('input', id = 'Peak_Name').get('value').strip(),
            'host_contries': main_info.find('select', {'name': 'Hosts'}).text.strip(),
            'alternative_names': main_info.find('input', id = 'Alt_Name').get('value').strip(),
            'location': main_info.find('input', id = 'Location').get('value').strip(),
            'height_m': main_info.find('input', id = 'Heightm').get('value').strip(),
            'height_ft': main_info.find('input', id = 'Heightf').get('value').strip(),
            'himal': main_info.find('select', {'name': 'Himal'}).text.strip(),
            'region': main_info.find('select', {'name': 'Region'}).text.strip(),
            'restrictions': main_info.find('input', id = 'Restrict').get('value').strip(),
            'climb_status': main_info.find('select', {'name': 'Pstatus'}).text.strip(),

            'is_open': nan_check(main_info.find('input', id = 'Open').get('checked')),
            'is_unlisted': nan_check(main_info.find('input', id = 'Unlisted').get('checked')),
            'is_trekking': nan_check(main_info.find('input', id = 'Trekking').get('checked')),
            'trek_year': main_info.find('input', id = 'TrekYear').get('value').strip(),

            'first_asc_yr': main_info.find('input', id = 'Year').get('value').strip(),
            'first_asc_season': main_info.find('select', {'name': 'Season'}).text.strip(),
            'first_asc_date': main_info.find('input', id = 'Psmtdate').get('value').strip(),

            'countries': main_info.find('input', id = 'Countries').get('value').strip(),
            'first_summiters': main_info.find('textarea', id = 'Summiters').text.strip(),
            'summiters_notes': main_info.find('textarea', id = 'Psmtnote').text.strip()
        }
        peaks_data.append(current_peak)
    except:
        print(f'Peak {peak} NOT PARSED!')
        continue

# df = pd.DataFrame(peaks_data)
# df.to_csv(r'C:\Users\vlad\Desktop\himalayan_db\peaks_data\peaks_info.csv', index = False)