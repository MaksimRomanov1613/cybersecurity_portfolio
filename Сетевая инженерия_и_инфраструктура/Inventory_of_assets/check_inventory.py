import openpyxl
import ipaddress
import re

def check_inventory(file_path='My_inventory.xlsx'):
    # Load workbook
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    
    headers = [cell.value for cell in sheet[1]]
    errors = []
    
    # Find column indices
    col_map = {header: idx for idx, header in enumerate(headers, 1)}
    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        asset = row[col_map.get('Asset_Name', 0) - 1] if 'Asset_Name' in col_map else 'Unknown'
        ip_field = str(row[col_map.get('IP_Address', 0) - 1]) if 'IP_Address' in col_map else ''
        os_version = str(row[col_map.get('OS_Version', 0) - 1]) if 'OS_Version' in col_map else ''
        software = str(row[col_map.get('Installed_Software', 0) - 1]) if 'Installed_Software' in col_map else ''
        
        # Check IP
        if not re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', ip_field):
            errors.append(f"Row {row[0] if row[0] else 'N/A'} ({asset}): No valid IPv4 address found")
        
        # Check OS
        if not os_version or str(os_version).strip() == '':
            errors.append(f"Row {row[0] if row[0] else 'N/A'} ({asset}): No OS version specified")
        
        # Check Software for non-network devices
        if 'Cisco' not in str(asset) and 'Catalyst' not in str(asset):
            if not software or str(software).strip() == '':
                errors.append(f"Row {row[0] if row[0] else 'N/A'} ({asset}): No software listed for endpoint/server")
    
    if errors:
        print("❌ Errors found:")
        for e in errors:
            print(e)
        return False
    else:
        print("✅ Inventory check passed! All devices have required fields.")
        return True

if __name__ == "__main__":
    check_inventory()
