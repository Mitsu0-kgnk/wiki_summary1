from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from .application.scray import wiki_summ
from .form import SearchForm
from django.http import HttpResponse
# Create your views here.

class Form(TemplateView):
    template_name = 'form.html'

    def get(self,request, *args, **kwargs):
        form = SearchForm(request.POST or None)
        return render(request, 'form.html',{
            'form': form
        })
    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        if form.is_valid():
            # word = form['kwd']
            word = request.POST['kwd']
            kwd = form.cleaned_data['kwd']
            w = wiki_summ(word)
            sentences = w.get_summary(w.scrayping())
            return render(request,'summary.html',{'sentences': sentences,'kwd':word})

class SummaryView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'summary.html')