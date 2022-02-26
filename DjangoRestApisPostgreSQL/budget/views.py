from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from . import  scotiaParser 
import os
from budget.models import Transaction
from budget.serializers import TransactionSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.files.storage import default_storage
from django.core.files import File

@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def tutorial_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == 'GET':
        tutorials = Transaction.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TransactionSerializer(tutorials, many=True)
        # 'safe=False' for objects serialization
        parsers =[]
        statement_dir_lists =[]
        
        SCOTIA_BANK_PATH = os.getcwd()+"/scotiaBankStatments"
        statement_dir_lists.append(SCOTIA_BANK_PATH)
        parsers.append(scotiaParser)
        def automateParse(full_path, parser):
            statement_dir_list = os.listdir(full_path)
            for  path  in (statement_dir_list):
                file_path = full_path +"/"+ path
                return parser.main(file_path)

        for job in range(0,len(parsers)) : 
            automateParse(statement_dir_lists[job],parsers[job])
        return JsonResponse(tutorials_serializer.data, safe=False)

    elif request.method == 'DELETE':
        count = Transaction.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TransactionSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    # find tutorial by pk (id)
    try: 
        tutorial = Transaction.objects.get(pk=pk) 
    except Transaction.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = Transaction.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = TransactionSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)




@csrf_exempt
def Save_File(request):
  
    file = request.FILES['uploadedFile']
    file_name =default_storage.save(file.name,file)
    scotiaParser.main()

    return JsonResponse(file_name, safe=False)

 
