def get_sheet():
    creds_json = os.environ.get('GOOGLE_CREDS_JSON')
    creds_dict = json.loads(creds_json)
    
    # AÑADIR SCOPES EXPLÍCITOS
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1
