from rest_framework import serializers
from .models import Credit_score, Auto_eda

class Credit_serializer(serializers.ModelSerializer):
    class Meta:
        model = Credit_score
        fields = '__all__'
        
        
class Auto_serializer(serializers.ModelSerializer):
    class Meta:
        model = Auto_eda
        fields = '__all__'

# # serializers.py

# from rest_framework import serializers
# from .models import UploadedFile

# class UploadedFileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UploadedFile
#         fields = ['id', 'file_name', 'uploaded_at']


