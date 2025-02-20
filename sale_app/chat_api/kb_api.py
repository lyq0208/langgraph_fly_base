import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms.excel_form import ExcelUploadForm
from .forms.file_upload_form import FileUploadForm

from ..config.log import Logger
from ..core.kb.kb_sevice import KBService
from ..core.kb.xlsx_qa_view import xlsx_qa_upload

logger = Logger("fly_base")


# xlsx文件上传
class DocumentForm:
    pass


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_doc = request.FILES['document']
            file_extension = os.path.splitext(file_doc.name)[1].lower()
            if file_extension == '.xlsx':
                xlsx_qa_upload(file_doc)
            else:
                return HttpResponse(f'文件格式错误！目前不支持{file_extension}')
            return HttpResponse('文件上传成功！')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form})


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['document']
            collection_name = request.POST.get("collection_name")
            # 使用 FileSystemStorage 来保存文件到指定目录
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'kb_file'))
            filename = fs.save(excel_file.name, excel_file)
            # 获取文件的URL路径
            absolute_path = os.path.join(fs.base_location, filename)
            KBService.parse(absolute_path, collection_name)
            return HttpResponse('文件上传成功！')
    # else:
    # form = DocumentForm()
    return render(request, 'upload_document.html')


@csrf_exempt
def search(request):
    query = request.GET.get('query')
    collection_name = request.GET.get("collection_name")
    file_name = request.GET.get("file_name")
    data = KBService.similarity_search(query, collection_name, file_name)
    json = {
        "data": data.__str__()
    }
    return JsonResponse(json)


@csrf_exempt
def create_collection_api(request):
    if request.method == 'POST':
        collection_name = request.POST.get("collection_name")
        if not collection_name:
            return HttpResponse("collection_name is null")
        KBService.create_collection(collection_name)

    return render(request, 'create_collection.html')


@csrf_exempt
def upload_and_read_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            collection_name = request.GET.get("collection_name")
            # 使用 FileSystemStorage 来保存文件到指定目录
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'kb_file'))
            filename = fs.save(excel_file.name, excel_file)
            # 获取文件的URL路径
            # fs.base_location = settings.MEDIA_ROOT
            # file_url = fs.url(filename)
            absolute_path = os.path.join(fs.base_location, filename)
            KBService.parse_excel(absolute_path, collection_name)
    return JsonResponse({'data': 'sucess'})


@csrf_exempt
def text_insert_milvus(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        collection_name = request.POST.get("collection_name", None) or None
        KBService.text_insert(text, collection_name)
    return JsonResponse({'data': 'sucess'})


@csrf_exempt
def hybrid_search(request):
    query = request.GET.get('query')
    collection_name = request.GET.get("collection_name")
    file_name = request.GET.get("file_name")

    data = KBService.hybrid_search(query, collection_name, file_name)
    json = {
        "data": data.__str__()
    }
    return JsonResponse(json)


@csrf_exempt
def keyword_search(request):
    query = request.GET.get('query')
    collection_name = request.GET.get("collection_name")
    file_name = request.GET.get("file_name")

    data = KBService.keyword_search(query, collection_name, file_name)
    json = {
        "data": data.__str__()
    }
    return JsonResponse(json)
