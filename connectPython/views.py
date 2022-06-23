# import filter
from django.shortcuts import render
from django.http import JsonResponse
import requests
from . import test
from . import Filter_Page
from django.shortcuts import HttpResponse
# import sys
# sys.path.append(
#     'C:Users/Pratik Kumar/Desktop/python/connectPython/connectPython')


def button(request):
    return render(request, "home.html")


def head(request):
    return render(request, "head.html")


def category(request):
    return render(request, "category.html")


def dateFilter(request):
    if(request.method == "POST"):
        # foo = request.GET.get('foo')
        # print(request.POST)
        print(request.POST)
        # return render(request,"category.html")
        res = outputdd()
        return JsonResponse({"res": "hii", "data": res})
        # return HttpResponse(res)


def output(request):
    data = requests.get("https://www.google.com/")
    # data=requests.get(“https://www.google.com/“)
    print(data.text)
    data = data.text
    return render(request, 'home.html', {'data': data})


def outputdd():
    # print("hii")
    res1 = test.past_VI_XII_monthCall()
    # print(res1, "kkkk")
    return res1
    # print(test.foo(5))
