from django.shortcuts import render  # type: ignore
from .models import  UserModel
from .serializers import (
    LoginSerializer,
    UserSerializer,
    InvoiceSerializer,
    ItemSerializer
)
from django.http import JsonResponse, HttpResponseBadRequest  # type: ignore
from django.views import View  # type: ignore
import json
from django.core.paginator import Paginator  # type: ignore
from django.db.models import Q
# from .data import invoiceData
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
import pymongo

from .models import Invoice,Item


#sample invoice data

# [
#     {
#         "items": [
#             {
#                 "desc": "testing",
#                 "quantity": 20,
#                 "rate": "200.00"
#             },
#             {
#                 "desc": "testing2",
#                 "quantity": 20,
#                 "rate": "200.00"
#             },
#             {
#                 "desc": "testing3",
#                 "quantity": 20,
#                 "rate": "200.00"
#             }
#         ],
#         "invoice_id": 1,
#         "client_name": "test",
#         "date": "2024-06-25"
#     }
# ]

######################################################################################3


# This project is done to view the db in Mongo ATLAS , so used collection,dbname connecting to
# MongoClient from pymongo. if need to see in mongoshell (mongosh) in cmd means , in settings.py,
# set the name of database and don,t connect to mongo client and can access the db using 
# model.objects.all() etc 

# if connected to mongoclient - accessed by Collection.find({}) etc

#---------------------------------------------------------------------------------------------

# MONGODB database and collection


client = pymongo.MongoClient("mongodb+srv://lavanya4301:lavanya1034@Cluster0.workfq9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
dbname = client['MongoDB']
collection = dbname['invoices']




###############################################################################################

# Module 46

# input used to sign up is 

#sample input:

# {
# "username":"test",
# "email":"test@gmail.com",
# "password":"password",
# "name":"testing"
# }

# if userid is set null means updated in db
# db.rest_api_usermodel.updateOne( { username: "test" }, { $set: { id: 1 } } )

# then signin data:

# {
# "username":"test",
# "password":"password"
# }



# deepak class signup method

# class SignupView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return JsonResponse({"message": "Äccount created successfully"}, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class SigninView(APIView):
#     def post(self,request):
#         data = request.data
#         serializer = LoginSerializer(data=data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             # print(user)
#             token = RefreshToken.for_user(user)
#             # return Response({"messages":"login done"},status = status.HTTP_200_OK)
#             return Response({"message": "login done", "access_token": str(token.access_token), "refresh_token": str(token)}, status=status.HTTP_200_OK)
#         return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
                
      
    
    
# to change password- extra function
class ChangePassword(View):
    permission_classes= [IsAuthenticated]
    
    def post(self,request):
        data= request.data
        user=request.user
        if user.check_password(data['old_password']):
            user.set_password(data['new_password'])
            user.save()
            return JsonResponse({"message":"Password has been changed"},status=200)
        return JsonResponse({"message":"password does not match"},status=400)
##########################################################################################3

class SignUpView(View):
    def post (self, request):
        inp = json.loads(request.body)
        
        # request.data- already json converted
        # request.body- have to change so use json.loads
        
        print(inp)
        # Hash the password
        raw_password =inp['password']  # Replace with the actual password you want to hash
        hashed_password = make_password(raw_password)
        print(hashed_password)
        inp['password'] = hashed_password
          
        serializer = UserSerializer(data=inp)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "message":"account created successfully",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                }, status = status.HTTP_201_CREATED)
        return JsonResponse (serializer.errors, status=status.HTTP_400_BAD_REQUEST,safe=False)



class SignInView(View):
    def post (self, request):
        inp = json.loads(request.body)
        serializer = LoginSerializer(data=inp)
        print(serializer)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "message":"login done",
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                }, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class UsersViewAll(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self,request):
        
#         user = UserModel.objects.all().values()
#         return JsonResponse (list (user), safe=False)
    
class InvoiceView(APIView):
    
    def get(self,request):
        serializer_class = InvoiceSerializer
        invoiceData = collection.find({})
        serializer = serializer_class(invoiceData,many=True).data
        return JsonResponse(serializer,status=200,safe=False)
    
    def post(self,request):
       
        invoice_data = list(collection.find({}))
        print("inv",invoice_data)
        data=request.data  # request.data is dic format
        # request.body have to be converted so will use json.load
        
        data["invoice_id"]= len(invoice_data)+1
        serialiser = InvoiceSerializer(data=data)
        if serialiser.is_valid():
            collection.insert_one(serialiser.data)
            return JsonResponse({"message":"Invoice added"},safe=False,status=200)
        
class InvoiceDetailView(APIView):
    
    
    def get(self,request,id):
        queryset = collection.find({})
        for val in queryset:
            if val["invoice_id"]==id:
                serializer= InvoiceSerializer(val)
                return JsonResponse(serializer.data)
        return JsonResponse({"message":"Invoice Not found"},status=404)
                    
          
class ItemsView(APIView):
    
   
    
    def post(self,request,id):
        invoice = collection.find_one({"invoice_id": id})
        
        if invoice:
            serializer= ItemSerializer(data=request.data)
            if serializer.is_valid():
                collection.update_one(
                {"invoice_id": id},
                {"$push": {"items": serializer.data}}
            )
                    
                return JsonResponse({"message":"Item has been added"},status=200)
            return JsonResponse(serializer.errors,status=400)                
        return JsonResponse({"message":"Invoice Not found"},status=404)
                
        
            
              
            