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

            # ---super admin---

            if request.user.is_staff == 1:
                refresh = RefreshToken.for_user(log_user)
                return Response(
                    {
                        "status": True,
                        "redirect": "admin_home",
                        "user": str(log_user.id),
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "role": "Admin",
                    },
                    status=status.HTTP_200_OK,
                )

        # -------distributor ------

        # if Fin_Login_Details.objects.filter(
        #     User_name=user_name, password=passw
        # ).exists():
        #     data = Fin_Login_Details.objects.get(User_name=user_name, password=passw)
        #     if data.User_Type == "Distributor":
        #         did = Fin_Distributors_Details.objects.get(Login_Id=data.id)
        #         if did.Admin_approval_status == "Accept":
        #             request.session["s_id"] = data.id
        #             current_day = date.today()
        #             if current_day > did.End_date:
        #                 print("wrong")

        #                 if not Fin_Payment_Terms_updation.objects.filter(
        #                     Login_Id=data, status="New"
        #                 ).exists():
        #                     return Response(
        #                         {
        #                             "status": False,
        #                             "redirect": "wrong",
        #                             "Login_id": data.id,
        #                             "message": "Terms Expired",
        #                         }
        #                     )
        #                 else:
        #                     return Response(
        #                         {
        #                             "status": False,
        #                             "redirect": "distributor_registration",
        #                             "Login_id": data.id,
        #                             "message": "Term Updation Request is pending..",
        #                         }
        #                     )
        #             else:
        #                 return Response(
        #                     {
        #                         "status": True,
        #                         "redirect": "distributor_home",
        #                         "user": "Distributor",
        #                         "Login_id": data.id,
        #                     },
        #                     status=status.HTTP_200_OK,
        #                 )

        #         else:
        #             return Response(
        #                 {"status": False, "message": "Approval is Pending"},
        #                 status=status.HTTP_404_NOT_FOUND,
        #             )

        #     if data.User_Type == "Company":
        #         cid = Fin_Company_Details.objects.get(Login_Id=data.id)
        #         if (
        #             cid.Admin_approval_status == "Accept"
        #             or cid.Distributor_approval_status == "Accept"
        #         ):
        #             request.session["s_id"] = data.id

        #             com = Fin_Company_Details.objects.get(Login_Id=data.id)

        #             current_day = date.today()
        #             if current_day > com.End_date:
        #                 print("wrong")

        #                 if not Fin_Payment_Terms_updation.objects.filter(
        #                     Login_Id=data, status="New"
        #                 ).exists():
        #                     return Response(
        #                         {
        #                             "status": False,
        #                             "Login_id": data.id,
        #                             "redirect": "wrong",
        #                             "message": "Terms Expired",
        #                         }
        #                     )
        #                 else:
        #                     return Response(
        #                         {
        #                             "status": False,
        #                             "Login_id": data.id,
        #                             "redirect": "company_registration",
        #                             "message": "Term Updation Request is pending..",
        #                         }
        #                     )

        #             else:
        #                 return Response(
        #                     {
        #                         "status": True,
        #                         "redirect": "company_home",
        #                         "user": "Company",
        #                         "Login_id": data.id,
        #                     },
        #                     status=status.HTTP_200_OK,
        #                 )
        #         else:
        #             return Response(
        #                 {"status": False, "message": "Approval is Pending"},
        #                 status=status.HTTP_404_NOT_FOUND,
        #             )

        #     if data.User_Type == "Staff":
        #         cid = Fin_Staff_Details.objects.get(Login_Id=data.id)
        #         if cid.Company_approval_status == "Accept":
        #             request.session["s_id"] = data.id
        #             com = Fin_Staff_Details.objects.get(Login_Id=data.id)

        #             current_day = date.today()
        #             if current_day > com.company_id.End_date:
        #                 print("wrong")
        #                 return Response(
        #                     {
        #                         "status": False,
        #                         "Login_id": data.id,
        #                         "redirect": "staff_registration",
        #                         "message": "Your account is temporarily blocked",
        #                     }
        #                 )
        #             else:
        #                 return Response(
        #                     {
        #                         "status": True,
        #                         "redirect": "company_home",
        #                         "user": "Staff",
        #                         "Login_id": data.id,
        #                     },
        #                     status=status.HTTP_200_OK,
        #                 )
        #         else:
        #             return Response(
        #                 {"status": False, "message": "Approval is Pending"},
        #                 status=status.HTTP_404_NOT_FOUND,
        #             )

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
