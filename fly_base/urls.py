"""
URL configuration for fly_base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from sale_app.chat_api.api import to_chat
from sale_app.chat_api.file import image_preview
from sale_app.chat_api.kb_api import upload_file, search, create_collection_api, upload_and_read_excel, \
    hybrid_search, keyword_search, text_insert_milvus, upload

# app_name = 'fly-base'

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("api/chat", to_chat, name='chat'),
    path('kb/upload', upload, name='upload'),
    path('kb/upload_file', upload_file, name='upload_file'),
    path('kb/search', search),
    path('kb/create_collection', create_collection_api,name='create_collection'),
    path('kb/upload_and_read_excel', upload_and_read_excel),
    path('kb/hybrid_search', hybrid_search),
    path('kb/keyword_search', keyword_search),
    path('kb/text_insert_milvus', text_insert_milvus),
    path('file/image-preview/<str:fileName>', image_preview, name='image_preview'),
]
