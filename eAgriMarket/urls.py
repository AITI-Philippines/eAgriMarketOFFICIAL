from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from ourWebApp.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', home, {'template_name':'homepage.html'}),
    # url(r'^eAgriMarket/', include('eAgriMarket.foo.urls')),
    # url(r'^([a-zA-Z0-9]+)$', show_profile, {'template_name':'profile_page.html'}),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    #pages
    url(r'^sign_up/$', signUp, {'template_name':'sign_up.html'}),
    url(r'^profile/([a-zA-Z0-9]+)', profile, {'template_name':'profile.html'}),
    url(r'^profile/$', myprofile, {'template_name':'profile.html'}),
    url(r'^search/', search, {'template_name':'results.html'}),
    url(r'^log_out/', logout ),
    url(r'^my_store/', mystore, {'template_name':'my_store.html'} ),
	url(r'^removeitem/(\d+)$', removeitem, {'template_name':'profile.html'} ),
	url(r'^my_carts/$', mycarts, {'template_name':'my_carts.html'} ),
	#url(r'^buy/(\d+)$', createBuyForm, {'template_name':'buyfo
    url(r'^my_transactions/', mytransactions, {'template_name':'my_transactions.html'} ),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
