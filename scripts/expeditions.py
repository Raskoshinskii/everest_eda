import requests
from bs4 import BeautifulSoup
import fake_useragent
import pandas as pd
import numpy as np
import time 

# Get All Expeditions on a peak
def get_peak_expeditions(url, peak_id):
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    form_data = {
        'Peak_ID': peak_id,
        'Pk_Year1': '',
        'Pk_Year2': '',
        'Season': '0',
        'Pk_Nation': '',
        'Pk_Leader': '',
        'Pk_Sponsor': '',
        'Host': '0'
    }
    response = requests.post(url, headers = header, data = form_data)
    return BeautifulSoup(response.text, 'lxml')get

# Get All Expedition Codes on a peak
def get_expeditions_codes(peak_id):
    html = get_peak_expeditions('https://www.himalayandatabase.com/scripts/getexplist.php', peak_id)
    target_elms = html.find('select', id = 'ExpList').find_all('option')

    exp_codes = []

    for elem in target_elms:
        exp_codes.append(elem.get('value'))
    print(f'Found {len(exp_codes)} Expeditions on {peak_id}')
    return exp_codes

# Get all data about an expedition on a certain peak
def get_expedition_data(url, exp_code):
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}
    form_data = {
        'ExpList': exp_code
    }
    response = requests.post(url, headers = header, data = form_data)
    return BeautifulSoup(response.text, 'lxml')

# For CheckBoxes
nan_check = lambda x: 1 if x is not None else 0

