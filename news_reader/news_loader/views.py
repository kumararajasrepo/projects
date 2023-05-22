from django.shortcuts import render,redirect
from gnews.consumer import Consumer



def load_news(request):
    obj=Consumer("gnews")    
    nwarticles=obj.news_compile()
    context={'nwarticles':nwarticles}
    return render(request, 'news_loader/news_space.html',context)