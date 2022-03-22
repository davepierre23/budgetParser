
from django.shortcuts import render, redirect 
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status, generics
from .parsers import  parser
import os
from budget.models import Transaction
from budget.serializers import TransactionSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.parsers import JSONParser
from django.core.files.storage import default_storage
from django.core.files import File
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.db.models import Q
from .models  import Transaction


@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def transaction_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        transactions_serializer = TransactionSerializer(transactions,many=True)
        return JsonResponse(transactions_serializer.data,safe=False)
        

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
 

@api_view(['GET'])
def transaction_detail(request):
    bankAction =request.GET.get('bankAction', None)
    startDate =request.GET.get('startDate', None)
    endDate  =request.GET.get('endDate', None)

    # bankAction = request.GET["bankAction"]
    numberOfResults = None
    transaction_description = "Payroll Deposit"

    #lazy loaded so can dynamicially do it
    transactions = Transaction.objects.filter( transactonDate__range=[startDate,endDate ])

    if bankAction is not None :
        transactions = transactions.filter( bankAction__in=bankAction)

    #case insentive check to see if a word is similar
    if transaction_description is not None:
        transactions = transactions.filter( transactonDescript__icontains=transaction_description)

    #limit order by number if Results
    if numberOfResults is not None :
        transactions= transactions[:numberOfResults]


    transactions_serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(transactions_serializer.data, safe=False)
 

@csrf_exempt
def save_file(request):
    file = request.FILES['uploadedFile']
    file_name =default_storage.save(file.name,file)
    print(file_name)

    #  Reading file from storage
    file = default_storage.open(file_name)
    file_url = default_storage.url(file_name)
    print(os.getcwd() + file_url)
    data =parser.parse(os.getcwd() +file_url)
    
    for model in data :
        populateTransaction(model)


    return JsonResponse({
        'result':'sucess'
    })

def populateTransaction(data):
    model =Transaction(bankAction=data["bankAction"],transactonDate = data["transactonDate"],amount=data["amount"],transactonDescript=data["transactonDescript"])
    model.save()


#User Authentication functions has not been tested yet 
@csrf_exempt
def create_user(request):

    # username = request.POST['username']
    password = request.POST['password']
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    email = request.POST['email']
    password = request.POST['password']
    if request.method == 'POST':
        user = User.objects.create_user(email,email,password)
        user.first_name = firstName
        user.last_name = lastName
        user.save()
        return JsonResponse({"result":"success"})



@csrf_exempt
def login_user(request):
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"result":"success"})

        # Redirect to a success page.
        ...
    else:
        return JsonResponse({"result":"fail user authentication"})

        # Return an 'invalid login' error message.

def logout_view(request):
    logout(request)
    # Redirect to a success page.



@login_required(login_url="/login")
def home(request):
    posts = Transaction.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    return render(request, 'main/home.html', {"posts": posts})


@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, 'main/create_post.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})