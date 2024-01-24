from pandas import *
import sqlalchemy
import time
import requests
import json
from threads import *

def give_details(outletapikey):
	'''
	gives the shop name and access token of it
	'''
	url=" https://api.demo.xircls.in/utility/api/v1/get_shopname_access_token/"
	headers = {'api-key': outletapikey, 'Content-Type': 'application/json'}
	response = requests.request("POST", url, headers=headers)
	# print("===========>response",response)
	data=response.json()
	shop=data["response"]["shop"]
	access=data["response"]["access_token"]
	print("=============>access======>",access,shop)
	return shop,access



dates=date_range(start="2023-11-28",end="2023-11-30")

user = 'root'
password = 'root'
host = '127.0.0.1'
port = 3306

database = 'shops_insights'
engine=sqlalchemy.create_engine(
		url=f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)


outletapikey="KwbxBMaHmIQ2WXHq4E4t3guJ7uYczUiJsEcxsi6ZkmE="
# outletapikey="Fv14sMRkz8uYqd3VMbKy5U+7h6QE4Rcb7MeG1d/PoXU="
# outletapikey=request.headers.get('outletapikey')
print("=============>outletapikey",outletapikey)

shop,access=give_details(outletapikey)

url = f"https://{shop}/admin/api/2023-07/graphql.json"
newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}

#gives the shop and access token


# cursor=request.POST.get('cursor')
# startdate=request.POST.get('startdate')
# enddate=request.POST.get('enddate')
# next_page=request.POST.get('next_page')
for date in dates:
    date=str(date).split()[0]
    print(str(date))
    startdate=f"{date}"

    enddate=f"{date}"

    startdate_q=startdate+'T00:00:00Z' 
    enddate=enddate+'T23:59:59Z' 
    sleep(1)
    filterq=f"created_at:>='{startdate_q}' AND created_at:<='{enddate}'"
    
   
    filtercount=f"&created_at_min={startdate}&created_at_max={enddate}"
 
    urlcount = f"https://{shop}/admin/api/2023-10/orders/count.json?status=any{filtercount}"
    print("==================================================")
    datacount = json.loads(requests.get(urlcount, headers=newheaders).text)

    urlcount_for_customers = f"https://{shop}/admin/api/2023-10/customers/count.json?status=any{filtercount}"
    # newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}
    datacount_for_customers = json.loads(requests.get(urlcount_for_customers, headers=newheaders).text)

    data={
        'datacount':datacount['count'],
        'datacount_for_customers':datacount_for_customers['count']


    }
    print("==================================================")

    insight_thread=InsightsThread(filterq,shop,newheaders)
    products_thread=ProductsThread(filterq,shop,newheaders)
    return_products_thread=ReturnProductsThread(filterq,shop,newheaders)
    channels_thread=ChannelsThread(filterq,shop,newheaders)

    print("================================= created thread objects ========================")
    insight_thread.start()
    # insight_thread.join()
    products_thread.start()
    insight_thread.join()
    products_thread.join()
    return_products_thread.start()
    # return_products_thread.join()
    channels_thread.start()
    channels_thread.join()
    return_products_thread.join()

    print("======================= all threads started =======================")

    # insight_thread.join()
    # products_thread.join()
    # return_products_thread.join()
    # channels_thread.join()

    print("====================== all threads ended ==========================")

    data.update(insight_thread.data)
    insights_df=DataFrame([data])
    insights_df['date']=startdate

    products_df=products_thread.df
    products_df['date']=startdate

    # print(insights_df.columns)
    # print(products_df)

    return_products_df=return_products_thread.df
    return_products_df['date']=startdate

    # print(return_products_df)
    channels_df=channels_thread.df
    channels_df['date']=startdate
    # print(channels_df)


    shop_of_sql=shop.split(".")[0].replace("-",'')
    print(shop_of_sql)
    
    insights_df.to_sql(
    name=f'{shop_of_sql}insights',
    con=engine,
    index=False,
    if_exists='append'
            )

    products_df.to_sql(
    name=f'{shop_of_sql}top_products',
    con=engine,
    index=False,
    if_exists='append'
        )

    return_products_df.to_sql(
    name=f'{shop_of_sql}top_return_products',
    con=engine,
    index=False,
    if_exists='append',

        )

    channels_df.to_sql(
    name=f'{shop_of_sql}top_channels',
    con=engine,
    index=False,
    if_exists='append'
    )
    print("\n\n======================================================\ndone for ",date,"\n================================")
    # sleep(5)
    
