from django.shortcuts import render
from django.http import HttpResponse
from vahansathi.models import UserData
from django.http import HttpResponse,JsonResponse
import qrcode
from io import BytesIO
import os

from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
from dotenv import load_dotenv
load_dotenv()
Cashfree.XClientId = os.getenv("CASHFREE_CLIENT_ID")
Cashfree.XClientSecret = os.getenv("CASHFREE_CLIENT_SECRET")
Cashfree.XEnvironment = Cashfree.SANDBOX
x_api_version = "2023-08-01"

# Create your views here.
import gspread
from google.oauth2.service_account import Credentials

scopes=[
    "https://www.googleapis.com/auth/spreadsheets"
]
creds=Credentials.from_service_account_file("credentials.json", scopes=scopes)
client=gspread.authorize(creds)

sheet_id="1SJ9r42YF0dENDcdTScWigbhopxHIu9Gix7FNo82bl9w"
sheet=client.open_by_key(sheet_id)

# def home(request):
#     if request.method=='GET':
#         return render(request,'vahansathi/home.html')
#     if request.method=="POST":
#         fullname=request.POST.get("full_name")
#         address=request.POST.get('address')
#         contact1=request.POST.get('contact1')
#         contact2=request.POST.get('contact2')
#         import uuid

#         unique_id = str(uuid.uuid4())  # Example: 'f47ac10b-58cc-4372-a567-0e02b2c3d479'
#         user=UserData.objects.create(full_name=fullname,address=address,emergency_contact1=contact1,emergency_contact2=contact2,unique_id=unique_id)
        
#         load_dotenv()
#         # The link you want the QR code for
#         host=os.getenv("HOST")
#         link = f"{host}/vahansathi/user/get/{user.unique_id}"
        
#         # Generate QR code
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_H,
#             box_size=10,
#             border=4
#         )
#         qr.add_data(link)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
        
#         # Save to in-memory file
#         buffer = BytesIO()
#         img.save(buffer, format="PNG")
#         buffer.seek(0)  # Move pointer to the beginning of the file
        
#         # Return as HTTP response
#         return HttpResponse(buffer, content_type="image/png")
    
# def get_user_data(request,uid):
#     if request.method=='GET':
#         user_data=UserData.objects.get(unique_id=uid)
#         username=user_data.full_name
#         address=user_data.address
#         number1=user_data.emergency_contact1
#         number2=user_data.emergency_contact2
#         return render(request,'vahansathi/user_data.html',{"user":user_data})
def create_order_api(request):
    if request.method=="GET":
        try:
            api_response = Cashfree().PGFetchOrder(x_api_version, "order_3242X4jQ5f0S9KYxZO9mtDL1Kx2Y7u", None)
            print(api_response.data)
        except Exception as e:
            print(e)
    if request.method=="POST":

        customerDetails = CustomerDetails(customer_id="walterwNrcMi", customer_phone="9999999999")
        orderMeta = OrderMeta(return_url="https://www.cashfree.com/devstudio/thankyou")
        createOrderRequest = CreateOrderRequest(order_amount=1, order_currency="INR", customer_details=customerDetails, order_meta=orderMeta)

        response=Cashfree().PGCreateOrder(x_api_version,createOrderRequest,None,None)
        order_entity=response.data
        if order_entity.order_status=="ACTIVE":
            return JsonResponse({"payment_session_id":order_entity.payment_session_id},status=200)
        else:
            return JsonResponse({"error":"Order Creation Failed"},status=400)

def save_user_data(request):
    if request.method=='GET':
        return render(request,'vahansathi/home.html')
    if request.method=="POST":
        fullname=request.POST.get("full_name")
        address=request.POST.get('address')
        contact1=request.POST.get('contact1')
        contact2=request.POST.get('contact2')
        # import uuid

        # unique_id = str(uuid.uuid4())  # Example: 'f47ac10b-58cc-4372-a567-0e02b2c3d479'
        user=UserData.objects.create(full_name=fullname,address=address,emergency_contact1=contact1,emergency_contact2=contact2)
        users_sheet=sheet.worksheet("Users")

        id = str(user.id)   # UUID → string
        full_name = user.full_name
        address=user.address
        emergency_contact1 = user.emergency_contact1
        emergency_contact2 = user.emergency_contact2
        unique_id = str(user.unique_id)
        print(id,full_name,emergency_contact1,emergency_contact2,unique_id)

        users_sheet.append_row([id,full_name,address,emergency_contact1,emergency_contact2,unique_id])
        
        # The link you want the QR code for
        host=os.getenv("HOST")
        link = f"{host}/vahansathi/user/get/{user.unique_id}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to in-memory file
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)  # Move pointer to the beginning of the file
        
        # Return as HTTP response
        return HttpResponse(buffer, content_type="image/png")
    
def get_user_data(request,uid):
    if request.method=='GET':
        user_data=None

        users_sheet=sheet.worksheet("Users")
        all_users=users_sheet.get_all_records()

        for row in all_users:
            # print(str(row["unique_id"]))
            if str(row["unique_id"])==uid:
                user_data=row

        # username=user_data.full_name
        # address=user_data.address
        # number1=user_data.emergency_contact1
        # number2=user_data.emergency_contact2
        return render(request,'vahansathi/user_data.html',{"user":user_data})