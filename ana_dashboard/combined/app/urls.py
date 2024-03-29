from .views import *
from django.urls import path,include

urlpatterns = [
    # path('alltimesales/',alltimessales,name='alltimesales'),
    # path('mycustomers/',mycustomers,name='mycustomers'),
    # path('averageordervalue/',averageordervalue,name='averageordervalue'),
    # path('returnrate/',returnrate,name='returnrate'),
    # path('datacount/',datacount,name='datacount'),
    # path('healthsegmentation/',healthsegmentation,name='healthsegmentation'),

    # path("monthlycohorts/",monthlycohorts,name='monthlycohorts'),
    # path('return_customer_rate/',return_customer_rate,name='return_customer_rate'),
    # ##################################################################
    # path('giveinsights/',give_insights,name='give_insights'),
    # path('aov_rr_rcr/',give_aov_rr_rcr,name='give_aov_rr'),
    
    # path('top_products/',top_products,name='top_products'),
    # path('top_channels/',top_channels,name='top_channels'),
    # path('top_return_products/',top_return_products,name='top_return_products'),
    # path('all_in_one/',all_in_one,name='all_in_one'),
    # path('give_analytics/',give_analytics,name='give_analytics'),
    # path('all_in_one/',all_in_one,name='all_in_one'),
    
    # path('return_customer_rate/',return_customer_rate,name='return_customer_rate'),
    
    ################# main daily apis #############################
    
    path('daily/top_channels/',daily_top_channels,name='daily_top_channels'),
    path('daily/top_return_products/',daily_top_return_products,name='daily_top_return_products'),
    path('daily/aov_rr_rcr/',daily_give_aov_rr_rcr,name='daily_give_aov_rr_rcr'),
    path('daily/top_products/',daily_top_products,name='daily_top_products'),
    
    ######################### custom week month api #####################
    path('give_analytics/',give_analytics,name='give_analytics'),
    #######################################################################

    
]
