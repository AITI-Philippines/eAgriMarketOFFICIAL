from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import admin

class Dealer(models.Model):
    user = models.OneToOneField(User, related_name="user")
    dealer_name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.dealer_name

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_price = models.FloatField()
    dealer = models.ForeignKey( Dealer, related_name="dealer" )
    def __unicode__(self):
        return self.item_name

class ItemGroup(models.Model):
    item = models.ForeignKey(Item, related_name="item")
    quantity = models.IntegerField()
    def __unicode__(self):
        return "%s x%s" % ( self.item, self.quantity)

class Cart(models.Model):
	name = models.CharField(max_length=100)
	owner = models.ForeignKey( Dealer, related_name="owner")
	items = models.ManyToManyField(ItemGroup, related_name="items", null=True)
	def __unicode__(self):
		return "%s" % ( self.name )
    
class Transaction(models.Model):
    buyer = models.ForeignKey( Dealer, related_name="buyer" )
    seller = models.ForeignKey( Dealer, related_name="seller" )
    transaction_date = models.DateField()
    cart = models.ForeignKey(Cart, related_name="cart")
    def save(self, *args, **kwargs):
        if self.buyer != self.seller:
            super(Transaction, self).save(*args, **kwargs)
        else:
            raise ValidationError("Error")
 
admin.site.register(Transaction)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(ItemGroup)
admin.site.register(Dealer)