# Parsing Data
peaks = pd.read_csv(r'C:\Users\vlad\Desktop\himalayan_db\peaks_data\peak_ids.csv')
for peak in peaks['peak_id']:
    print(f'Parse {peak}')
    try:
        exp_codes_for_peak = get_expeditions_codes(peak)
    except:
        print(f'No Expeditions Found on {peak}')
        continue

    exp_data = []
    not_parsed_exp = []

    for idx, exp_code in enumerate(exp_codes_for_peak):
        sleep_value = round(np.random.uniform(1,2), 4)
        time.sleep(sleep_value)
        try:
            html = get_expedition_data('https://www.himalayandatabase.com/scripts/getexprecrdwc.php', exp_code)
            main_info = html.select_one('fieldset.field_set')
        except:
            print(f'Expedition {idx} NOT PARSED!')
            not_parsed_exp.append(exp_code)
            continue
            
        try:
            mbrs = html.find('select', id = 'MbrList').text.strip()
        except:
            mbrs = ''
        try:
            data = {
                'nationality': main_info.find('input', id = 'Nation').get('value').strip(),
                'year': main_info.find('input', id = 'Year').get('value').strip(),
                'season': main_info.find('select', {'name': 'Season'}).text.strip(),
                'host_cntr': main_info.find('select', {'name': 'Host'}).text.strip(),
                'other_cntrs': main_info.find('textarea', id = 'Countries').text.strip(),
                'sponsor': main_info.find('input', id = 'Sponsor').get('value').strip(), # reparse
                'leaders': main_info.find('input', id = 'Leader').get('value').strip(), 

                'rte_1_name': main_info.find('input', id = 'Route1').get('value').strip(),
                'rte_2_name': main_info.find('input', id = 'Route2').get('value').strip(),
                'rte_3_name': main_info.find('input', id = 'Route3').get('value').strip(),
                'rte_4_name': main_info.find('input', id = 'Route3').get('value').strip(),
                'team_asc_1': main_info.find('input', id = 'Ascent1').get('value').strip(),
                'team_asc_2': main_info.find('input', id = 'Ascent2').get('value').strip(),
                'team_asc_3': main_info.find('input', id = 'Ascent3').get('value').strip(),
                'team_asc_4': main_info.find('input', id = 'Ascent4').get('value').strip(),

                'is_disputed': nan_check(main_info.find('input', id = 'Dsput').get('checked')),
                'is_claim': nan_check(main_info.find('input', id = 'Claim').get('checked')),
                'is_commercial_rte': nan_check(main_info.find('input', id = 'ComRte').get('checked')),
                'is_standard_rte': nan_check(main_info.find('input', id = 'StdRte').get('checked')),

                'other_smts': main_info.find('textarea', id = 'OtherSmts').text.strip(),
                'approach': main_info.find('input', id = 'Approach').get('value').strip().replace('->', ' '),
                'bc_arrived': main_info.find('input', id = 'BCdate').get('value').strip(),
                'bc_left': main_info.find('input', id = 'Termdate').get('value').strip(),
                'total_days': main_info.find('input', id = 'Totdays').get('value').strip(),
                'exp_result': main_info.find('select' , {'name': 'TermReas'}).text.strip(),

                'is_traverse': nan_check(main_info.find('input', id = 'Traverse').get('checked')),
                'is_ski_snowboard': nan_check(main_info.find('input', id = 'Ski').get('checked')),
                'is_parapente': nan_check(main_info.find('input', id = 'Parapente').get('checked')),

                'term_note': main_info.find('textarea', id = 'TermNote').text.strip(),
                'summit_day': main_info.find('input', id = 'Smtdate').get('value').strip(),
                'time': main_info.find_all('input', id = 'Smttime')[0].get('value').strip(),
                'max_elev_reached': main_info.find_all('input', id = 'Smttime')[1].get('value').strip(),
                'summit_days': main_info.find('input', id = 'Smtdays').get('value').strip(),
                
                'total_mbrs': main_info.find('input', id = 'TotMbrs').get('value').strip(),
                'mbrs_summited': main_info.find('input', id = 'SmtMbrs').get('value').strip(),
                'mbrs_deaths': main_info.find('input', id = 'DthMbrs').get('value').strip(),
                'high_camps': main_info.find('input', id = 'HiCamps').get('value').strip(),
                'hired_abc': main_info.find('input', id = 'HiredABC').get('value').strip(),
                'hired_summits': main_info.find('input', id = 'SmtHired').get('value').strip(),
                'hired_deaths': main_info.find('input', id = 'DthHired').get('value').strip(),
                'rope_fixed': main_info.find('input', id = 'FixdRope').get('value').strip(),

                'is_no_hired_abc': nan_check(main_info.find('input', id = 'NoHired').get('checked')),
                'is_o2_not_used': nan_check(main_info.find('input', id = 'O2None').get('checked')),
                'is_o2_climbing': nan_check(main_info.find('input', id = 'O2Climb').get('checked')),
                'is_o2_descent': nan_check(main_info.find('input', id = 'O2Descent').get('checked')),
                'is_o2_sleeping': nan_check(main_info.find('input', id = 'O2Sleep').get('checked')),
                'is_o2_medical': nan_check(main_info.find('input', id = 'O2Medical').get('checked')),
                'is_o2_used': nan_check(main_info.find('input', id = 'O2Used').get('checked')),
                'is_o2_unkwn': nan_check(main_info.find('input', id = 'O2Unkwn').get('checked')),
                'had_o2': nan_check(main_info.find('input', id = 'O2Taken').get('checked')), 

                'camp_sites': main_info.find('textarea', id = 'CampSites').text.strip(),
                'accidents': main_info.find('textarea', id = 'Accidents').text.strip(),
                'achievements': main_info.find('textarea', id = 'Achiev').text.strip(),
                'agency': main_info.find('input', id = 'Agency').get('value').strip(),
                'members': mbrs
                }
            exp_data.append(data)
            print(f'Expedition {idx} has been parsed')
        except:
            print('Dictionary was not created')
            continue

    # Save All Expeditions Data For a Peak
    df = pd.DataFrame(exp_data)
    df.to_csv(f'C:/Users/vlad/Desktop/himalayan_db/expeditions_data/{peak}_exp_parsed.csv', index = False)

    # Save Expeditions That Were Not Parsed (If we had them)
    if len(not_parsed_exp) > 0:
        df = pd.DataFrame({f'{peak}': not_parsed_exp})
        df.to_csv(f'C:/Users/vlad/Desktop/himalayan_db/expeditions_data/{peak}_exp_not_parsed.csv', index = False)

