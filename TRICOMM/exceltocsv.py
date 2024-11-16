import pandas as pd


excel_file = 'Basketball_dataset.xlsx'  


sheets = pd.read_excel(excel_file, sheet_name=None)  # 'sheet_name=None' loads all sheets


for sheet_name, data in sheets.items():
    csv_file = f"{sheet_name}.csv" 
    data.to_csv(csv_file, index=False)  
    print(f"Saved {sheet_name} as {csv_file}")
