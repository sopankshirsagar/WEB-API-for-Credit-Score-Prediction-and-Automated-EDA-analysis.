from django.urls import path
from .views import File_upload_view, Json_data, home , Auto_eda_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home,  name='home'),
    path('upload/',File_upload_view.as_view(), name='upload-json'),
    path('upload/<int:record_id>',Json_data.as_view(), name='prediction'),
    
    # path('base/', Upload_file, name='file-upload'), 
    path('auto_eda/', Auto_eda_view , name='Auto_eda_view')



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urls.py

# from django.urls import path
# from .views import FileUploadView

# urlpatterns = [
#     path('upload/', FileUploadView.as_view(), name='file-upload'),
# ]
