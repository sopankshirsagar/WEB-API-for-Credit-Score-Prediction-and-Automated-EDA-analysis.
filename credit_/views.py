
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
import pandas as pd 
import numpy as np
import json
import os
from ydata_profiling import ProfileReport
import requests


from .models import Credit_score , Auto_eda
from .serializers import Credit_serializer, Auto_serializer
from rest_framework.views import APIView


# Create your views here.




def home(request):    
    if request.method == 'POST':
        file = request.FILES['file']
        documents = Credit_score.objects.create(file=file)
        documents.save()

        try:    
    
            file_path = documents.file.path
            if not os.path.exists(file_path):
                return render(request, 'index.html',{"error": "File not found"})
            
            with open(file_path, 'r') as file:
                    file_content = json.load(file)
                
            model = pd.read_pickle(r"C:\Users\sopan\Desktop\jupyter\All dataset\Credit score prediction\credit_score.pkl")
                
                # for single record 
            if type(file_content) ==dict: 
                data =[np.array(list(file_content.values()))] 
                pred = model.predict(data)
                return render(request, 'index.html',{"CreditScore": pred})
                
                # for multiple records
            else:
                result =dict()
                for i in range(len(file_content)):                    
                    data = ([np.array(list(file_content[i].values()))])   
                    pred = model.predict(data)
                    result[i] =pred
                return render(request,'index.html',{"result1":result})                    
                
        except Credit_score.DoesNotExist:
            return render(request, 'index.html',{"error": "Record not found"})
        except json.JSONDecodeError:
            return render(request, 'index.html',{"error": "Invalid JSON format"})
        except Exception as e:
            return render(request, 'index.html',{"error": str(e)})
    else:
        
        try :
            api_url = requests.get('http://127.0.0.1:8000/')
            response = requests.get(api_url)
            response.raise_for_status()
            api_data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            api_data = {"error": str(e)}
        return render(request, 'index.html', {'api_data': api_data})
    
    

def Auto_eda_view (request): 
    if request.method == 'POST':
        file = request.FILES['file']
        documents = Credit_score.objects.create(file=file)
        documents.save()
        
        try:    
    
            file_path = documents.file.path
            if not os.path.exists(file_path):
                return render(request, 'prediction.html',{"error": "File not found"})
            
            
            file_content = pd.read_csv(file_path)
            profile = ProfileReport(file_content, title='')
            output_file_path = os.path.join('templates', 'output.html')
            profile.to_file(output_file_path)
            
            with open(output_file_path,'r', encoding='utf-8') as file:
                profile_html = file.read()
                
                
            return render(request, 'prediction.html',{"profile_html": profile_html})

            
            
                    
        except Exception as e:
            return render(request, 'prediction.html',{"error": str(e)})
    
    
    else:
        return render(request,'prediction.html' )
    



class File_upload_view(APIView):
    def post(self, request, *args, **kwargs):
        # credit = Credit_score.objects.all()
        serializer = Credit_serializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
        
        
            return Response({'File uploaded successfully':serializer.data}, status=status.HTTP_201_CREATED)
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Json_data(APIView):
    def get(self, request, record_id, *args, **kwargs):
        try:
            json_file_record = Credit_score.objects.get(record_id=record_id)    
            file_path = json_file_record.file.path
            if not os.path.exists(file_path):
                return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

            with open(file_path, 'r') as file:
                file_content = json.load(file)
            
            model = pd.read_pickle(r"C:\Users\sopan\Desktop\jupyter\All dataset\Credit score prediction\credit_score.pkl")
            
            # for single record 
            if type(file_content) ==dict: 
                data =[np.array(list(file_content.values()))] 
                pred = model.predict(data)
                return Response({"Credit Score : ": pred}, status=status.HTTP_200_OK)
             
            # for multiple records
            else:
                result =dict()
                for i in range(len(file_content)):                    
                    data = ([np.array(list(file_content[i].values()))])   
                    pred = model.predict(data)
                    result[i] =({"Recored no": i, "Credit Score : ": pred})
                return Response(result, status=status.HTTP_200_OK)                    

                
        
        except Credit_score.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

