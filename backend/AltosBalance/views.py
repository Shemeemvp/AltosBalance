from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
from .serializers import *
from django.contrib import auth
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import json
from rest_framework.decorators import api_view, parser_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
import random
import string
from datetime import date, timedelta, datetime
from django.db.models import Q
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMessage
from io import BytesIO
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def home(request):
    return HttpResponse("Okay")


@api_view(("POST",))
def Login(request):
    try:
        user_name = request.data["username"]
        passw = request.data["password"]

        log_user = auth.authenticate(username=user_name, password=passw)

        if log_user is not None:
            auth.login(request, log_user)
            user = User.objects.get(username=user_name)

            refresh = RefreshToken.for_user(user)
            # ---super admin---
            if user.is_staff == 1:
                return Response(
                    {
                        "status": True,
                        "redirect": "admin_home",
                        "user": str(user.id),
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "role": "Admin",
                    },
                    status=status.HTTP_200_OK,
                )
            # -------distributor ------
            elif user.role == "Distributor":
                did = Distributor.objects.get(user=user)
                if did.admin_approval_status == "Accept":
                    current_day = date.today()
                    if current_day > did.end_date:
                        if not Payment_Terms_updation.objects.filter(
                            user=user, status="New"
                        ).exists():
                            return Response(
                                {
                                    "status": False,
                                    "redirect": "wrong",
                                    "user": str(user.id),
                                    "message": "Terms Expired",
                                }
                            )
                        else:
                            return Response(
                                {
                                    "status": False,
                                    "redirect": "login",
                                    "user": str(user.id),
                                    "message": "Term Updation Request is pending..",
                                }
                            )
                    else:
                        return Response(
                            {
                                "status": True,
                                "redirect": "distributor_home",
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                                "role": "Distributor",
                                "user": str(user.id),
                            },
                            status=status.HTTP_200_OK,
                        )

                else:
                    return Response(
                        {"status": False, "message": "Approval is Pending"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            # Company
            elif user.role == "Company":
                cid = Company.objects.get(user=user)
                if (
                    cid.admin_approval_status == "Accept"
                    or cid.distributor_approval_status == "Accept"
                ):
                    current_day = date.today()
                    if current_day > cid.end_date:
                        if not Payment_Terms_updation.objects.filter(
                            user=user, status="New"
                        ).exists():
                            return Response(
                                {
                                    "status": False,
                                    "user": str(user.id),
                                    "redirect": "wrong",
                                    "message": "Terms Expired",
                                }
                            )
                        else:
                            return Response(
                                {
                                    "status": False,
                                    "user": str(user.id),
                                    "redirect": "login",
                                    "message": "Term Updation Request is pending..",
                                }
                            )

                    else:
                        return Response(
                            {
                                "status": True,
                                "redirect": "company_home",
                                "role": "Company",
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                                "user": str(user.id),
                            },
                            status=status.HTTP_200_OK,
                        )
                else:
                    return Response(
                        {"status": False, "message": "Approval is Pending"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            # Staff
            elif user.role == "Staff":
                cid = Staff.objects.get(user=user)
                if cid.company_approval_status == "Accept":
                    com = cid.company

                    current_day = date.today()
                    if current_day > com.end_date:
                        return Response(
                            {
                                "status": False,
                                "user": str(user.id),
                                "redirect": "login",
                                "message": "Your account is temporarily blocked",
                            }
                        )
                    else:
                        return Response(
                            {
                                "status": True,
                                "redirect": "company_home",
                                "role": "Staff",
                                "refresh": str(refresh),
                                "access": str(refresh.access_token),
                                "user": str(user.id),
                            },
                            status=status.HTTP_200_OK,
                        )
                else:
                    return Response(
                        {"status": False, "message": "Approval is Pending"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
        else:
            return Response(
                {"status": False, "message": "Invalid username or password, try again"},
                status=status.HTTP_404_NOT_FOUND,
            )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("POST",))
def add_payment_terms(request):
    try:
        num = int(request.data["num"])
        select = request.data["value"]
        if select == "Years":
            days = int(num) * 365
            pt = PaymentTerms(
                payment_terms_number=num, payment_terms_value=select, days=days
            )
            pt.save()
            return Response({"status": True}, status=status.HTTP_201_CREATED)
        else:
            days = int(num * 30)
            pt = PaymentTerms(
                payment_terms_number=num, payment_terms_value=select, days=days
            )
            pt.save()
            return Response({"status": True}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def getPaymentTerms(request):
    try:
        terms = PaymentTerms.objects.all()
        if terms:
            serializer = PaymentTermsSerializer(terms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"status": False}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("DELETE",))
def delete_payment_terms(request, id):
    try:
        term = PaymentTerms.objects.get(id=id)
        term.delete()
        return Response({"status": True}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("POST",))
def companyReg_action(request):
    if User.objects.filter(username=request.data["username"]).exists():
        return Response(
            {
                "status": False,
                "message": "This username already exists. Sign up again",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif Company.objects.filter(email=request.data["email"]).exists():
        return Response(
            {
                "status": False,
                "message": "This email already exists. Sign up again",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        request.data["role"] = "Company"

        # AbstractUser

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(id=serializer.data["id"])
            user.set_password(request.data["password"])
            user.save()

            code_length = 8
            characters = string.ascii_letters + string.digits  # Letters and numbers

            while True:
                unique_code = "".join(
                    random.choice(characters) for _ in range(code_length)
                )
                # Check if the code already exists in the table
                if not Company.objects.filter(company_code=unique_code).exists():
                    break

            request.data["user"] = user.id
            request.data["company_code"] = unique_code
            request.data["admin_approval_status"] = "NULL"
            request.data["distributor_approval_status"] = "NULL"
            companySerializer = CompanySerializer(data=request.data)
            if companySerializer.is_valid():
                companySerializer.save()
                return Response(
                    {"status": True, "data": companySerializer.data},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"status": False, "data": companySerializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:

            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(("PUT",))
@parser_classes((MultiPartParser, FormParser))
def companyReg2_action2(request):
    try:
        login_id = request.data["Id"]
        data = User.objects.get(id=login_id)
        com = Company.objects.get(user=data.id)

        dis_code = request.data.get("distId", "")
        distr_id = None
        if dis_code:
            if not Distributor.objects.filter(distributor_code=dis_code).exists():
                return Response(
                    {
                        "status": False,
                        "message": "Sorry, distributor id does not exist",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                distr_id = Distributor.objects.get(distributor_code=dis_code)
                # request.data["Distributor_id"] = Distributor.objects.filter(distributor_code=dis_code).first().id
                # print('distrId==',request.data['Distributor_id'])
        serializer = CompanySerializer(com, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update the company with trial period dates
            com.start_date = date.today()
            com.end_date = date.today() + timedelta(days=30)
            com.distributor = distr_id
            com.save()

            # Create a trial period instance
            trial_period = TrialPeriod(
                company=com, start_date=com.start_date, end_date=com.end_date
            )
            trial_period.save()

            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except User.DoesNotExist:
        return Response(
            {"status": False, "message": "User details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Company details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("POST",))
def addModules(request):
    try:
        login_id = request.data["user"]
        data = User.objects.get(id=login_id)
        com = Company.objects.get(user=data.id)

        request.data["company"] = com.id

        serializer = ModulesListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Adding Default Units under company
            Units.objects.create(company=com, name="BOX")
            Units.objects.create(company=com, name="NUMBER")
            Units.objects.create(company=com, name="PACK")

            # Adding Default loan terms under company by TINTO MT
            Loan_Term.objects.create(company=com, duration=3, term="MONTH", days=90)
            Loan_Term.objects.create(company=com, duration="6", term="MONTH", days=180)
            Loan_Term.objects.create(company=com, duration=1, term="YEAR", days=365)

            # Adding default accounts for companies

            created_date = date.today()
            account_info = [
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Accounts Payable",
                    "account_name": "Accounts Payable",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "This is an account of all the money which you owe to others like a pending bill payment to a vendor,etc.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Accounts Receivable",
                    "account_name": "Accounts Receivable",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "The money that customers owe you becomes the accounts receivable. A good example of this is a payment expected from an invoice sent to your customer.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "Advance Tax",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Any tax which is paid in advance is recorded into the advance tax account. This advance tax payment could be a quarterly, half yearly or yearly payment",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Advertising and Marketing",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Your expenses on promotional, marketing and advertising activities like banners, web-adds, trade shows, etc. are recorded in advertising and marketing account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Automobile Expense",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Transportation related expenses like fuel charges and maintenance charges for automobiles, are included to the automobile expense account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Bad Debt",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Any amount which is lost and is unrecoverable is recorded into the bad debt account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Bank Fees and Charges",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": " Any bank fees levied is recorded into the bank fees and charges account. A bank account maintenance fee, transaction charges, a late payment fee are some examples.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Consultant Expense",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Charges for availing the services of a consultant is recorded as a consultant expenses. The fees paid to a soft skills consultant to impart personality development training for your employees is a good example.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Cost Of Goods Sold",
                    "account_name": "Cost of Goods Sold",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account which tracks the value of the goods sold.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Credit Card Charges",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": " Service fees for transactions , balance transfer fees, annual credit fees and other charges levied on a credit card are recorded into the credit card account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Depreciation Expense",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Any depreciation in value of your assets can be captured as a depreciation expense.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Income",
                    "account_name": "Discount",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Any reduction on your selling price as a discount can be recorded into the discount account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Equity",
                    "account_name": "Drawings",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "The money withdrawn from a business by its owner can be tracked with this account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "Employee Advance",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Money paid out to an employee in advance can be tracked here till it's repaid or shown to be spent for company purposes",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Liability",
                    "account_name": "Employee Reimbursements",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "This account can be used to track the reimbursements that are due to be paid out to employees.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Expense",
                    "account_name": "Exchange Gain or Loss",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Changing the conversion rate can result in a gain or a loss. You can record this into the exchange gain or loss account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Fixed Asset",
                    "account_name": "Furniture and Equipment",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Purchases of furniture and equipment for your office that can be used for a long period of time usually exceeding one year can be tracked with this account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Income",
                    "account_name": "General Income",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "A general category of account where you can record any income which cannot be recorded into any other category",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Income",
                    "account_name": "Interest Income",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "A percentage of your balances and deposits are given as interest to you by your banks and financial institutions. This interest is recorded into the interest income account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Stock",
                    "account_name": "Inventory Asset",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An account which tracks the value of goods in your inventory.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "IT and Internet Expenses",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Money spent on your IT infrastructure and usage like internet connection, purchasing computer equipment etc is recorded as an IT and Computer Expense",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Janitorial Expense",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "All your janitorial and cleaning expenses are recorded into the janitorial expenses account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Income",
                    "account_name": "Late Fee Income",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Any late fee income is recorded into the late fee income account. The late fee is levied when the payment for an invoice is not received by the due date",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Lodging",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Any expense related to putting up at motels etc while on business travel can be entered here.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Meals and Entertainment",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Expenses on food and entertainment are recorded into this account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Office Supplies",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "All expenses on purchasing office supplies like stationery are recorded into the office supplies account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Liability",
                    "account_name": "Opening Balance Adjustments",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "This account will hold the difference in the debits and credits entered during the opening balance.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Equity",
                    "account_name": "Opening Balance Offset",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "This is an account where you can record the balance from your previous years earning or the amount set aside for some activities. It is like a buffer account for your funds.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Income",
                    "account_name": "Other Charges",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Miscellaneous charges like adjustments made to the invoice can be recorded in this account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Other Expenses",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": " Any minor expense on activities unrelated to primary business operations is recorded under the other expense account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Equity",
                    "account_name": "Owner's Equity",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "The owners rights to the assets of a company can be quantified in the owner's equity account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Cash",
                    "account_name": "Petty Cash",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "It is a small amount of cash that is used to pay your minor or casual expenses rather than writing a check.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Postage",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Your expenses on ground mails, shipping and air mails can be recorded under the postage account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "Prepaid Expenses",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An asset account that reports amounts paid in advance while purchasing goods or services from a vendor.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Printing and Stationery",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": " Expenses incurred by the organization towards printing and stationery.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Rent Expense",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "The rent paid for your office or any space related to your business can be recorded as a rental expense.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Repairs and Maintenance",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "The costs involved in maintenance and repair of assets is recorded under this account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Equity",
                    "account_name": "Retained Earnings",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "The earnings of your company which are not distributed among the share holders is accounted as retained earnings.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Salaries and Employee Wages",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Salaries for your employees and the wages paid to workers are recorded under the salaries and wages account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Income",
                    "account_name": "Sales",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": " The income from the sales in your business is recorded under the sales account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Income",
                    "account_name": "Shipping Charge",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Shipping charges made to the invoice will be recorded in this account.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Liability",
                    "account_name": "Tag Adjustments",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": " This adjustment account tracks the transfers between different reporting tags.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Liability",
                    "account_name": "Tax Payable",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "The amount of money which you owe to your tax authority is recorded under the tax payable account. This amount is a sum of your outstanding in taxes and the tax charged on sales.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Telephone Expense",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "The expenses on your telephone, mobile and fax usage are accounted as telephone expenses.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Travel Expense",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": " Expenses on business travels like hotel bookings, flight charges, etc. are recorded as travel expenses.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Uncategorized",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "This account can be used to temporarily track expenses that are yet to be identified and classified into a particular category.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Cash",
                    "account_name": "Undeposited Funds",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "Record funds received by your company yet to be deposited in a bank as undeposited funds and group them as a current asset in your balance sheet.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Liability",
                    "account_name": "Unearned Revenue",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "A liability account that reports amounts received in advance of providing goods or services. When the goods or services are provided, this account balance is decreased and a revenue account is increased.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Equity",
                    "account_name": "Capital Stock",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": " An equity account that tracks the capital introduced when a business is operated through a company or corporation.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Long Term Liability",
                    "account_name": "Construction Loans",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account that tracks the amount you repay for construction loans.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Contract Assets",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An asset account to track the amount that you receive from your customers while you're yet to complete rendering the services.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Depreciation And Amortisation",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account that is used to track the depreciation of tangible assets and intangible assets, which is amortization.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Equity",
                    "account_name": "Distributions",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An equity account that tracks the payment of stock, cash or physical products to its shareholders.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Equity",
                    "account_name": "Dividends Paid",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An equity account to track the dividends paid when a corporation declares dividend on its common stock.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Liability",
                    "account_name": "GST Payable",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Liability",
                    "account_name": "Output CGST",
                    "credit_card_no": "",
                    "sub_account": True,
                    "parent_account": "GST Payable",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Liability",
                    "account_name": "Output IGST",
                    "credit_card_no": "",
                    "sub_account": True,
                    "parent_account": "GST Payable",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Liability",
                    "account_name": "Output SGST",
                    "credit_card_no": "",
                    "sub_account": True,
                    "parent_account": "GST Payable",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "GST TCS Receivable",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "GST TDS Receivable",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "Input Tax Credits",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "Input CGST",
                    "credit_card_no": "",
                    "sub_account": True,
                    "parent_account": "Input Tax Credits",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "Input IGST",
                    "credit_card_no": "",
                    "sub_account": True,
                    "parent_account": "Input Tax Credits",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "Input SGST",
                    "credit_card_no": "",
                    "sub_account": True,
                    "parent_account": "Input Tax Credits",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Equity",
                    "account_name": "Investments",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An equity account used to track the amount that you invest.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Cost Of Goods Sold",
                    "account_name": "Job Costing",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account to track the costs that you incur in performing a job or a task.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Cost Of Goods Sold",
                    "account_name": "Labor",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account that tracks the amount that you pay as labor.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Cost Of Goods Sold",
                    "account_name": "Materials",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account that tracks the amount you use in purchasing materials.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Merchandise",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account to track the amount spent on purchasing merchandise.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Long Term Liability",
                    "account_name": "Mortgages",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account that tracks the amounts you pay for the mortgage loan.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Raw Materials And Consumables",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account to track the amount spent on purchasing raw materials and consumables.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "Reverse Charge Tax Input but not due",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "The amount of tax payable for your reverse charge purchases can be tracked here.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "Sales to Customers (Cash)",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Cost Of Goods Sold",
                    "account_name": "Subcontractor",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": " An expense account to track the amount that you pay subcontractors who provide service to you.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Liability",
                    "account_name": "TDS Payable",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Other Current Asset",
                    "account_name": "TDS Receivable",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Expense",
                    "account_name": "Transportation Expense",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "An expense account to track the amount spent on transporting goods or providing services.",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Bank",
                    "account_name": "Bank Account",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Cash",
                    "account_name": "Cash Account",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Credit Card",
                    "account_name": "Credit Card Account",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
                {
                    "company_id": com,
                    "Login_Id": data,
                    "account_type": "Payment Clearing Account",
                    "account_name": "Payment Clearing Account",
                    "credit_card_no": "",
                    "sub_account": "",
                    "parent_account": "",
                    "bank_account_no": None,
                    "account_code": "",
                    "description": "",
                    "balance": 0.0,
                    "balance_type": "",
                    "date": created_date,
                    "create_status": "default",
                    "status": "active",
                },
            ]

            for account in account_info:
                if not Chart_Of_Account.objects.filter(
                    company=com, account_name=account["account_name"]
                ).exists():
                    new_account = Chart_Of_Account(
                        company=account["company_id"],
                        user=account["Login_Id"],
                        account_name=account["account_name"],
                        account_type=account["account_type"],
                        credit_card_no=account["credit_card_no"],
                        sub_account=account["sub_account"],
                        parent_account=account["parent_account"],
                        bank_account_no=account["bank_account_no"],
                        account_code=account["account_code"],
                        description=account["description"],
                        balance=account["balance"],
                        balance_type=account["balance_type"],
                        create_status=account["create_status"],
                        status=account["status"],
                        date=account["date"],
                    )
                    new_account.save()

            # Adding Default Customer payment under company
            Company_Payment_Terms.objects.create(
                company=com, term_name="Due on Receipt", days=0
            )
            Company_Payment_Terms.objects.create(
                company=com, term_name="NET 30", days=30
            )
            Company_Payment_Terms.objects.create(
                company=com, term_name="NET 60", days=60
            )

            # sumayya-------- Adding default repeat every values for company

            CompanyRepeatEvery.objects.create(
                company=com,
                repeat_every="3 Month",
                repeat_type="Month",
                duration=3,
                days=90,
            )
            CompanyRepeatEvery.objects.create(
                company=com,
                repeat_every="6 Month",
                repeat_type="Month",
                duration=6,
                days=180,
            )
            CompanyRepeatEvery.objects.create(
                company=com,
                repeat_every="1 Year",
                repeat_type="Year",
                duration=1,
                days=360,
            )

            # Creating default transport entries with company information---aiswarya
            Eway_Transportation.objects.create(Name="Bus", Type="Road", company=com)
            Eway_Transportation.objects.create(Name="Train", Type="Rail", company=com)
            Eway_Transportation.objects.create(Name="Car", Type="Road", company=com)

            Stock_Reason.objects.create(company=com, user=data, reason="Stock on fire")
            Stock_Reason.objects.create(
                company=com, user=data, reason="High demand of goods"
            )
            Stock_Reason.objects.create(
                company=com, user=data, reason="Stock written off"
            )
            Stock_Reason.objects.create(
                company=com, user=data, reason="Inventory Revaluation"
            )

            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except User.DoesNotExist:
        return Response(
            {"status": False, "message": "User details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Company details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("POST",))
def staffReg_action(request):
    if not Company.objects.filter(company_code=request.data["company_code"]).exists():
        return Response(
            {
                "status": False,
                "message": "This company code does not exists. try again.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif User.objects.filter(username=request.data["username"]).exists():
        return Response(
            {
                "status": False,
                "message": "This username already exists. Sign up again",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif Staff.objects.filter(email=request.data["email"]).exists():
        return Response(
            {
                "status": False,
                "message": "This email already exists. Sign up again",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        com = Company.objects.get(company_code=request.data["company_code"])

        request.data["role"] = "Staff"

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(id=serializer.data["id"])

            user.set_password(request.data["password"])
            user.save()

            request.data["user"] = user.id
            request.data["company_approval_status"] = "Null"
            request.data["company"] = com.id
            staffSerializer = StaffSerializer(data=request.data)
            if staffSerializer.is_valid():
                staffSerializer.save()
                return Response(
                    {"status": True, "data": staffSerializer.data},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"status": False, "data": staffSerializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["GET"])
def getStaffData(request, id):
    try:
        login_id = id
        data = User.objects.get(id=login_id)
        if data:
            stf = Staff.objects.get(user=data)
            dict = {
                "name": data.first_name + " " + data.last_name,
                "uName": data.username,
                "email": stf.email,
            }
            return JsonResponse(
                {"status": True, "data": dict}, status=status.HTTP_200_OK
            )
        else:
            return JsonResponse({"status": False}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("PUT",))
@parser_classes((MultiPartParser, FormParser))
def staffReg2_Action(request):
    try:
        login_id = request.data["Id"]
        data = User.objects.get(id=login_id)
        sdata = Staff.objects.get(user=data)

        serializer = StaffSerializer(sdata, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except User.DoesNotExist:
        return Response(
            {"status": False, "message": "User details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Staff.DoesNotExist:
        return Response(
            {"status": False, "message": "Staff details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("POST",))
def distributorReg_Action(request):
    if request.method == "POST":
        if User.objects.filter(username=request.data["username"]).exists():
            return Response(
                {
                    "status": False,
                    "message": "This username already exists. Sign up again",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif Company.objects.filter(email=request.data["email"]).exists():
            return Response(
                {
                    "status": False,
                    "message": "This email already exists. Sign up again",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            request.data["role"] = "Distributor"

            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(id=serializer.data["id"])
                user.set_password(request.data["password"])
                user.save()

                code_length = 8
                characters = string.ascii_letters + string.digits  # Letters and numbers

                while True:
                    unique_code = "".join(
                        random.choice(characters) for _ in range(code_length)
                    )
                    # Check if the code already exists in the table
                    if not Distributor.objects.filter(
                        distributor_code=unique_code
                    ).exists():
                        break

                request.data["user"] = user.id
                request.data["distributor_code"] = unique_code
                request.data["admin_approval_status"] = "NULL"

                distributorSerializer = DistributorSerializer(data=request.data)
                if distributorSerializer.is_valid():
                    distributorSerializer.save()
                    return Response(
                        {"status": True, "data": distributorSerializer.data},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(
                        {"status": False, "data": distributorSerializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"status": False, "data": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )


@api_view(["GET"])
def getDistributorData(request, id):
    try:
        login_id = id
        data = User.objects.get(id=login_id)
        if data:
            distr = Distributor.objects.get(user=data)
            dict = {
                "fName": data.first_name,
                "lName": data.last_name,
                "uName": data.username,
                "email": distr.email,
            }
            return JsonResponse(
                {"status": True, "data": dict}, status=status.HTTP_200_OK
            )
        else:
            return JsonResponse({"status": False}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("PUT",))
@parser_classes((MultiPartParser, FormParser))
def distributorReg2_Action2(request):
    try:
        login_id = request.data["Id"]
        data = User.objects.get(id=login_id)
        ddata = Distributor.objects.get(user=data)

        serializer = DistributorSerializer(ddata, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update the company with trial period dates
            payment_term = request.data["payment_term"]
            terms = PaymentTerms.objects.get(id=payment_term)

            start_date = date.today()
            days = int(terms.days)
            end = date.today() + timedelta(days=days)

            ddata.start_date = start_date
            ddata.end_date = end
            ddata.save()

            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except User.DoesNotExist:
        return Response(
            {"status": False, "message": "User details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Distributor.DoesNotExist:
        return Response(
            {"status": False, "message": "Distributor details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getClients(request):
    try:
        data = Company.objects.filter(admin_approval_status="Accept")
        # serializer = DistributorDetailsSerializer(data, many=True)
        requests = []
        for i in data:
            req = {
                "id": i.id,
                "name": i.user.first_name + " " + i.user.last_name,
                "email": i.email,
                "contact": i.contact,
                "term": (
                    str(i.payment_term.payment_terms_number)
                    + " "
                    + i.payment_term.payment_terms_value
                    if i.payment_term
                    else "Trial Period"
                ),
                "endDate": i.end_date,
            }
            requests.append(req)

        return Response({"status": True, "data": requests})
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getClientsRequests(request):
    try:
        data = Company.objects.filter(
            registration_type="self", admin_approval_status="NULL"
        )
        requests = []
        for i in data:
            req = {
                "id": i.id,
                "name": i.user.first_name + " " + i.user.last_name,
                "email": i.email,
                "contact": i.contact,
                "term": (
                    str(i.payment_term.payment_terms_number)
                    + " "
                    + i.payment_term.payment_terms_value
                    if i.payment_term
                    else "Trial Period"
                ),
                "endDate": i.end_date,
            }
            requests.append(req)

        return Response({"status": True, "data": requests})
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("PUT",))
def client_Req_Accept(request, id):
    try:
        data = Company.objects.get(id=id)
        data.admin_approval_status = "Accept"
        data.save()
        return Response({"status": True}, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Client details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("DELETE",))
def client_Req_Reject(request, id):
    try:
        data = Company.objects.get(id=id)
        data.user.delete()
        data.delete()
        return Response({"status": True}, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Client details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getDistributorsRequests(request):
    try:
        data = Distributor.objects.filter(admin_approval_status="NULL")
        requests = []
        for i in data:
            req = {
                "id": i.id,
                "name": i.user.first_name + " " + i.user.last_name,
                "email": i.email,
                "contact": i.contact,
                "term": (
                    str(i.payment_term.payment_terms_number)
                    + " "
                    + i.payment_term.payment_terms_value
                    if i.payment_term
                    else ""
                ),
                "endDate": i.end_date,
            }
            requests.append(req)
        return Response({"status": True, "data": requests})
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getDistributors(request):
    try:
        data = Distributor.objects.filter(admin_approval_status="Accept")
        requests = []
        for i in data:
            req = {
                "id": i.id,
                "name": i.user.first_name + " " + i.user.last_name,
                "email": i.email,
                "contact": i.contact,
                "term": (
                    str(i.payment_term.payment_terms_number)
                    + " "
                    + i.payment_term.payment_terms_value
                    if i.payment_term
                    else ""
                ),
                "endDate": i.end_date,
            }
            requests.append(req)

        return Response({"status": True, "data": requests})
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("PUT",))
def distributorReq_Accept(request, id):
    try:
        data = Distributor.objects.get(id=id)
        data.admin_approval_status = "Accept"
        data.save()
        return Response({"status": True}, status=status.HTTP_200_OK)
    except Distributor.DoesNotExist:
        return Response(
            {"status": False, "message": "Distributor details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("DELETE",))
def distributorReq_Reject(request, id):
    try:
        data = Distributor.objects.get(id=id)
        data.user.delete()
        data.delete()
        return Response({"status": True}, status=status.HTTP_200_OK)
    except Distributor.DoesNotExist:
        return Response(
            {"status": False, "message": "Distributor details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getDistributorsOverviewData(request, id):
    try:
        data = Distributor.objects.get(id=id)
        # serializer = DistributorDetailsSerializer(data, many=True)
        req = {
            "id": data.id,
            "name": data.user.first_name + " " + data.user.last_name,
            "email": data.email,
            "code": data.distributor_code,
            "contact": data.contact,
            "username": data.user.username,
            "image": data.image.url if data.image else None,
            "endDate": data.end_date,
            "term": (
                str(data.payment_term.payment_terms_number)
                + " "
                + data.payment_term.payment_terms_value
                if data.payment_term
                else ""
            ),
        }
        return Response({"status": True, "data": req}, status=status.HTTP_200_OK)
    except Distributor.DoesNotExist:
        return Response(
            {"status": False, "message": "Distributor details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getClientsOverviewData(request, id):
    try:
        data = Company.objects.get(id=id)
        modules = Modules_List.objects.get(company=data, status="New")
        serializer = ModulesListSerializer(modules)
        req = {
            "id": data.id,
            "name": data.user.first_name + " " + data.user.last_name,
            "email": data.email,
            "code": data.company_code,
            "contact": data.contact,
            "username": data.user.username,
            "image": data.image.url if data.image else "",
            "endDate": data.end_date,
            "term": (
                str(data.payment_term.payment_terms_number)
                + " "
                + data.payment_term.payment_terms_value
                if data.payment_term
                else "Trial Period"
            ),
        }
        return Response(
            {"status": True, "data": req, "modules": serializer.data},
            status=status.HTTP_200_OK,
        )
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Client details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(("GET",))
def fetchAdminNotifications(request):
    try:
        noti = ANotification.objects.filter(status="New").order_by(
            "-id", "-noti_date"
        )
        serializer = ANotificationsSerializer(noti, many=True)
        return Response(
            {"status": True, "notifications": serializer.data},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

@api_view(("GET",))
def getAdminNotificationOverview(request, id):
    try:
        data = ANotification.objects.get(id=id)
        if data.user.role == "Company":
            com = Company.objects.get(user=data.user)
            modules = Modules_List.objects.get(company=com, status="New")
            serializer = ModulesListSerializer(modules)
            req = {
                "id": data.id,
                "user": "Company",
                "name": com.company_name,
                "email": com.email,
                "code": com.company_code,
                "contact": com.contact,
                "username": com.user.username,
                "image": com.image.url if com.image else "",
                "endDate": com.end_date,
                "termUpdation": True if data.payment_terms_updation else False,
                "moduleUpdation": True if data.module_list else False,
                "term": (
                    str(com.payment_term.payment_terms_number)
                    + " "
                    + com.payment_term.payment_terms_value
                    if com.payment_term
                    else "Trial Period"
                ),
                "newTerm": (
                    str(data.payment_terms_updation.payment_term.payment_terms_number)
                    + " "
                    + data.payment_terms_updation.payment_term.payment_terms_value
                    if data.payment_terms_updation
                    else ""
                ),
            }
            if data.module_list:
                modules_pending = Modules_List.objects.filter(
                    user=data.user, status="pending"
                )
                current_modules = Modules_List.objects.filter(
                    user=data.user, status="New"
                )

                print('modules_pending',modules_pending)
                print('current_modules',current_modules)

                # Extract the field names related to modules
                module_fields = [
                    field.name
                    for field in Modules_List._meta.fields
                    if field.name
                    not in [
                        "id",
                        "company",
                        "status",
                        "update_action",
                        "company",
                        "user",
                    ]
                ]

                # Get the previous and new values for the selected modules
                previous_values = current_modules.values(*module_fields).first()
                new_values = modules_pending.values(*module_fields).first()

                # Iterate through the dictionary and replace None with 0
                for key, value in previous_values.items():
                    if value is None:
                        previous_values[key] = 0

                # Iterate through the dictionary and replace None with 0
                for key, value in new_values.items():
                    if value is None:
                        new_values[key] = 0

                # Identify added and deducted modules
                added_modules = {}
                deducted_modules = {}

                for field in module_fields:
                    if new_values[field] > previous_values[field]:
                        added_modules[field] = (
                            new_values[field] - previous_values[field]
                        )
                    elif new_values[field] < previous_values[field]:
                        deducted_modules[field] = (
                            previous_values[field] - new_values[field]
                        )

                return Response(
                    {
                        "status": True,
                        "data": req,
                        "modules": serializer.data,
                        "added_modules": added_modules,
                        "deducted_modules": deducted_modules,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": True, "data": req}, status=status.HTTP_200_OK
                )
        else:
            com = Distributor.objects.get(user=data.user)
            print('com-',com)
            req = {
                "id": data.id,
                "user": "Distributor",
                "name": com.user.first_name + " " + com.user.last_name,
                "email": com.email,
                "code": com.distributor_code,
                "contact": com.contact,
                "username": com.user.username,
                "image": com.image.url if com.image else "",
                "endDate": com.end_date,
                "termUpdation": True if data.payment_terms_updation else False,
                "moduleUpdation": False,
                "term": (
                    str(com.payment_term.payment_terms_number)
                    + " "
                    + com.payment_term.payment_terms_value
                    if com.payment_term
                    else "Trial Period"
                ),
                "newTerm": (
                    str(data.payment_terms_updation.payment_term.payment_terms_number)
                    + " "
                    + data.payment_terms_updation.payment_term.payment_terms_value
                    if data.payment_terms_updation
                    else ""
                ),
            }
            return Response({"status": True, "data": req}, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Company not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Distributor.DoesNotExist:
        return Response(
            {"status": False, "message": "Distributor not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("POST",))
def module_Updation_Accept(request):
    try:
        id = request.data["id"]
        data = ANotification.objects.get(id=id)
        allmodules = Modules_List.objects.get(user=data.user, status="New")
        allmodules.delete()

        allmodules1 = Modules_List.objects.get(
            user=data.user, status="pending"
        )
        allmodules1.status = "New"
        allmodules1.save()

        data.status = "old"
        data.save()

        # notification
        CNotification.objects.create(
            user=allmodules1.user,
            company=allmodules1.company,
            title="Modules Updated..!",
            description="Your module update request is approved",
        )

        return Response({"status": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("DELETE",))
def module_Updation_Reject(request):
    try:
        id = request.data["id"]
        data = ANotification.objects.get(id=id)
        allmodules = Modules_List.objects.get(
            user=data.user, status="pending"
        )
        allmodules.delete()

        data.delete()

        return Response({"status": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def distributorClientRequest(request, id):
    try:
        data = Distributor.objects.get(user__id=id)
        lst = Company.objects.filter(
            registration_type="distributor",
            distributor_approval_status="NULL",
            distributor=data,
        )
        requests = []
        for i in lst:
            req = {
                "id": i.id,
                "name": i.user.first_name + " " + i.user.last_name,
                "email": i.email,
                "contact": i.contact,
                "term": (
                    str(i.payment_term.payment_terms_number)
                    + " "
                    + i.payment_term.payment_terms_value
                    if i.payment_term
                    else "Trial Period"
                ),
                "endDate": i.end_date,
            }
            requests.append(req)

        return Response({"status": True, "data": requests})
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def distributorClients(request, id):
    try:
        data = Distributor.objects.get(user__id=id)
        lst = Company.objects.filter(
            registration_type="distributor",
            distributor_approval_status="Accept",
            distributor=data,
        )
        requests = []
        for i in lst:
            req = {
                "id": i.id,
                "name": i.user.first_name + " " + i.user.last_name,
                "email": i.email,
                "contact": i.contact,
                "term": (
                    str(i.payment_term.payment_terms_number)
                    + " "
                    + i.payment_term.payment_terms_value
                    if i.payment_term
                    else "Trial Period"
                ),
                "endDate": i.end_date,
            }
            requests.append(req)

        return Response({"status": True, "data": requests})
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("PUT",))
def distributorClient_Req_Accept(request, id):
    try:
        data = Company.objects.get(id=id)
        data.distributor_approval_status = "Accept"
        data.save()
        return Response({"status": True}, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Client details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("DELETE",))
def distributorClient_Req_Reject(request, id):
    try:
        data = Company.objects.get(id=id)
        data.user.delete()
        data.delete()
        return Response({"status": True}, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Client details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def checkDistributorPaymentTerms(request, id):
    try:
        s_id = id
        data = User.objects.get(id=s_id)
        com = Distributor.objects.get(user=data)
        payment_request = Payment_Terms_updation.objects.filter(
            user=data, status="New"
        ).exists()

        title2 = ["Modules Updated..!", "New Plan Activated..!", "Change Payment Terms"]
        today_date = date.today()
        notification = DNotification.objects.filter(
            status="New", distributor=com, title__in=title2, noti_date__lt=today_date
        )
        notification.update(status="old")

        diff = (com.end_date - today_date).days

        # payment term and trial period alert notifications for notification page
        dis_name = com.user.first_name + "  " + com.user.last_name
        if (
            not DNotification.objects.filter(
                user=data,
                distributor=com,
                title="Payment Terms Alert",
                status="New",
            ).exists()
            and diff <= 20
        ):
            n = DNotification(
                user=data,
                distributor=com,
                title="Payment Terms Alert",
                description="Your Payment Terms End Soon",
            )
            n.save()
            d = ANotification(
                user=data,
                title="Payment Terms Alert",
                description=f"Current  payment terms of {dis_name} is expiring",
            )
            d.save()
        noti = DNotification.objects.filter(status="New", distributor=com).order_by(
            "-id", "-noti_date"
        )
        n = len(noti)

        # Calculate the date 20 days before the end date for payment term renew and 10 days before for trial period renew
        reminder_date = com.end_date - timedelta(days=20)
        current_date = date.today()
        alert_message = current_date >= reminder_date

        # Calculate the number of days between the reminder date and end date
        days_left = (com.end_date - current_date).days
        return Response(
            {
                "status": True,
                "alert_message": alert_message,
                "endDate": com.end_date,
                "days_left": days_left,
                "payment_request": payment_request,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getDistributorProfileData(request, id):
    try:
        data = User.objects.get(id=id)
        usrData = Distributor.objects.get(user=data)
        payment_request = Payment_Terms_updation.objects.filter(
            user=data, status="New"
        ).exists()
        personal = {
            "userImage": usrData.image.url if usrData.image else False,
            "distributorCode": usrData.distributor_code,
            "firstName": data.first_name,
            "lastName": data.last_name,
            "email": usrData.email,
            "username": data.username,
            "userContact": usrData.contact,
            "joinDate": usrData.start_date,
            "paymentTerm": (
                str(usrData.payment_term.payment_terms_number)
                + " "
                + usrData.payment_term.payment_terms_value
                if usrData.payment_term
                else ""
            ),
            "endDate": usrData.end_date,
        }

        return Response(
            {
                "status": True,
                "personalData": personal,
                "payment_request": payment_request,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("POST",))
def changeDistributorPaymentTerms(request):
    try:
        s_id = request.data["ID"]
        data = User.objects.get(id=s_id)
        com = Distributor.objects.get(user=data)
        pt = request.data["payment_term"]

        pay = PaymentTerms.objects.get(id=pt)

        data1 = Payment_Terms_updation(user=data, payment_term=pay)
        data1.save()

        noti = ANotification(
            user=data,
            payment_terms_updation=data1,
            title="Change Payment Terms",
            description=com.user.first_name
            + " "
            + com.user.last_name
            + " wants to subscribe a new plan",
        )
        noti.save()

        return Response(
            {"status": True, "message": "Request Sent.!"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("PUT",))
@parser_classes((MultiPartParser, FormParser))
def editDistributorProfile(request):
    try:
        login_id = request.data["Id"]
        data = User.objects.get(id=login_id)
        distr = Distributor.objects.get(user=data)

        logSerializer = UserSerializer(data, data=request.data)
        serializer = DistributorSerializer(distr, data=request.data, partial=True)

        fName = request.data["first_name"]
        lName = request.data["last_name"]
        email = request.data["email"]

        if fName != "":
            data.first_name = fName
        if lName != "":
            data.last_name = lName
        if email != "":
            data.email = email

        data.save()

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except User.DoesNotExist:
        return Response(
            {"status": False, "message": "User details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Distributor.DoesNotExist:
        return Response(
            {"status": False, "message": "Distributor details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(("GET",))
def fetchDistNotifications(request, id):
    try:
        s_id = id
        data = User.objects.get(id=s_id)
        com = Distributor.objects.get(user=data)
        noti = DNotification.objects.filter(
            status="New", distributor=com
        ).order_by("-id", "-noti_date")
        serializer = DNotificationsSerializer(noti, many=True)
        return Response(
            {"status": True, "notifications": serializer.data},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(("GET",))
def getDistributorNotificationOverview(request, id):
    try:
        data = DNotification.objects.get(id=id)
        com = Company.objects.get(user=data.user)
        modules = Modules_List.objects.get(company=com, status="New")
        serializer = ModulesListSerializer(modules)
        req = {
            "id": data.id,
            "user": "Company",
            "name": com.company_name,
            "email": com.email,
            "code": com.company_code,
            "contact": com.contact,
            "username": com.user.username,
            "image": com.image.url if com.image else None,
            "endDate": com.end_date,
            "termUpdation": True if data.payment_terms_updation else False,
            "moduleUpdation": True if data.module_list else False,
            "term": (
                str(com.payment_term.payment_terms_number)
                + " "
                + com.payment_term.payment_terms_value
                if com.payment_term
                else "Trial Period"
            ),
            "newTerm": (
                str(data.payment_terms_updation.payment_term.payment_terms_number)
                + " "
                + data.payment_terms_updation.payment_term.payment_terms_value
                if data.payment_terms_updation
                else ""
            ),
        }
        if data.module_list:
            modules_pending = Modules_List.objects.filter(
                user=data.user, status="pending"
            )
            current_modules = Modules_List.objects.filter(
                user=data.user, status="New"
            )

            # Extract the field names related to modules
            module_fields = [
                field.name
                for field in Modules_List._meta.fields
                if field.name
                not in [
                    "id",
                    "company",
                    "status",
                    "update_action",
                    "company",
                    "user",
                ]
            ]

            # Get the previous and new values for the selected modules
            previous_values = current_modules.values(*module_fields).first()
            new_values = modules_pending.values(*module_fields).first()

            # Iterate through the dictionary and replace None with 0
            for key, value in previous_values.items():
                if value is None:
                    previous_values[key] = 0

            # Iterate through the dictionary and replace None with 0
            for key, value in new_values.items():
                if value is None:
                    new_values[key] = 0

            # Identify added and deducted modules
            added_modules = {}
            deducted_modules = {}

            for field in module_fields:
                if new_values[field] > previous_values[field]:
                    added_modules[field] = new_values[field] - previous_values[field]
                elif new_values[field] < previous_values[field]:
                    deducted_modules[field] = previous_values[field] - new_values[field]

            return Response(
                {
                    "status": True,
                    "data": req,
                    "modules": serializer.data,
                    "added_modules": added_modules,
                    "deducted_modules": deducted_modules,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"status": True, "data": req}, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Company not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Distributor.DoesNotExist:
        return Response(
            {"status": False, "message": "Distributor not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(("POST",))
def distributorModuleUpdationAccept(request):
    try:
        id = request.data["id"]
        data = DNotification.objects.get(id=id)
        allmodules = Modules_List.objects.get(user=data.user, status="New")
        allmodules.delete()

        allmodules1 = Modules_List.objects.get(
            user=data.user, status="pending"
        )
        allmodules1.status = "New"
        allmodules1.save()

        data.status = "old"
        data.save()

        # notification
        CNotification.objects.create(
            user=allmodules1.user,
            company=allmodules1.company,
            title="Modules Updated..!",
            description="Your module update request is approved",
        )

        return Response({"status": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("DELETE",))
def distributorModuleUpdationReject(request):
    try:
        id = request.data["id"]
        data = DNotification.objects.get(id=id)
        allmodules = Modules_List.objects.get(
            user=data.user, status="pending"
        )
        allmodules.delete()

        data.delete()

        return Response({"status": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(("GET",))
def getSelfData(request, id):
    try:
        data = User.objects.get(id=id)
        img = None
        name = None
        if data.role == "Company":
            usrData = Company.objects.get(user=data)
            img = usrData.image.url if usrData.image else None
            name = usrData.company_name
        elif data.role == "Distributor":
            usrData = Distributor.objects.get(user=data)
            img = usrData.image.url if usrData.image else None
            name = data.first_name + " " + data.last_name
        elif data.role == "Staff":
            usrData = Staff.objects.get(user=data)
            img = usrData.image.url if usrData.image else None
            name = data.first_name + " " + data.last_name
        else:
            usrData = None

        details = {"name": name, "image": img}

        return Response({"status": True, "data": details})
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Company_Staff


@api_view(("GET",))
def checkCompanyPaymentTerms(request, id):
    try:
        s_id = id
        data = User.objects.get(id=s_id)
        if data.role == "Company":
            com = Company.objects.get(user=data)
            payment_request = Payment_Terms_updation.objects.filter(
                user=data, status="New"
            ).exists()

            title2 = ["Modules Updated..!", "New Plan Activated..!"]
            today_date = date.today()
            notification = CNotification.objects.filter(
                status="New", company=com, title__in=title2, noti_date__lt=today_date
            ).order_by("-id", "-noti_date")
            notification.update(status="old")

            diff = (com.end_date - today_date).days

            # payment term and trial period alert notifications for notification page
            cmp_name = com.company_name
            if com.payment_term:
                if (
                    not CNotification.objects.filter(
                        company=com, title="Payment Terms Alert", status="New"
                    ).exists()
                    and diff <= 20
                ):

                    n = CNotification(
                        user=data,
                        company=com,
                        title="Payment Terms Alert",
                        description="Your Payment Terms End Soon",
                    )
                    n.save()
                    if com.registration_type == "self":
                        d = ANotification(
                            user=data,
                            title="Payment Terms Alert",
                            description=f"Current  payment terms of {cmp_name} is expiring",
                        )
                    else:
                        d = DNotification(
                            user=data,
                            distributor=com.distributor,
                            title="Payment Terms Alert",
                            description=f"Current  payment terms of {cmp_name} is expiring",
                        )

                    d.save()
            else:
                if (
                    not CNotification.objects.filter(
                        company=com, title="Trial Period Alert", status="New"
                    ).exists()
                    and diff <= 10
                ):
                    n = CNotification(
                        user=data,
                        company=com,
                        title="Trial Period Alert",
                        description="Your Trial Period End Soon",
                    )
                    n.save()

                    if com.registration_type == "self":
                        d = ANotification(
                            user=data,
                            title="Payment Terms Alert",
                            description=f"Current  payment terms of {cmp_name} is expiring",
                        )
                    else:
                        d = DNotification(
                            user=data,
                            distributor=com.distributor,
                            title="Payment Terms Alert",
                            description=f"Current  payment terms of {cmp_name} is expiring",
                        )

                    d.save()

            # Calculate the date 20 days before the end date for payment term renew and 10 days before for trial period renew
            if com.payment_term:
                term = True
                reminder_date = com.end_date - timedelta(days=20)
            else:
                term = False
                reminder_date = com.end_date - timedelta(days=10)
            current_date = date.today()
            alert_message = current_date >= reminder_date

            # Calculate the number of days between the reminder date and end date
            days_left = (com.end_date - current_date).days
            return Response(
                {
                    "status": True,
                    "alert_message": alert_message,
                    "endDate": com.end_date,
                    "days_left": days_left,
                    "paymentTerm": term,
                    "payment_request": payment_request,
                    "companyName": cmp_name,
                },
                status=status.HTTP_200_OK,
            )
        else:
            com = Staff.objects.get(user=data).company
            return Response(
                {"status": True, "companyName": com.company_name},
                status=status.HTTP_200_OK,
            )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getModules(request, id):
    try:
        data = User.objects.get(id=id)
        if data.role == "Company":
            com = Company.objects.get(user=data)
        else:
            com = Staff.objects.get(user=data).company
        # com = Company.objects.get(user=data)
        modules = Modules_List.objects.get(company=com, status="New")
        module_request = Modules_List.objects.filter(
            company=com, status="pending"
        ).exists()
        serializer = ModulesListSerializer(modules)
        return Response(
            {
                "status": True,
                "module_request": module_request,
                "modules": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Company not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getProfileData(request, id):
    try:
        data = User.objects.get(id=id)
        if data.role == "Company":
            usrData = Company.objects.get(user=data)
            payment_request = Payment_Terms_updation.objects.filter(
                user=data, status="New"
            ).exists()
            personal = {
                "companyLogo": usrData.image.url if usrData.image else False,
                "userImage": False,
                "firstName": data.first_name,
                "lastName": data.last_name,
                "email": usrData.email,
                "username": data.username,
                "companyContact": usrData.contact,
                "userContact": "",
            }
            company = {
                "businessName": usrData.business_name,
                "companyName": usrData.company_name,
                "companyType": usrData.company_type,
                "industry": usrData.industry,
                "companyCode": usrData.company_code,
                "companyEmail": usrData.email,
                "panNumber": usrData.pan_no,
                "gstType": usrData.gst_type,
                "gstNo": usrData.gst_no,
                "paymentTerm": (
                    str(usrData.payment_term.payment_terms_number)
                    + " "
                    + usrData.payment_term.payment_terms_value
                    if usrData.payment_term
                    else "Trial Period"
                ),
                "endDate": usrData.end_date,
                "address": usrData.address,
                "city": usrData.city,
                "state": usrData.state,
                "pincode": usrData.pincode,
            }

        if data.role == "Staff":
            staffData = Staff.objects.get(user=data)
            payment_request = Payment_Terms_updation.objects.filter(
                user=staffData.company.user, status="New"
            ).exists()

            personal = {
                "companyLogo": False,
                "userImage": staffData.image.url if staffData.image else False,
                "firstName": data.first_name,
                "lastName": data.last_name,
                "email": staffData.email,
                "username": data.username,
                "companyContact": staffData.company.contact,
                "userContact": staffData.contact,
            }
            company = {
                "businessName": staffData.company.business_name,
                "companyName": staffData.company.company_name,
                "companyType": staffData.company.company_type,
                "industry": staffData.company.industry,
                "companyCode": staffData.company.company_code,
                "companyEmail": staffData.company.email,
                "panNumber": staffData.company.pan_no,
                "gstType": staffData.company.gst_type,
                "gstNo": staffData.company.gst_no,
                "paymentTerm": (
                    str(staffData.company.payment_term.payment_terms_number)
                    + " "
                    + staffData.company.payment_term.payment_terms_value
                    if staffData.company.payment_term
                    else "Trial Period"
                ),
                "endDate": staffData.company.end_date,
                "address": staffData.company.address,
                "city": staffData.company.city,
                "state": staffData.company.state,
                "pincode": staffData.company.pincode,
            }

        return Response(
            {
                "status": True,
                "personalData": personal,
                "companyData": company,
                "payment_request": payment_request,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("PUT",))
@parser_classes((MultiPartParser, FormParser))
def editCompanyProfile(request):
    try:
        login_id = request.data["Id"]
        data = User.objects.get(id=login_id)
        com = Company.objects.get(user=data)

        logSerializer = UserSerializer(data, data=request.data)
        serializer = CompanySerializer(com, data=request.data, partial=True)

        fName = request.data['first_name']
        lName = request.data['last_name']
        email = request.data['email']

        if fName != "":
            data.first_name = fName
        if lName != "":
            data.last_name = lName
        if email != "":
            data.email = email

        data.save()

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if logSerializer.is_valid():
        #     logSerializer.save()
        # else:
        #     return Response(
        #         {"status": False, "data": logSerializer.errors},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

    except User.DoesNotExist:
        return Response(
            {"status": False, "message": "User details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Company details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("PUT",))
@parser_classes((MultiPartParser, FormParser))
def editStaffProfile(request):
    try:
        login_id = request.data["Id"]
        data = User.objects.get(id=login_id)
        stf = Staff.objects.get(user=data)

        logSerializer = UserSerializer(data, data=request.data)
        serializer = StaffSerializer(stf, data=request.data, partial=True)

        fName = request.data["first_name"]
        lName = request.data["last_name"]
        email = request.data["email"]

        if fName != "":
            data.first_name = fName
        if lName != "":
            data.last_name = lName
        if email != "":
            data.email = email

        data.save()

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except User.DoesNotExist:
        return Response(
            {"status": False, "message": "User details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Staff.DoesNotExist:
        return Response(
            {"status": False, "message": "Staff details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(("GET",))
def getStaffRequests(request, id):
    try:
        data = User.objects.get(id=id)
        com = Company.objects.get(user=data)
        data1 = Staff.objects.filter(company=com, company_approval_status="NULL")
        requests = []
        for i in data1:
            req = {
                "id": i.id,
                "name": i.user.first_name + " " + i.user.last_name,
                "email": i.email,
                "contact": i.contact,
                "username": i.user.username,
            }
            requests.append(req)

        return Response({"status": True, "data": requests})
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("GET",))
def getAllStaffs(request, id):
    try:
        data = User.objects.get(id=id)
        com = Company.objects.get(user=data)
        data1 = Staff.objects.filter(company=com, company_approval_status="Accept")
        requests = []
        for i in data1:
            req = {
                "id": i.id,
                "name": i.user.first_name + " " + i.user.last_name,
                "email": i.email,
                "contact": i.contact,
                "username": i.user.username,
            }
            requests.append(req)

        return Response({"status": True, "data": requests})
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("PUT",))
def staffRequestAccept(request, id):
    try:
        data = Staff.objects.get(id=id)
        data.company_approval_status = "Accept"
        data.save()
        return Response({"status": True}, status=status.HTTP_200_OK)
    except Staff.DoesNotExist:
        return Response(
            {"status": False, "message": "Staff details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("DELETE",))
def staffRequestReject(request, id):
    try:
        data = Staff.objects.get(id=id)
        data.user.delete()
        data.delete()
        return Response({"status": True}, status=status.HTTP_200_OK)
    except Staff.DoesNotExist:
        return Response(
            {"status": False, "message": "Staff details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(("POST",))
def company_gsttype_change(request):
    try:
        s_id = request.data["ID"]
        data = User.objects.get(id=s_id)
        com = Company.objects.get(user=data)

        # Get data from the form

        # gstno = request.POST.get('gstno')
        gsttype = request.data["gsttype"]

        com.gst_type = gsttype

        com.save()

        # Check if gsttype is one of the specified values
        if gsttype in ["unregistered Business", "Overseas", "Consumer"]:
            com.gst_no = ""
            com.save()
            return Response(
                {"status": True, "message": "GST Type changed"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": True, "message": "GST Type changed, add GST Number"},
                status=status.HTTP_200_OK,
            )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(("POST",))
def changeCompanyPaymentTerm(request):
    try:
        s_id = request.data["ID"]
        data = User.objects.get(id=s_id)
        com = Company.objects.get(user=data)
        pt = request.data["payment_term"]

        pay = PaymentTerms.objects.get(id=pt)

        data1 = Payment_Terms_updation(user=data, payment_term=pay)
        data1.save()

        if com.registration_type == "self":
            noti = ANotification(
                user=data,
                payment_terms_updation=data1,
                title="Change Payment Terms",
                description=com.company_name + " wants to subscribe a new plan",
            )
            noti.save()
        else:
            noti = DNotification(
                distributor=com.distributor,
                user=data,
                payment_terms_updation=data1,
                title="Change Payment Terms",
                description=com.company_name + " wants to subscribe a new plan",
            )
            noti.save()

        return Response(
            {"status": True, "message": "Request Sent.!"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

@api_view(("POST",))
def editModules(request):
    try:
        login_id = request.data["user"]
        data = User.objects.get(id=login_id)
        com = Company.objects.get(user=data)

        request.data["company"] = com.id
        request.data["status"] = "pending"

        serializer = ModulesListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data1 = Modules_List.objects.filter(company=com).update(
                update_action=1
            )
            modules = Modules_List.objects.get(id=serializer.data["id"])
            if com.registration_type == "self":
                noti = ANotification(
                    user=data,
                    module_list=modules,
                    title="Module Updation",
                    description=com.company_name + " wants to update current Modules",
                )
                noti.save()
            else:
                noti = DNotification(
                    distributor=com.distributor,
                    user=data,
                    module_list=modules,
                    title="Module Updation",
                    description=com.company_name + " wants to update current Modules",
                )
                noti.save()

            return Response(
                {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": False, "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except User.DoesNotExist:
        return Response(
            {"status": False, "message": "Login details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Company.DoesNotExist:
        return Response(
            {"status": False, "message": "Company details not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@api_view(("GET",))
def fetchNotifications(request, id):
    try:
        s_id = id
        data = User.objects.get(id=s_id)
        if data.role == "Company":
            com = Company.objects.get(user=data)
            noti = CNotification.objects.filter(
                status="New", company=com
            ).order_by("-id", "-noti_date")
            serializer = CNotificationsSerializer(noti, many=True)
            return Response(
                {"status": True, "notifications": serializer.data, 'count':len(noti)},
                status=status.HTTP_200_OK,
            )
        else:
            com = Staff.objects.get(user=data).company
            nCount = CNotification.objects.filter(company = com, status = 'New')
            return Response(
                {"status": True, "notifications": None, 'count':len(nCount)}, status=status.HTTP_200_OK
            )
    except Exception as e:
        return Response(
            {"status": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )