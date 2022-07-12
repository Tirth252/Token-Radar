
from django.contrib.auth.models import User
from django.db.models.fields.related import create_many_to_many_intermediary_model
from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from requests.models import default_hooks
from .models import Coins
from django import forms,template

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from pythonpancakes import PancakeSwapAPI
import pprint as pp 

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from allauth.account.views import PasswordChangeView



ps = PancakeSwapAPI()





class Home(ListView):
    template_name = 'index.html'
    queryset = Coins.objects.filter(usercoin = True)
    context_object_name = 'coins'
    ordering = ['-votes']
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if len(Coins.objects.filter(registeredBy=self.request.user.id)) > 0:
                context['user_coin'] = Coins.objects.filter(registeredBy=self.request.user.id)
            else:
                context['user_coin'] = False
        context['promoted_coins'] = Coins.objects.filter(is_promoted = True).order_by("-votes")
        for usercoin in Coins.objects.filter(usercoin = True):
            usercoin.updatePrice()
            print(usercoin)
       
        return context




class coinsubmissionView(CreateView):
    model = Coins
    template_name = 'coinsubmit.html'
    fields = ['name','symbol','network','contractAddress','description','launchDate','telegram','twitter','discord','logo','customchart']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if len(Coins.objects.filter(registeredBy=self.request.user.id)) > 0:
                context['user_coin'] = Coins.objects.filter(registeredBy=self.request.user.id)
            else:
                context['user_coin'] = False
     
        return context


    def get_form(self, form_class=None):
        
        if form_class is None:
            form_class = self.get_form_class()

        form = super(coinsubmissionView, self).get_form(form_class)
        form.fields['launchDate'].widget = forms.DateInput(attrs={'type': 'date'})
        form.fields['captcha'] = ReCaptchaField(widget=ReCaptchaV2Checkbox)
        return form

    def form_valid(self,form):
        form.instance.registeredBy = self.request.user
        
        return super().form_valid(form)


class coindetailView(DetailView):
    model = Coins
    template_name = 'coindetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if len(Coins.objects.filter(registeredBy=self.request.user.id)) > 0:
                context['user_coin'] = Coins.objects.filter(registeredBy=self.request.user.id)
            else:
                context['user_coin'] = False
        obj = super(coindetailView,self).get_object()
        obj.updatePrice()

        return context


class alltimebestView(ListView):
    model = Coins
    template_name = 'alltimebest.html'
    context_object_name = "coins"
    ordering = ['id']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if len(Coins.objects.filter(registeredBy=self.request.user.id)) > 0:
                context['user_coin'] = Coins.objects.filter(registeredBy=self.request.user.id)
            else:
                context['user_coin'] = False

        tokens = ps.tokens()

        for contractA,data in tokens.get('data').items():
            try:
                coin = Coins.objects.get(contractAddress = contractA)
                coin.priceUSD = data.get('price')
                coin.priceBNB = data.get('price_BNB')
                coin.save()
          
            except ObjectDoesNotExist:
                continue
        for usercoin in Coins.objects.filter(usercoin = True):
            usercoin.updatePrice()
       
            
        return context  


class SearchcoinView(ListView):

    template_name = "search.html"
    context_object_name = "coins"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if len(Coins.objects.filter(registeredBy=self.request.user.id)) > 0:
                context['user_coin'] = Coins.objects.filter(registeredBy=self.request.user.id)
            else:
                context['user_coin'] = False

        
        return context
    def get_queryset(self):
        if "search" in self.request.GET:
            self.inpt = self.request.GET.get("search")
        
   
            return Coins.objects.filter(name__icontains=self.inpt)
        else:
            return Coins.objects.all()

@login_required
def Vote(request,pk):

    coin = Coins.objects.get(id=pk)
    if request.user not in coin.votedBy.all():
        coin.votedBy.add(request.user)
        print(coin.votedBy.all())
        coin.votes = coin.votes + 1
        coin.save()
    
    return redirect(request.META['HTTP_REFERER'])



def search_status(request):

    if request.method == "GET":
        search_text = request.GET['search_text']
        if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
            statuss = Coins.objects.filter(status__contains = search_text)
        else:
            statuss = []

        return render(request, 'alltimebest.html', {'statuss':statuss})



def privacypolicy(request):

    if request.user.is_authenticated:

        if len(Coins.objects.filter(registeredBy=self.request.user.id)) > 0:
            return render(request, 'privacypolicy.html', {"user_coin":Coins.objects.filter(registeredBy=request.user.id)})
            
        else:
             return render(request, 'privacypolicy.html', {"user_coin":False} )
    else:
         return render(request, 'privacypolicy.html', {"user_coin":False} )

