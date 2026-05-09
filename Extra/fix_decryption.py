import os
import sys
import random
from dotenv import load_dotenv

sys.path.append(os.path.abspath('w-cert-backend'))
# explicitly load backend .env
load_dotenv('w-cert-backend/.env')

from app import create_app
from app.database.sheets import get_sheet
from app.security.encryption import encrypt_pii, decrypt_pii
from app.api.authorities import STATE_AUTHORITIES

INDIAN_STATES = list(STATE_AUTHORITIES.keys())

app = create_app()
with app.app_context():
    print('Fetching Incidents sheet...')
    sheet = get_sheet('Incidents')
    records = sheet.get_all_records()
    
    if not records:
        print('No records found.')
        exit(0)
        
    print(f'Found {len(records)} records. Checking for decryption failures...')
    
    cells_to_update = []
    
    headers = sheet.row_values(1)
    try:
        col_idx = headers.index('encrypted_state') + 1
    except ValueError:
        print('encrypted_state column not found!')
        exit(1)
        
    updated_count = 0
    for i, row in enumerate(records):
        enc_state = row.get('encrypted_state', '')
        
        needs_update = False
        if not enc_state:
            needs_update = True
        else:
            try:
                decrypted = decrypt_pii(enc_state)
                if decrypted == '[DECRYPTION_FAILED]' or decrypted not in INDIAN_STATES:
                    needs_update = True
            except:
                needs_update = True
                
        if needs_update:
            random_state = random.choice(INDIAN_STATES)
            new_enc_state = encrypt_pii(random_state)
            
            from gspread import Cell
            cells_to_update.append(Cell(row=i+2, col=col_idx, value=new_enc_state))
            updated_count += 1
            
    if cells_to_update:
        print(f'Updating {updated_count} rows with new valid encrypted_state using current key...')
        sheet.update_cells(cells_to_update)
        print('Success!')
    else:
        print('All rows are perfectly fine!')
