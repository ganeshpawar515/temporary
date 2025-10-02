import gspread
from google.oauth2.service_account import Credentials

scopes=[
    "https://www.googleapis.com/auth/spreadsheets"
]
creds=Credentials.from_service_account_file("credentials.json", scopes=scopes)
client=gspread.authorize(creds)

sheet_id="1SJ9r42YF0dENDcdTScWigbhopxHIu9Gix7FNo82bl9w"
sheet=client.open_by_key(sheet_id)

users_sheet=sheet.worksheet("Users")
# users_sheet.append_row(["1","Rohit Patil","81bf78ac166444b4a75c32caca29e6b5","","","ve new delhi aprt 42 delhi-115151",""])


# import os
# import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "temp.settings")
# django.setup()
# from vahansathi.models import UserData
# import json
# users=UserData.objects.all()

# for user in users:
#     id = str(user.id)   # UUID → string
#     full_name = user.full_name
#     address=user.address
#     emergency_contact1 = user.emergency_contact1
#     emergency_contact2 = user.emergency_contact2
#     unique_id = str(user.unique_id)
#     print(id,full_name,emergency_contact1,emergency_contact2,unique_id)
#     users_sheet.append_row([id,full_name,address,emergency_contact1,emergency_contact2,unique_id])

all_users=users_sheet.get_all_records()

for row in all_users:
    # print(str(row["unique_id"]))
    if str(row["unique_id"])=="d59ef82e-a22d-47e1-a3e5-79b20cc08efb":
        print(row)

# print(all_users)

