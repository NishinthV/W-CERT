import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

sa_path = r"c:\Users\nishi\OneDrive\Documents\Desktop\CSF\SEM8\Capestone\service_account.json"
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(sa_path, scope)
client = gspread.authorize(creds)

try:
    sheet = client.open_by_key('1oR1GdpXTwjpT7l4MW2NhIRjQ-Tmb3vHugMH4YjsywMU').worksheet('Incidents')
    all_values = sheet.get_all_values()

    data = all_values[1:]
    print(f"Total rows: {len(data)}")

    severities = {}
    categories = {}

    headers = all_values[0]
    sev_idx = headers.index('severity') if 'severity' in headers else -1
    type_idx = headers.index('attack_type') if 'attack_type' in headers else -1

    for row in data:
        sev = row[sev_idx] if sev_idx != -1 and sev_idx < len(row) else 'UNKNOWN'
        typ = row[type_idx] if type_idx != -1 and type_idx < len(row) else 'UNKNOWN'
        
        severities[sev] = severities.get(sev, 0) + 1
        categories[typ] = categories.get(typ, 0) + 1

    print("\nSeverities:")
    print(severities)

    print("\nCategories:")
    print(categories)
except Exception as e:
    print(f"Error accessing sheet: {e}")
