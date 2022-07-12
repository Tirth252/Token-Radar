from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from pythonpancakes import PancakeSwapAPI
ps = PancakeSwapAPI()


# Create your models here.
class Coins(models.Model):
    NETWORK = [
    ('BSC', 'Binance Smart Chain'),
    ('ERC-20', 'Ethereum Network'),
    ('POLYGON', 'Polygon Network'),
    ('TRC-20', 'Tron Smart Chain'),
    ('OEC-20', "OkEx network"),
    ('FRC-20', "Fantom smart chain"),
]
    name = models.CharField(max_length=50,blank=False)
    symbol = models.CharField(max_length=50,blank=False)
    network = models.CharField(max_length=7, choices=NETWORK, default='BSC')
    contractAddress = models.CharField(max_length=100,blank=False,unique=True)
    description = models.TextField(default= ' ', blank=False)
    launchDate = models.DateTimeField(blank=True,null=True)
    telegram = models.CharField(max_length=100,blank=True)
    twitter = models.CharField(max_length=100,blank=True)
    discord = models.CharField(max_length=100,blank=True)
    is_promoted = models.BooleanField(default=False)
    website = models.URLField(blank=True)
    priceUSD = models.DecimalField(max_digits=100, decimal_places=15,blank=True,null= True,max_length = 100)
    priceBNB = models.DecimalField(max_digits=100, decimal_places=15,blank=True,null= True,max_length = 100)
    votes = models.IntegerField(default=0)
    votedBy = models.ManyToManyField(User,blank=True,related_name= 'whovoted')
    registeredBy = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    logo = models.ImageField(upload_to="logos", blank=True, null=True, default = '../static/images/icons/bitcoin.png' )
    customchart = models.URLField(blank=True)
    alltimebest = models.BooleanField(default = False) #coins from api (for alltimebest table)
    usercoin = models.BooleanField(default=True) #coins which user registered (for normal coin table)

    def get_absolute_url(self):
        print(reverse("coin", kwargs= {'pk': self.pk}))
        return reverse("coin", kwargs= {'pk': self.pk})

    
    def __str__(self):
        return self.name

    
    def updatePrice(self):
        try:
            token = ps.tokens(self.contractAddress)
            self.priceUSD = token.get('data').get('price')
            self.priceBNB = token.get('data').get('price_BNB')
            self.save()
            return self
        except:
            return self