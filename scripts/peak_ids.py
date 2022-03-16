import pdfplumber
import pandas as pd

# All Peaks IDs and their location will be stored here
peaks_data = []

with pdfplumber.open(r'C:\Users\vlad\Desktop\himalayan_db\peaks_data\peak_list.pdf') as pdf:
    for page in range(0, len(pdf.pages)):
        current_page = pdf.pages[page]
        current_text = current_page.extract_text()
        # Use try because there are empty lists
        for line in current_text.split('\n'):
            try:
                if line.split()[0].isupper():
                    current_peak = {
                        'peak_id': line.split()[0],
                        'location': line.split()[-1]
                    }
                    peaks_data.append(current_peak)
            except:
                pass

# Saving Found Peaks
print(f'Found Peaks: {len(peaks_data)}')
res_df = pd.DataFrame(peaks_data)
res_df.to_csv(r'C:\Users\vlad\Desktop\himalayan_db\peaks_data\peak_ids_loc.csv', index=False)

