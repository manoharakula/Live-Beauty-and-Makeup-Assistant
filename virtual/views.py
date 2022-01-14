from django.http.response import JsonResponse
from django.shortcuts import render
from .models import ColorsPallete, LipsModel , LooksModel , FaceModel , EyesModel
import json
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps
from django.core import serializers
from django.views.generic import View, TemplateView
from .serialize import ColorsPalleteSerializer , LipsSerializer, FaceSerializer , EyesSerializer , LooksSerializer





def lips(request):
    return render(request , "virtual/list.html",{})

def virtual_demo(request):
    liplist = LipsModel.objects.all()
    facelist  = FaceModel.objects.all()
    lookslist = LooksModel.objects.all()
    eyeslist = EyesModel.objects.all()
    return render(request , "virtual/index.html",{"eyeslist":eyeslist ,"lookslist":lookslist,"facelist":facelist, "liplist" : liplist})


def profile(request,objectid):
    lipobject = list(LipsModel.objects.all())[objectid]
    print(lipobject)
    return render(request , "virtual/profile.html" , {"object" : lipobject})


class PostJsonView(View):
    def get(self, *args , **kwargs):
        print(kwargs)
        
        classname = kwargs["class"]

        if classname == "lookspage":
            modelobject = LooksModel.objects.filter(name__icontains = kwargs["name"])
            data = LipsSerializer(modelobject , many  = True).data
        
        if classname == "facepage":
            modelobject = FaceModel.objects.filter(name__icontains = kwargs["name"])
            data = LipsSerializer(modelobject , many  = True).data
        
        if classname == "eyespage":
            modelobject = EyesModel.objects.filter(name__icontains = kwargs["name"])
            data = LipsSerializer(modelobject , many  = True).data

        if classname == "lipspage":
            modelobject = LipsModel.objects.filter(name__icontains = kwargs["name"])
            data = LipsSerializer(modelobject , many  = True).data

       
        print(data)
        return JsonResponse({"object":data}, safe= False)