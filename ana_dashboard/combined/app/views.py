from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import datetime as dt
import pandas as pd
import numpy as np
import json
import datetime as dt
import requests
from time import time
from .threads import *
from rest_framework.status import *
from rest_framework.decorators import api_view
import sqlalchemy

user = 'root'
password = 'root'
host = '127.0.0.1'
port = 3306
database = 'shops_insights'
engine=sqlalchemy.create_engine(
		url=f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)

#gives the shop and access token
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

def give_data(url,newheaders, payload):
	response = requests.request("POST", url, headers=newheaders, json=payload)
	data=response.json()["data"]["orders"]
	next_page=str(data["pageInfo"]["hasNextPage"])
	cursor=str(data["pageInfo"]["endCursor"])
	return data,next_page,cursor

# def give_payload(graphql_query,filterq,cursor=''):
	# variables = {
    # 	"filterq": filterq
	# 	}

	# # JSON payload including the query and variables
	# payload = {
	# 	"query": graphql_query,
	# 	"variables": variables
	# }

	# return payload


def give_graphql_query_for_while(filterq,cursor):
    graphql_query = """
        query MyQuery($cursor: String, $filterq: String) {
          orders(after: $cursor, first: 250, query: $filterq) {
            edges {
              cursor
              node {
                totalPrice
                createdAt
                currentSubtotalLineItemsQuantity
                subtotalLineItemsQuantity
				email
              }
            }
            pageInfo {
              endCursor
              hasNextPage
            }
          }
        }
        """
        
    # # Your cursor and filterq variables
    # cursor = "your_cursor_value"  # Replace with the actual cursor value
    # filterq = "your_filterq_value"  # Replace with the actual filterq value
    
    # Variables as a dictionary
    variables = {
        "cursor": cursor,
        "filterq": filterq
    }
    
    # JSON payload including the query and variables
    payload = {
        "query": graphql_query,
        "variables": variables
    }

    return payload


# def salesalltime(request,datacount,filterq,shop,newheaders):
# 	url = f"https://{shop}/admin/api/2023-07/graphql.json"

# 	cursor=''
# 	graphql_query = """ 
# 				query MyQuery($filter: String) {
# 				orders(
# 					reverse: true
# 					first: 25
# 					query: $filter
# 				) {
# 					edges {
# 					cursor
# 					node {
# 						name
# 						createdAt
# 						displayFinancialStatus
# 						displayFulfillmentStatus
# 						totalPrice
# 						email
# 						subtotalPrice
# 						customer {
# 						addresses {
# 							country
# 							province
# 							city
# 							lastName
# 							firstName
# 						}
# 						}
# 						totalDiscounts
# 						fulfillments(first: 10) {
# 						createdAt
# 						}
# 						discountApplications(first: 10) {
# 						edges {
# 							cursor
# 							node {
# 							value {
# 								... on PricingPercentageValue {
# 								__typename
# 								percentage
# 								}
# 								... on MoneyV2 {
# 								__typename
# 								amount
# 								}
# 							}
# 							}
# 						}
# 						}
# 						shippingAddress {
# 						city
# 						country
# 						province
# 						}
# 						customer {
# 						addresses {
# 							country
# 							province
# 							city
# 						}
# 						displayName
# 						}
# 						currencyCode
# 						discountCode
# 					}
# 					}
# 					pageInfo {
# 					endCursor
# 					hasNextPage
# 					}
# 				}
# 				}
# 				"""
# 	variables = {
# 		"filter": filterq
# 	}

# 	# JSON payload including the query and variables
# 	payload = {
# 		"query": graphql_query,
# 		"variables": variables
# 	}

# 	response = requests.request("POST", url, headers=newheaders, json=payload)
# 	data=json.loads(response.text)["data"]["orders"]
# 	if data["edges"]!=[]:
# 		next_page =str(data["pageInfo"]["hasNextPage"])
# 		cursor=str(data["pageInfo"]["endCursor"])
# 		rlocation=[request.GET.get('location') if request.GET.get('location') not in [None,''] else True][0]
# 		dic=[]
# 		for i in data["edges"]:
# 			data=i["node"]
# 			if data["customer"] not in [None,{}] and 'addresses' in data["customer"].keys() and data["customer"]['addresses'] not in [None,{}] and rlocation!=True:location=data["customer"]["addresses"][0]["country"]
# 			else:location=True
# 			if rlocation==location :
# 				d=dict()
# 				d['created_at'],d['currency'],d["current_subtotal_price"],d["current_total_discounts"],d["current_total_price"],d["email"],d["financial_status"],d["fulfillment_status"],d["order_number"]=data['createdAt'],data['currencyCode'],data["subtotalPrice"],data["totalDiscounts"],data["totalPrice"],data["email"],data["displayFinancialStatus"],data["displayFulfillmentStatus"],data["name"]
# 				if data["customer"] not in [None,{}] and 'addresses' in data["customer"].keys() and data["customer"]['addresses'] not in [None,{}]:d["customer"]=[data["customer"]["addresses"][0]]
# 				if data["discountApplications"]["edges"] not in [[],None]:
# 					value=data["discountApplications"]["edges"][0]["node"]["value"]
# 					d["value"],d["value_type"]=value["amount"]  if 'amount' in value.keys() else value["percentage"],value["__typename"]
# 					d['code']=data["discountCode"]
# 				if data["shippingAddress"] not in [{},None]:d["shipping_address"]=[data["shippingAddress"]]
# 				d["timetofulfill"]=(dt.datetime.strptime(data["fulfillments"][0]["createdAt"],"%Y-%m-%dT%H:%M:%SZ")-dt.datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ")).days if data["fulfillments"]!=[] else 'unfulfilled'
# 				dic.append(d)
# 		alltime_sales_data={'orders':dic,'next_page':next_page,'cursor':cursor,'count':datacount['count']}
# 	else:
# 		alltime_sales_data={'orders':[],'next_page':'False','cursor':"",'count':datacount['count']}
# 	# print("alltime sales data=>",alltime_sales_data)
# 	return alltime_sales_data

# def customers(request,datacount,filterq,shop,newheaders):
# 	url = f"https://{shop}/admin/api/2023-07/graphql.json"
# 	payload = "{\"query\":\"query MyQuery {\\n  customers(reverse: true, \\n    query: \\\"%s\\\"\\n first: 25) {\\n    edges {\\n      cursor\\n      node {\\n        acceptsMarketing\\n        createdAt\\n        email\\n        displayName\\n              numberOfOrders\\n        addresses {\\n          country\\n          city\\n          province\\n        }\\n        amountSpent {\\n          amount\\n        }\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n   \\n  }\\n}\",\"variables\":{}}"%(filterq)

# 	response = requests.request("POST", url, headers=newheaders, data=payload)
# 	data=json.loads(response.text)['data']['customers']
# 	cursor=str(data["pageInfo"]["endCursor"])
# 	next_page=str(data["pageInfo"]["hasNextPage"])
# 	if data["edges"]!=[]:
# 		#cursor=str(data["pageInfo"]["endCursor"])
# 		cust=[]
# 		for i in data["edges"]:
# 			custdata={}
# 			custdata['email'],custdata['name'],custdata['created_at'],custdata['accept_email_marketing'],custdata['orders_count'],custdata['total_spent'],custdata['country'],custdata['average_order_value']=i["node"]['email'],i["node"]['displayName'],i["node"]["createdAt"],i["node"]['acceptsMarketing'],i["node"]['numberOfOrders'],float(i["node"]['amountSpent']['amount']),i["node"]['addresses'][0]['country'] if i["node"]['addresses']!=[] else None,[round(float(i["node"]['amountSpent']['amount'])/int(i['node']['numberOfOrders']),2) if int(i['node']['numberOfOrders'])!=0 else 0][0]
# 			cust.append(custdata)
# 		data={'data':cust,'next_page':next_page,'cursor':cursor,'count':datacount["count"]}
# 	else:
# 		data={'data':[],'next_page':'False','cursor':'','count':datacount["count"]} 
	
# 	return data

@csrf_exempt
def give_insights(request):
	if request.method=='POST':
		cursor=request.POST.get('cursor')
		startdate=request.POST.get('startdate')
		enddate=request.POST.get('enddate')
		next_page=request.POST.get('next_page')
		
		# =request.POST.get('cursor'),request.POST.get('startdate'),request.POST.get('enddate')
		startdate=startdate+'T00:00:00Z' 
		enddate=enddate+'T23:59:59Z' 
		# print(startdate,enddate)

		filterq=f"created_at:>='{startdate}' AND created_at:<='{enddate}'"
		outletapikey=request.headers.get('outletapikey')
		print("=============>outletapikey",outletapikey)

		shop,access=give_details(outletapikey)
		newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}
		filtercount=f"&created_at_min={startdate}&created_at_max={enddate}"
		urlcount = f"https://{shop}/admin/api/2023-10/orders/count.json?status=any{filtercount}"
		datacount = json.loads(requests.get(urlcount, headers=newheaders).text)

		url = f"https://{shop}/admin/api/2023-07/graphql.json"
		# alltime_sales_data=salesalltime(request,datacount,filterq,shop,newheaders)


		


		# customers api
		urlcount_for_customers = f"https://{shop}/admin/api/2023-10/customers/count.json?status=any{filtercount}"
		# newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}
		datacount_for_customers = json.loads(requests.get(urlcount_for_customers, headers=newheaders).text)
		# cutomers_data=customers(request,datacount,filterq,shop,newheaders)

		s_t=SalesThread(request,datacount,filterq,shop,newheaders)
		c_t=CustomerThread(request,datacount_for_customers,filterq,shop,newheaders)
		s_t.start()
		c_t.start()
		s_t.join()
		c_t.join()
		alltime_sales_data=s_t.data
		cutomers_data=c_t.data
  
		data={
			'datacount':datacount['count'],
			'datacount_for_customers':datacount_for_customers['count']
		}
		# df=pd.DataFrame([data])
		# df.to_csv("insights.csv",index=False
            
            # )
		# print(len(dic))
		return JsonResponse(data=data,
                      status=200
			)



@csrf_exempt
def give_aov_rr_rcr(request):
	if request.method=='POST':
		try:
			# st=time()
			startdate,enddate=request.POST.get('startdate'),request.POST.get('enddate')
			startdate=startdate+'T00:00:00Z' 
			enddate=enddate+'T23:59:59Z' 
			outletapikey=request.headers.get('outletapikey')
			filterq=f"created_at:>='{startdate}' AND created_at:<='{enddate}'" 
			shop,access=give_details(outletapikey)
			url = f"https://{shop}/admin/api/2023-10/graphql.json"
			newheaders = {
			'X-Shopify-Access-Token':access,
			'Content-Type': 'application/json'
			}

			
			graphql_query = """
			query MyQuery($filterq: String) {
			orders(query: $filterq, first: 250) {
				edges {
				cursor
				node {
					totalPrice
					createdAt
					currentSubtotalLineItemsQuantity
					subtotalLineItemsQuantity
					email
				}
				}
				pageInfo {
				endCursor
				hasNextPage
				}
			}
			}
			"""

			variables = {
				"filterq": filterq
			}

			# JSON payload including the query and variables
			payload = {
				"query": graphql_query,
				"variables": variables
			}

			response = requests.request("POST", url, headers=newheaders, json=payload)
			data=json.loads(response.text)["data"]["orders"]
			next_page =str(data["pageInfo"]["hasNextPage"])
			cursor=str(data["pageInfo"]["endCursor"])
			df=pd.json_normalize(data['edges'])

			while next_page == "True":
				print(69)
				payload=give_graphql_query_for_while(filterq,cursor)
				response = requests.request("POST", url, headers=newheaders, json=payload)
				data=json.loads(response.text)["data"]["orders"]
				next_page=str(data["pageInfo"]["hasNextPage"])
				cursor=str(data["pageInfo"]["endCursor"])
				df1=pd.json_normalize(data['edges'])
				df=pd.concat([df,df1],axis=0)

			total_quantity=int(df['node.currentSubtotalLineItemsQuantity'].sum())
			total_price=round(df['node.totalPrice'].astype('float').sum(),2)
			total_order=int(len(df)) 
			total_return_quantity=sum(df["node.subtotalLineItemsQuantity"].astype(float)-df["node.currentSubtotalLineItemsQuantity"].astype(float))
			return_rate=round((total_return_quantity/total_quantity)*100,2)
			average_order_value=round(total_price/total_order,2)
			average_units_ordered=round(total_quantity/total_order,2)
			unique_users=df['node.email'].nunique()
			returned_users=len(df[df['node.email'].duplicated()])
			return_customer_rate=round((returned_users*100/unique_users),2)

			data={
					
					'total_quantity':total_quantity,
					'total_price':total_price,
					'total_order':total_order,
					'total_return_quantity':total_return_quantity,
					'return_rate':return_rate,
					'average_order_value':average_order_value,
					'average_units_ordered':average_units_ordered,
					'return_customer_rate':return_customer_rate,
					'unique_users':unique_users,
					'returned_users':returned_users

				}
			# print(len(df))
			# print(len(df[df['node.email'].duplicated()])/len(df))
			# df=pd.DataFrame([data])
			# df.to_csv("insights1.csv",index=False)
			return JsonResponse(data=
				data.update({'mssg':'data processed successfully'}),
				safe=False,
				status=HTTP_200_OK
			)
		except:
			return JsonResponse(data=
				{
					'mssg':'Error occurred from shopify.com'
					# 'total_quantity':total_quantity,
					# 'total_price':total_price,
					# 'total_order':total_order,
					# 'total_return_quantity':total_return_quantity,
					# 'return_rate':return_rate,
					# 'average_order_value':average_order_value,
					# 'average_units_ordered':average_units_ordered

				},
				safe=False,
				status=HTTP_204_NO_CONTENT
			)


@api_view(['POST'])
@csrf_exempt
def top_products(request):
	st=time()
	cursor=request.POST.get('cursor')
	startdate=request.POST.get('startdate')
	enddate=request.POST.get('enddate')
	next_page=request.POST.get('next_page')
	
	# =request.POST.get('cursor'),request.POST.get('startdate'),request.POST.get('enddate')
	startdate_q=startdate+'T00:00:00Z' 
	enddate=enddate+'T23:59:59Z' 
	# print(startdate,enddate)

	filterq=f"created_at:>='{startdate_q}' AND created_at:<='{enddate}'"
	outletapikey=request.headers.get('outletapikey')
	print("=============>outletapikey",outletapikey)

	shop,access=give_details(outletapikey)

	url = f"https://{shop}/admin/api/2023-07/graphql.json"

	newheaders = {
		'X-Shopify-Access-Token': access,
		'Content-Type': 'application/json'
		}
	graphql_query = """
	query MyQuery($filter: String) {
	orders(first: 70, query: $filter) {
		edges {
		cursor
		node {
			createdAt
			lineItems (first: 10){
			edges {
				node {
				quantity
				title
				originalTotal
				variantTitle
				}
			}
			
			}
		}
		}
		pageInfo {
		endCursor
		hasNextPage
		}
	}
	}
	"""



	# Variables as a dictionary
	variables = {
		"filter": filterq
	}

	# JSON payload including the query and variables
	payload = {
		"query": graphql_query,
		"variables": variables
	}

	response = requests.request("POST", url, headers=newheaders, json=payload)
	data=json.loads(response.text)["data"]["orders"]
	next_page = "True"
	cursor=str(data["pageInfo"]["endCursor"])
	# print(data['edges'])
	df_inner=pd.json_normalize(data['edges'][0]['node']['lineItems']['edges'])
	for i in range(1,len(data['edges'])):
		df_inner1=pd.json_normalize(data['edges'][i]['node']['lineItems']['edges'])
		df_inner=pd.concat([df_inner,df_inner1],axis=0)
	df_list=[df_inner]

	while next_page == "True":
		print(69)
		graphql_query = """
				query MyQuery($cursor: String, $filterq: String) {
				orders(after: $cursor, first: 70, query: $filterq) {
					edges {
					cursor
					node {
						createdAt
						lineItems(first: 10) {
						edges {
							node {
							quantity
							title
							originalTotal
							variantTitle
							}
						}
						}
					}
					}
					pageInfo {
					endCursor
					hasNextPage
					}
				}
				}
				"""



	# Variables as a dictionary
		variables = {
			"cursor": cursor,
			"filterq": filterq
		}
		
		# JSON payload including the query and variables
		payload = {
			"query": graphql_query,
			"variables": variables
		}
	
		data,next_page,cursor=give_data(url,newheaders, payload)
		df_inner=pd.json_normalize(data['edges'][0]['node']['lineItems']['edges'])
		for i in range(1,len(data['edges'])):
			df_inner1=pd.json_normalize(data['edges'][i]['node']['lineItems']['edges'])
			df_inner=pd.concat([df_inner,df_inner1],axis=0)
		

		df_list.append(df_inner)

	df=pd.concat(df_list,axis=0)
	# df.to_csv("top_products.csv",index=False)
	df['node.originalTotal']=df['node.originalTotal'].apply(pd.to_numeric)
	df=df.groupby(by='node.title').sum()
	# df['date']=startdate
	# df.reset_index(inplace=True)
	# df.to_csv("top_products.csv",index=False)
	# top_products_by_total_price=list(df.sort_values('node.originalTotal',ascending=False).index[:10])
	# top_products_by_units_sold=list(df.sort_values('node.quantity',ascending=False).index[1:10])
	print(time()-st)
	return JsonResponse(
		data={
			# 'top_products_by_total_price':top_products_by_total_price,
			# 'top_products_by_units_sold':top_products_by_units_sold
			'mssg':'done'
		},
		status=200
	)

from time import sleep

@api_view(['POST'])
@csrf_exempt
def top_channels(request):
	st=time()
	cursor=request.POST.get('cursor')
	startdate=request.POST.get('startdate')
	enddate=request.POST.get('enddate')
	next_page=request.POST.get('next_page')
	
	# =request.POST.get('cursor'),request.POST.get('startdate'),request.POST.get('enddate')
	startdate=startdate+'T00:00:00Z' 
	enddate=enddate+'T23:59:59Z' 
	# print(startdate,enddate)

	filterq=f"created_at:>='{startdate}' AND created_at:<='{enddate}'"
	outletapikey=request.headers.get('outletapikey')
	print("=============>outletapikey",outletapikey)

	shop,access=give_details(outletapikey)

	url = f"https://{shop}/admin/api/2023-07/graphql.json"

	newheaders = {
		'X-Shopify-Access-Token': access,
		'Content-Type': 'application/json'
		}
	
	graphql_query = """
	query MyQuery($filter: String) {
		orders(first: 250, query: $filter) {
		edges {
			
			node {
			channel {
				name
			}
			createdAt
			currentSubtotalLineItemsQuantity
			totalDiscounts
			totalPrice
			totalRefunded
			totalShippingPrice
			totalTax
			totalWeight
			}
		}
		pageInfo {
			endCursor
			hasNextPage
		}
		}
	}	
	"""

	# Your string variable
	# filterq = "your_filter_value"  # Replace with the actual filter value

	# Variables as a dictionary
	variables = {
		"filter": filterq
	}

	# JSON payload including the query and variables
	payload = {
		"query": graphql_query,
		"variables": variables
	}
	response = requests.request("POST", url, headers=newheaders, json=payload)
	data=json.loads(response.text)["data"]["orders"]
	next_page = "True"
	cursor=str(data["pageInfo"]["endCursor"])

	df=pd.json_normalize(data['edges'])

	while next_page == "True":
		print(69)
		# payload = "{\"query\":\"query MyQuery {\\n  orders(after: \\\"%s\\\"\\n first: 27) {\\n    edges {\\n      cursor\\n      node {\\n        channel {\\n          name\\n        }\\n        createdAt\\n        currentSubtotalLineItemsQuantity\\n        totalDiscounts\\n        totalPrice\\n        totalRefunded\\n        totalShippingPrice\\n        totalTax\\n        totalWeight\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n  }\\n}\",\"variables\":{}}"%format(cursor)
		#payload = "{\"query\":\"query MyQuery {\\n  orders(after: \\\"%s\\\"\\n  first: 10) {\\n    edges {\\n      cursor\\n      node {\\n    createdAt \\n    lineItems(first: 10) {\\n          edges {\\n            node {\\n              name\\n              originalTotal\\n              sku\\n              currentQuantity\\n              quantity\\n              discountedTotal\\n              totalDiscount\\n            }\\n          }\\n        }\\n          }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n  }\\n}\",\"variables\":{}}"
		# GraphQL query
		graphql_query = """
		query MyQuery($filter: String, $cursor: String) {
		orders(
			after: $cursor,
			first: 250,
			query: $filter
		) {
			edges {
			cursor
			node {
				channel {
				name
				}
				createdAt
				currentSubtotalLineItemsQuantity
				totalDiscounts
				totalPrice
				totalRefunded
				totalShippingPrice
				totalTax
				totalWeight
			}
			}
			pageInfo {
			endCursor
			hasNextPage
			}
		}
		}
		"""

		# Variables
		variables = {
			"filter": filterq,
			"cursor": cursor
		}
		
		# Payload
		payload = {
			"query": graphql_query,
			"variables": variables
		}
		

		response = requests.request("POST", url, headers=newheaders, json=payload)
		#print(json.loads(response.text))
		data=json.loads(response.text)["data"]["orders"]
		next_page = str(data["pageInfo"]["hasNextPage"])
		cursor=str(data["pageInfo"]["endCursor"])
		df1=pd.json_normalize(data['edges'])
		df=pd.concat([df,df1],axis=0)

	df['node.channel.name'].fillna("Not available",inplace=True)
	df_counted=df['node.channel.name'].value_counts()
	counts=df_counted.values
	variants=list(df_counted.index)
	print(counts)
	print(variants)
	zipped_data=dict(zip(variants,counts))
	print(zipped_data)
	df=pd.DataFrame(zipped_data.items(),columns=['channel_name','sold_quantity'])
	# df.to_csv("top_channels.csv",index=False)
	print(df)

	return JsonResponse(
		data={
			'top_products_by_channels':'zipped_data'
		}
	)


@api_view(['POST'])
@csrf_exempt
def top_return_products(request):

	st=time()
	cursor=request.POST.get('cursor')
	startdate=request.POST.get('startdate')
	enddate=request.POST.get('enddate')
	next_page=request.POST.get('next_page')
	
	# =request.POST.get('cursor'),request.POST.get('startdate'),request.POST.get('enddate')
	startdate_q=startdate+'T00:00:00Z' 
	enddate=enddate+'T23:59:59Z' 
	# print(startdate,enddate)

	filterq=f"created_at:>='{startdate_q}' AND created_at:<='{enddate}'"
	outletapikey=request.headers.get('outletapikey')
	print("=============>outletapikey",outletapikey)

	shop,access=give_details(outletapikey)

	url = f"https://{shop}/admin/api/2023-07/graphql.json"

	newheaders = {
		'X-Shopify-Access-Token': access,
		'Content-Type': 'application/json'
		}
	
	# graphql_query = """
	# query MyQuery($filter: String) {
	# orders(first: 76, query: $filter) {
	# 	edges {
		
	# 	node {
	# 		createdAt
	# 		returnStatus
	# 		name
	# 		lineItems(first: 10) {
	# 		edges {
				
	# 			node {
	# 			name
	# 			currentQuantity
    #             quantity
				
			
	# 			}
	# 		}
			
	# 		}
	# 	}
	# 	}
	# 	pageInfo {
	# 	endCursor
	# 	hasNextPage
	# 	}
	# }
	# }
	# """

	# variables = {
	# 	"filter": filterq
	# }
	# payload = {
	# 	"query": graphql_query, 
	# 	"variables": variables
	# }
	
	# response = requests.request("POST", url, headers=newheaders, json=payload)
	# data=json.loads(response.text)["data"]["orders"]
	# next_page = "True"
	# cursor=str(data["pageInfo"]["endCursor"])
	# # print(data['edges'])

	# edges=data['edges'][0]['node']['lineItems']['edges']
	# # dummy_return_list=[data['edges'][0]['node']['returnStatus']]*len(edges)
	# df_inner=pd.json_normalize(edges)
	# # return_list=return_list+dummy_return_list
	# for i in range(1,len(data['edges'])):
	# 	# return_list.append(data['edges'][i]['node']['returnStatus'])
		
	# 	edges=data['edges'][i]['node']['lineItems']['edges']
	# 	# dummy_return_list=[data['edges'][i]['node']['returnStatus']]*len(edges)
	# 	# return_list=return_list+dummy_return_list
	# 	df_inner1=pd.json_normalize(edges)
	# 	df_inner=pd.concat([df_inner,df_inner1],axis=0,ignore_index=True)


	# print(df_inner)
	# df_list=[df_inner]

	# while next_page == "True":
	# 	print(69)
	# #payload = "{\"query\":\"query MyQuery {\\n  orders( first: 10) {\\n    edges {\\n      cursor\\n      node {\\n        lineItems(first: 10) {\\n          edges {\\n            node {\\n              quantity\\n              title\\n              originalTotal\\n  variantTitle\\n           }\\n          }\\n        }\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n  }\\n}\",\"variables\":{}}"
	# # 

	# 	graphql_query = """
	# 	query MyQuery($filter: String, $cursor: String) {
	# 	orders(first: 76, query: $filter, after: $cursor) {
		
	# 		edges {
			
	# 		node {
	# 			createdAt
	# 			returnStatus
	# 			name
	# 			lineItems(first: 10) {
	# 			edges {
					
	# 				node {
	# 				name
	# 				currentQuantity
	# 				quantity
			
					
				
	# 				}
	# 			}
				
	# 			}
	# 		}
	# 		}
			
	# 		pageInfo {
	# 		endCursor
	# 		hasNextPage
	# 		}
	# 	}
	# 	}
	# 	"""
		
	# 	variables = {"filter": filterq, "cursor": cursor}
	# 	payload = {"query": graphql_query, "variables": variables}



		
	# 	response = requests.request("POST", url, headers=newheaders, json=payload)
	# 	data=json.loads(response.text)["data"]["orders"]
	# 	next_page=str(data["pageInfo"]["hasNextPage"])
	# 	cursor=str(data["pageInfo"]["endCursor"])

	# 	edges=data['edges'][0]['node']['lineItems']['edges']
	# 	# dummy_return_list=[data['edges'][0]['node']['returnStatus']]*len(edges)
	# 	df_inner=pd.json_normalize(edges)
	# 	# return_list=return_list+dummy_return_list
		
	# 	for i in range(1,len(data['edges'])):
	# 		# return_list.append(data['edges'][i]['node']['returnStatus'])
			
	# 		edges=data['edges'][i]['node']['lineItems']['edges']
	# 		# dummy_return_list=[data['edges'][i]['node']['returnStatus']]*len(edges)
	# 		# return_list=return_list+dummy_return_list
	# 		df_inner1=pd.json_normalize(edges)
	# 		df_inner=pd.concat([df_inner,df_inner1],axis=0,ignore_index=True)

	# 	df_list.append(df_inner)
		

	# df_final=pd.concat(df_list,axis=0,ignore_index=True)

	# df_final.fillna({
	# 	'node.currentQuantity':0,
	# 	'node.quantity':0
	# },inplace=True)

	# df_final=df_final[   df_final['node.currentQuantity'] < df_final['node.quantity'] ]
	# df_final['diff']=df_final['node.quantity']-df_final['node.currentQuantity']
	# # print(df_final.head(20))
	# # df_final=df_final[df_final['diff']>0]
	# df_ret_products=df_final.groupby('node.name').sum()
	# print(df_ret_products)
	# print("=========================================")
	# df_ret_products['date']=startdate
	# df_ret_products.reset_index(inplace=True)
	# # df.to_csv("top_return_products.csv",index=False)
	# # print(df)
	# df_ret_products.rename(
    # columns={
    #     'node.name':'name',
    #     'diff':'return_quantity'
    # },
    # inplace=True
	# 		)
	# df_ret_products.drop(columns=['node.currentQuantity','node.quantity'],inplace=True)
	# print(df_ret_products)
	# # print(df.head())
	# # print(df.sort_values('diff',ascending=False).tail())
	# # print(df.shape)
	# # return_products=list(df.sort_values('diff',ascending=False).index[1:10])
	# # print(return_products)
	return_products_thread=ReturnProductsThread(filterq,shop,newheaders)
	return_products_thread.start()
	return_products_thread.join()
	 
	return_products_df=return_products_thread.df
	return_products_df['date']=startdate
	return JsonResponse(
		data={
			"data":'done'
			# "data":return_products
		},
		status=200
	)

@api_view(['POST'])
@csrf_exempt
def all_in_one(request):
	# cursor=request.POST.get('cursor')
	startdate=request.POST.get('startdate')
	enddate=request.POST.get('enddate')
	# next_page=request.POST.get('next_page')

	startdate_q=startdate+'T00:00:00Z' 
	enddate=enddate+'T23:59:59Z' 

	filterq=f"created_at:>='{startdate_q}' AND created_at:<='{enddate}'"
	outletapikey=request.headers.get('outletapikey')
	print("=============>outletapikey",outletapikey)

	shop,access=give_details(outletapikey)

	url = f"https://{shop}/admin/api/2023-07/graphql.json"
 
	filtercount=f"&created_at_min={startdate}&created_at_max={enddate}"
	newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}
	urlcount = f"https://{shop}/admin/api/2023-10/orders/count.json?status=any{filtercount}"
	datacount = json.loads(requests.get(urlcount, headers=newheaders).text)
 
	urlcount_for_customers = f"https://{shop}/admin/api/2023-10/customers/count.json?status=any{filtercount}"
	# newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}
	datacount_for_customers = json.loads(requests.get(urlcount_for_customers, headers=newheaders).text)
 
	data={
		'datacount':datacount['count'],
  		'datacount_for_customers':datacount_for_customers['count']
    
  
	}
 
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
	insights_df=pd.DataFrame([data])
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
 
	
	shop=shop.split(".")[0].replace("-",'')
	print(shop)
	insights_df.to_sql(
    name=f'{shop}insights',
    con=engine,
    index=False,
    if_exists='append'
			)
	
	products_df.to_sql(
    name=f'{shop}top_products',
    con=engine,
    index=False,
    if_exists='append'
		)
 
	return_products_df.to_sql(
    name=f'{shop}top_return_products',
    con=engine,
    index=False,
    if_exists='append',
    
		)
 
	channels_df.to_sql(
    name=f'{shop}top_channels',
    con=engine,
    index=False,
    if_exists='append'
    )
 
	
 
	return JsonResponse(
		data=data,
		safe=False,
		status=200
	)
 
 
 
 
# Dashboard main api for custom,weekly and monthly data
def give_data_from_sql(shop,startdate,enddate):
    
	df=pd.read_sql_query(
	f'''
	select 
	sum(datacount_for_customers) as a,
	sum(datacount) as b,
	sum(total_quantity) as c,
	sum(total_price) as d,
	sum(total_order) as e,
	sum(total_return_quantity) as f,
	sum(unique_users) as g,
	sum(returned_users) as h
	from
	{shop}insights
	where date between "{startdate}" and "{enddate}"
	;
	''',
	engine

	)
	insights={
	'total_quantity':df.loc[0].c,
	'total_price':df.loc[0].d,
	'total_order':df.loc[0].e,
	'total_return_quantity':df.loc[0].f,
	'return_rate':round((df.loc[0].f/df.loc[0].c)*100,2),
	'average_order_value':round(df.loc[0].d/df.loc[0].e,2),
	'average_units_ordered':round(df.loc[0].c/df.loc[0].e,2),
	'return_customer_rate':round((df.loc[0].h*100)/df.loc[0].g,2),
	'returned_users':df.loc[0].h,
	'unique_users':df.loc[0].g

	}
	
	df=pd.read_sql_query(
	f'''
		select name,sum(quantity) as total_quantity,
		sum(total_price) as total_price
		from {shop}top_products where date between "{startdate}" and "{enddate}" and name not like "Free%"
		group by name
		;
		''',
		engine
	)

	top_products_by_quantity=list(df.sort_values('total_quantity',ascending=False).name[:10])
	top_products_by_total_price=list(df.sort_values('total_price',ascending=False).name[:10])

	df=pd.read_sql_query(
	'''
	select name ,sum(return_quantity) as total_return_quantity
	from bombayshavingtop_return_products
	where date between "2024-01-16" and "2024-01-18" and name not like "%Free%"
	group by name
	order by total_return_quantity desc
	limit 10;
	''',
	engine
			)

	top_return_products=list(df.name)


	df=pd.read_sql_query(
	f'''
	select channel_name,sum(sold_quantity) as total_quantity
	from {shop}top_channels 
	where date between "{startdate}" and "{enddate}"
	group by channel_name
	order by total_quantity ;
	''',
	engine
	)
	top_channels=list(df.channel_name)

	data={
		'insights':insights,
		'top_products_by_quantity':top_products_by_quantity,
		'top_products_by_total_price':top_products_by_total_price,
		'top_return_products':top_return_products,
		'top_channels':top_channels
	}
	return data
       
    
@api_view(['POST'])
@csrf_exempt
def give_analytics(request):
	startdate=request.POST.get('startdate')
	enddate=request.POST.get('enddate')
	outletapikey=request.headers.get('outletapikey')
	print("=============>outletapikey",outletapikey)

	shop,access=give_details(outletapikey)
	shop=shop.split(".")[0].replace("-",'')
	print(shop)

	
	data=give_data_from_sql(shop,startdate,enddate)
	
	return JsonResponse(
		data=data,
		safe=False,
		status=200
	)
###############################################################
	


 

 
	
 
	

		










# ###### shopify order GraphQL Api ####   ==>DONE
# @csrf_protect
# @csrf_exempt
# def alltimessales(request):
# 	st=time()
# 	if request.method=='POST':
# 		# print("=-=============>ewfesfsf",request.GET)
# 		if request.POST.get('next_page')=="True":
# 			cursor,startdate,enddate=request.POST.get('cursor'),request.POST.get('startdate'),request.POST.get('enddate')
# 			startdate=startdate+'T00:00:00Z' if startdate not in['',None] else startdate
# 			enddate=enddate+'T23:59:59Z' if enddate not in['',None] else enddate
# 			outletapikey=request.headers.get('outletapikey')
# 			print("=============>outletapikey",outletapikey)
# 			filterq=f"created_at:>='{startdate}' AND created_at:<='{enddate}'" if startdate not in['',None] and enddate not in['',None] else ''
# 			filtercount=f"&created_at_min={startdate}&created_at_max={enddate}" if startdate not in['',None] and enddate not in ['',None] else ''
# 			# url=" https://api.demo.xircls.in/utility/api/v1/get_shopname_access_token/"
# 			# headers = {'api-key': outletapikey, 'Content-Type': 'application/json'}
# 			# response = requests.request("POST", url, headers=headers)
# 			# print("===========>response",response)
# 			# data=json.loads(response.text)
# 			# shop=data["response"]["shop"]
# 			# access=data["response"]["access_token"]
# 			shop,access=give_details(outletapikey)
# 			print("=============>access======>",access,shop)
# 			urlcount = f"https://{shop}/admin/api/2023-10/orders/count.json?status=any{filtercount}"
# 			newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}
# 			datacount = json.loads(requests.get(urlcount, headers=newheaders).text)         
# 			url = f"https://{shop}/admin/api/2023-07/graphql.json"
# 			if cursor in ['',None]:
# 				# payload = """{\"query\":\"query MyQuery {\\n  orders(reverse:true,\\n    query: \\\"%s\\\"\\n   first: 25 ) {\\n    edges {\\n      cursor\\n      node {\\n        name\\n   createdAt\\n    displayFinancialStatus\\n   displayFulfillmentStatus\\n     totalPrice\\n        email\\n        subtotalPrice\\n  customer {\\n          addresses {\\n            country\\n            province\\n            city\\n  lastName\\n  firstName\\n       }\\n                }\\n      totalDiscounts\\n        fulfillments(first: 10) {\\n          createdAt\\n        }\\n        discountApplications(first: 10) {\\n          edges {\\n            cursor\\n            node {\\n              value {\\n                ... on PricingPercentageValue {\\n                  __typename\\n                  percentage\\n                }\\n                ... on MoneyV2 {\\n                  __typename\\n                  amount\\n                }\\n              }\\n            }\\n          }\\n        }\\n        shippingAddress {\\n          city\\n          country\\n          province\\n        }\\n        customer {\\n          addresses {\\n            country\\n            province\\n            city\\n          }\\n          displayName\\n        }\\n        currencyCode\\n        discountCode\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n  }\\n}\",\"variables\":{}}"""%(filterq)
# 				graphql_query = """
# 				query MyQuery($filter: String) {
# 				  orders(
# 					reverse: true
# 					query: $filter
# 					first: 25
# 				  ) {
# 					edges {
# 					  cursor
# 					  node {
# 						name
# 						createdAt
# 						displayFinancialStatus
# 						displayFulfillmentStatus
# 						totalPrice
# 						email
# 						subtotalPrice
# 						customer {
# 						  addresses {
# 							country
# 							province
# 							city
# 							lastName
# 							firstName
# 						  }
# 						}
# 						totalDiscounts
# 						fulfillments(first: 10) {
# 						  createdAt
# 						}
# 						discountApplications(first: 10) {
# 						  edges {
# 							cursor
# 							node {
# 							  value {
# 								... on PricingPercentageValue {
# 								  __typename
# 								  percentage
# 								}
# 								... on MoneyV2 {
# 								  __typename
# 								  amount
# 								}
# 							  }
# 							}
# 						  }
# 						}
# 						shippingAddress {
# 						  city
# 						  country
# 						  province
# 						}
# 						customer {
# 						  addresses {
# 							country
# 							province
# 							city
# 						  }
# 						  displayName
# 						}
# 						currencyCode
# 						discountCode
# 					  }
# 					}
# 					pageInfo {
# 					  endCursor
# 					  hasNextPage
# 					}
# 				  }
# 				}
# 				"""
# 				variables = {
# 					"filter": filterq
# 				}

# 				payload = {
# 				"query": graphql_query,
# 				"variables": variables
# 			}
# 			else:
# 				# payload = """{\"query\":\"query MyQuery {\\n  orders(reverse:true,\\n after: \\\"%s\\\"\\n  first: 25, query: \\\"%s\\\"\\n) {\\n    edges {\\n      cursor\\n      node {\\n        name\\n   createdAt\\n    displayFinancialStatus\\n   displayFulfillmentStatus\\n     totalPrice\\n        email\\n        subtotalPrice\\n  customer {\\n          addresses {\\n            country\\n            province\\n            city\\n  lastName\\n  firstName\\n       }\\n                }\\n      totalDiscounts\\n        fulfillments(first: 10) {\\n          createdAt\\n        }\\n        discountApplications(first: 10) {\\n          edges {\\n            cursor\\n            node {\\n              value {\\n                ... on PricingPercentageValue {\\n                  __typename\\n                  percentage\\n                }\\n                ... on MoneyV2 {\\n                  __typename\\n                  amount\\n                }\\n              }\\n            }\\n          }\\n        }\\n        shippingAddress {\\n          city\\n          country\\n          province\\n        }\\n        customer {\\n          addresses {\\n            country\\n            province\\n            city\\n          }\\n          displayName\\n        }\\n        currencyCode\\n        discountCode\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n  }\\n}\",\"variables\":{}}"""%(cursor,filterq)
# 				graphql_query = """ 
# 				  query MyQuery($cursor: String, $filter: String) {
# 					orders(
# 					  reverse: true
# 					  after: $cursor
# 					  first: 25
# 					  query: $filter
# 					) {
# 					  edges {
# 						cursor
# 						node {
# 						  name
# 						  createdAt
# 						  displayFinancialStatus
# 						  displayFulfillmentStatus
# 						  totalPrice
# 						  email
# 						  subtotalPrice
# 						  customer {
# 							addresses {
# 							  country
# 							  province
# 							  city
# 							  lastName
# 							  firstName
# 							}
# 						  }
# 						  totalDiscounts
# 						  fulfillments(first: 10) {
# 							createdAt
# 						  }
# 						  discountApplications(first: 10) {
# 							edges {
# 							  cursor
# 							  node {
# 								value {
# 								  ... on PricingPercentageValue {
# 									__typename
# 									percentage
# 								  }
# 								  ... on MoneyV2 {
# 									__typename
# 									amount
# 								  }
# 								}
# 							  }
# 							}
# 						  }
# 						  shippingAddress {
# 							city
# 							country
# 							province
# 						  }
# 						  customer {
# 							addresses {
# 							  country
# 							  province
# 							  city
# 							}
# 							displayName
# 						  }
# 						  currencyCode
# 						  discountCode
# 						}
# 					  }
# 					  pageInfo {
# 						endCursor
# 						hasNextPage
# 					  }
# 					}
# 				  }
# 				  """
# 				variables = {
# 					"cursor": cursor,
# 					"filter": filterq
# 				}

# 				# JSON payload including the query and variables
# 				payload = {
# 					"query": graphql_query,
# 					"variables": variables
# 				}


# 			newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}
# 			response = requests.request("POST", url, headers=newheaders, json=payload)
# 			data=json.loads(response.text)["data"]["orders"]
# 			if data["edges"]!=[]:
# 				next_page =str(data["pageInfo"]["hasNextPage"])
# 				cursor=str(data["pageInfo"]["endCursor"])
# 				rlocation=[request.GET.get('location') if request.GET.get('location') not in [None,''] else True][0]
# 				dic=[]
# 				for i in data["edges"]:
# 					data=i["node"]
# 					if data["customer"] not in [None,{}] and 'addresses' in data["customer"].keys() and data["customer"]['addresses'] not in [None,{}] and rlocation!=True:location=data["customer"]["addresses"][0]["country"]
# 					else:location=True
# 					if rlocation==location :
# 						d=dict()
# 						d['created_at'],d['currency'],d["current_subtotal_price"],d["current_total_discounts"],d["current_total_price"],d["email"],d["financial_status"],d["fulfillment_status"],d["order_number"]=data['createdAt'],data['currencyCode'],data["subtotalPrice"],data["totalDiscounts"],data["totalPrice"],data["email"],data["displayFinancialStatus"],data["displayFulfillmentStatus"],data["name"]
# 						if data["customer"] not in [None,{}] and 'addresses' in data["customer"].keys() and data["customer"]['addresses'] not in [None,{}]:d["customer"]=[data["customer"]["addresses"][0]]
# 						if data["discountApplications"]["edges"] not in [[],None]:
# 							value=data["discountApplications"]["edges"][0]["node"]["value"]
# 							d["value"],d["value_type"]=value["amount"]  if 'amount' in value.keys() else value["percentage"],value["__typename"]
# 							d['code']=data["discountCode"]
# 						if data["shippingAddress"] not in [{},None]:d["shipping_address"]=[data["shippingAddress"]]
# 						d["timetofulfill"]=(dt.datetime.strptime(data["fulfillments"][0]["createdAt"],"%Y-%m-%dT%H:%M:%SZ")-dt.datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ")).days if data["fulfillments"]!=[] else 'unfulfilled'
# 						dic.append(d)
# 				data={'orders':dic,'next_page':next_page,'cursor':cursor,'count':datacount['count']}
# 			else:
# 				data={'orders':[],'next_page':'False','cursor':"",'count':datacount['count']}
# 		else:
# 			data={'orders':[],'next_page':'False','cursor':"",'count':0}   
# 		print("time is  ",time()-st)
# 		print(len(dic))
# 		return JsonResponse(data)
	

# ##### shopify customer GraphQL Api   #####    ==> DONE  
# @csrf_protect    
# @csrf_exempt
# def mycustomers(request):
# 	st=time()
# 	if request.method=='POST':
# 		if request.POST.get('next_page')=="True":
# 			cursor,startdate,enddate=request.POST.get('cursor'),request.POST.get('startdate'),request.POST.get('enddate')

# 			startdate=startdate+'T00:00:00Z' if startdate not in['',None] else startdate
# 			enddate=enddate+'T23:59:59Z' if enddate not in['',None] else enddate
# 			filterq=f"customer_date:>='{startdate}' AND customer_date:<='{enddate}'" if startdate not in['',None] and enddate not in['',None] else ''
# 			filtercount=f"&created_at_min='{startdate}'&created_at_max='{enddate}'" if startdate not in['',None] and enddate not in ['',None] else ''

# 			outletapikey=request.headers.get('outletapikey')
# 			# url=" https://api.demo.xircls.in/utility/api/v1/get_shopname_access_token/"
# 			# headers = {
# 			#         'api-key': outletapikey,
# 			#         }
# 			# response = requests.request("POST", url, headers=headers)
# 			# data=json.loads(response.text)["response"]
# 			# shop=data["shop"]
# 			# access=data["access_token"]
# 			shop,access=give_details(outletapikey)
# 			urlcount = f"https://{shop}/admin/api/2023-10/customers/count.json?status=any{filtercount}"
# 			newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}
# 			datacount = json.loads(requests.get(urlcount, headers=newheaders).text)
# 			url = f"https://{shop}/admin/api/2023-07/graphql.json"

# 			if cursor in ['',None]:
# 				payload = "{\"query\":\"query MyQuery {\\n  customers(reverse: true, \\n    query: \\\"%s\\\"\\n first: 25) {\\n    edges {\\n      cursor\\n      node {\\n        acceptsMarketing\\n        createdAt\\n        email\\n        displayName\\n              numberOfOrders\\n        addresses {\\n          country\\n          city\\n          province\\n        }\\n        amountSpent {\\n          amount\\n        }\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n   \\n  }\\n}\",\"variables\":{}}"%(filterq)
# 			else:
# 				payload = "{\"query\":\"query MyQuery { \\n  customers(reverse: true, after: \\\"%s\\\"\\n    query: \\\"%s\\\"\\n first: 25) {\\n    edges {\\n      cursor\\n      node {\\n        acceptsMarketing\\n        createdAt\\n        email\\n        displayName\\n              numberOfOrders\\n        addresses {\\n          country\\n          city\\n          province\\n        }\\n        amountSpent {\\n          amount\\n        }\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n   \\n  }\\n}\",\"variables\":{}}"%(cursor,filterq)
# 			response = requests.request("POST", url, headers=newheaders, data=payload)
# 			data=json.loads(response.text)['data']['customers']
# 			cursor=str(data["pageInfo"]["endCursor"])
# 			next_page=str(data["pageInfo"]["hasNextPage"])
# 			if data["edges"]!=[]:
# 				#cursor=str(data["pageInfo"]["endCursor"])
# 				cust=[]
# 				for i in data["edges"]:
# 					custdata={}
# 					custdata['email'],custdata['name'],custdata['created_at'],custdata['accept_email_marketing'],custdata['orders_count'],custdata['total_spent'],custdata['country'],custdata['average_order_value']=i["node"]['email'],i["node"]['displayName'],i["node"]["createdAt"],i["node"]['acceptsMarketing'],i["node"]['numberOfOrders'],float(i["node"]['amountSpent']['amount']),i["node"]['addresses'][0]['country'] if i["node"]['addresses']!=[] else None,[round(float(i["node"]['amountSpent']['amount'])/int(i['node']['numberOfOrders']),2) if int(i['node']['numberOfOrders'])!=0 else 0][0]
# 					cust.append(custdata)
# 				data={'data':cust,'next_page':next_page,'cursor':cursor,'count':datacount["count"]}
# 			else:
# 				data={'data':[],'next_page':'False','cursor':'','count':datacount["count"]}  
# 		else:
# 			data={'data':[],'next_page':'False','cursor':'','count':0}
# 		print("time is  ",time()-st)
# 		return JsonResponse(data)
	

# ##### shopify average order value GraphQL Api   #####    ==> DONE     
# @csrf_protect          
# @csrf_exempt
# def averageordervalue(request):
# 	st=time()
# 	if request.method=='POST':
# 		startdate,enddate=request.POST.get('startdate'),request.POST.get('enddate')
# 		startdate=startdate+'T00:00:00Z' if startdate not in['',None] else startdate
# 		enddate=enddate+'T23:59:59Z' if enddate not in['',None] else enddate
# 		outletapikey=request.headers.get('outletapikey')
# 		filterq=f"created_at:>='{startdate}' AND created_at:<='{enddate}'" if startdate not in['',None] and enddate not in['',None] else ''
# 		# url=" https://api.demo.xircls.in/utility/api/v1/get_shopname_access_token/"
# 		# headers = {'api-key': outletapikey, 'Content-Type': 'application/json'}
# 		# response = requests.request("POST", url, headers=headers)
# 		# data=json.loads(response.text)
# 		# shop=data["response"]["shop"]
# 		# access=data["response"]["access_token"]
# 		shop,access=give_details(outletapikey)
# 		url = f"https://{shop}/admin/api/2023-10/graphql.json"

# 		payload2 = "{\"query\":\"query MyQuery {\\n  orders(\\n    query:\\\"%s\\\",first: 250) {edges {\\n          cursor\\n        \\n    node {\\n      totalPrice\\n  createdAt\\n    currentSubtotalLineItemsQuantity\\n    }}\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    \\n  }\\n}}\",\"variables\":{}}"%(filterq)

# 		newheaders = {
# 		'X-Shopify-Access-Token':access,
# 		'Content-Type': 'application/json'
# 		}
# 		response = requests.request("POST", url, headers=newheaders, data=payload2)
# 		data=json.loads(response.text)["data"]["orders"]
# 		next_page =str(data["pageInfo"]["hasNextPage"])
# 		cursor=str(data["pageInfo"]["endCursor"])

# 		df=pd.json_normalize(data['edges'])
# 		while next_page == "True":
# 			print(69)
# 			payload55 = "{\"query\":\"query MyQuery {\\n  orders(\\n after: \\\"%s\\\",  first: 250, query: \\\"%s\\\"\\n) {edges {\\n          cursor\\n        \\n    node {\\n      totalPrice\\n    createdAt\\n    currentSubtotalLineItemsQuantity\\n    }}\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    \\n  }\\n}}\",\"variables\":{}}"%(cursor,filterq)
# 			response = requests.request("POST", url, headers=newheaders, data=payload55)
# 			data=json.loads(response.text)["data"]["orders"]
# 			next_page=str(data["pageInfo"]["hasNextPage"])
# 			cursor=str(data["pageInfo"]["endCursor"])
# 			df1=pd.json_normalize(data['edges'])
# 			df=pd.concat([df,df1],axis=0)

# 		total_quantity=int(df['node.currentSubtotalLineItemsQuantity'].sum())
# 		total_price=round(df['node.totalPrice'].astype('float').sum(),2)
# 		total_order=int(len(df)) 
# 		average_order_value=round(total_price/total_order,2) if total_order!=0 else 0
# 		data={
# 			'aov':{
# 				'total_orders':total_order,
# 				'total_sales':total_price,
# 				'total_quantity':total_quantity,
# 				'Average_units_ordered':round(total_quantity/total_order,2) if total_order!=0 else 0,'average_order_value':average_order_value
# 				}
# 			  }
# 		print("time is ",time()-st)
# 		return JsonResponse(data) 


# ##### shopify return rate GraphQL Api   #####     ===>DONE        
# @csrf_protect    
# @csrf_exempt
# def returnrate(request):
# 	st=time()
# 	if request.method=='POST':
# 		if request.POST.get('next_page')=="True":
# 			cursor,startdate,enddate=request.POST.get('cursor'),request.POST.get('startdate'),request.POST.get('enddate')

# 			startdate=startdate+'T00:00:00Z' if startdate not in['',None] else startdate

# 			enddate=enddate+'T23:59:59Z' if enddate not in['',None] else enddate

# 			outletapikey=request.headers.get('outletapikey')

# 			filterq=f"created_at:>='{startdate}' AND created_at:<='{enddate}'" if startdate not in['',None] and enddate not in['',None] else ''

# 			shop,access=give_details(outletapikey)

# 			url = f"https://{shop}/admin/api/2023-07/graphql.json"

# 			newheaders = {
# 				'X-Shopify-Access-Token': access,
# 				'Content-Type': 'application/json'
# 				}
			
# 			# payload = "{\"query\":\"query MyQuery {\\n  orders(first: 250, query: \\\"%s\\\") {\\n    edges {\\n      cursor\\n      node {\\n        createdAt\\n                currentSubtotalLineItemsQuantity\\n        subtotalLineItemsQuantity\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n  }\\n}\",\"variables\":{}}"%(filterq)
# 			graphql_query = """
# 			query MyQuery($filter: String) {
# 			  orders(
# 				first: 250
# 				query: $filter
# 			  ) {
# 				edges {
# 				  cursor
# 				  node {
# 					createdAt
# 					currentSubtotalLineItemsQuantity
# 					subtotalLineItemsQuantity
# 				  }
# 				}
# 				pageInfo {
# 				  endCursor
# 				  hasNextPage
# 				}
# 			  }
# 			}
# 			"""
# 			variables = {
# 				"filter": filterq
# 			}

# 			# JSON payload including the query and variables
# 			payload = {
# 				"query": graphql_query,
# 				"variables": variables
# 			}

# 			response = requests.request("POST", url, headers=newheaders, json=payload)
# 			data=json.loads(response.text)["data"]["orders"]
# 			next_page =str(data["pageInfo"]["hasNextPage"])
# 			cursor=str(data["pageInfo"]["endCursor"])
# 			df=pd.json_normalize(data['edges'])

# 			while next_page == "True":
# 				print(69)
# 				# payload = "{\"query\":\"query MyQuery {\\n  orders(\\n after: \\\"%s\\\"\\n  first: 250, query: \\\"%s\\\") {\\n    edges {\\n      cursor\\n      node {\\n        createdAt\\n                currentSubtotalLineItemsQuantity\\n        subtotalLineItemsQuantity\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n  }\\n}\",\"variables\":{}}"%(cursor,filterq)
# 				graphql_query = """
# 				query MyQuery($cursor: String, $filter: String) {
# 				  orders(
# 					after: $cursor
# 					first: 250
# 					query: $filter
# 				  ) {
# 					edges {
# 					  cursor
# 					  node {
# 						createdAt
# 						currentSubtotalLineItemsQuantity
# 						subtotalLineItemsQuantity
# 					  }
# 					}
# 					pageInfo {
# 					  endCursor
# 					  hasNextPage
# 					}
# 				  }
# 				}
# 				"""
				
# 				variables = {
# 					"cursor": cursor,
# 					"filter": filterq
# 				}

# 				# JSON payload including the query and variables
# 				payload = {
# 					"query": graphql_query,
# 					"variables": variables
# 				}

# 				response = requests.request("POST", url, headers=newheaders, json=payload)
# 				data=json.loads(response.text)["data"]["orders"]
# 				next_page =str(data["pageInfo"]["hasNextPage"])
# 				cursor=str(data["pageInfo"]["endCursor"])
# 				df1=pd.json_normalize(data['edges'])
# 				df=pd.concat([df,df1],axis=0)  

# 			print(f"\n====\n{df.head()}\n")
# 			total_quantity,total_return_quantity=0,0
# 			total_quantity=int(df["node.currentSubtotalLineItemsQuantity"].sum())
# 			total_return_quantity=int(sum(df["node.subtotalLineItemsQuantity"]-df["node.currentSubtotalLineItemsQuantity"])) 

# 			data={
# 				'rr':{
# 					'totalquantitysold':total_quantity,'totalquantityreturn':total_return_quantity,
# 					'returnrate':[round((total_return_quantity/total_quantity)*100,2) if total_quantity!=0 else 0][0]
# 					}
# 					}
# 			print("time is  ",time()-st)
# 			return JsonResponse(data) 
		
# ##### shopify no of customers/orders on weekly basis GraphQL Api   #####     
# @csrf_protect    
# @csrf_exempt    
# def datacount(request):
# 	st=time()
# 	if request.method=='POST':
# 		startdate,enddate=dt.datetime.strptime(request.POST.get('startdate'), '%Y-%m-%d'),dt.datetime.strptime(request.POST.get('enddate'), '%Y-%m-%d')

# 		outletapikey,countof=request.headers.get('outletapikey'),request.POST.get('countof')

# 		# url=" https://api.demo.xircls.in/utility/api/v1/get_shopname_access_token/"
# 		# headers = {'api-key': outletapikey, 'Content-Type': 'application/json'}
# 		# response = requests.request("POST", url, headers=headers)
# 		# data=json.loads(response.text)
# 		# shop=data["response"]["shop"]
# 		# access=data["response"]["access_token"]
# 		shop,access=give_details(outletapikey)

# 		data={}
# 		for i in ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']:
# 			if startdate<=enddate:
# 				startdate2=str(startdate.date())+'T23:59:59Z'
# 				startdate1=str(startdate.date())+'T00:00:00Z'
		  
# 				filtercount=f"&created_at_min={str(startdate1)}&created_at_max={str(startdate2)}" if startdate not in['',None] and enddate not in ['',None] else ''
# 				urlcount = f"https://{shop}/admin/api/2023-10/{countof}/count.json?status=any{filtercount}"
# 				newheaders = {'X-Shopify-Access-Token': access,'Content-Type': 'application/json'}
# 				datacount = json.loads(requests.get(urlcount, headers=newheaders).text)['count']

# 				startdate=startdate+dt.timedelta(days=1)
# 				data[i]=datacount
# 			else:data[i]=0
# 		print("time is ",time()-st)
# 		return JsonResponse({'data':[data]})
	

##### shopify healthmeter basis on recent 30k orders GraphQL Api   #####   ==> Done      
@csrf_protect
@csrf_exempt
def healthsegmentation(request):
	st=time()
	if request.method=='POST':
		outletapikey=request.headers.get('outletapikey')

		shop,access=give_details(outletapikey)
		##################################
		cursor,startdate,enddate=request.POST.get('cursor'),request.POST.get('startdate'),request.POST.get('enddate')

		startdate=startdate+'T00:00:00Z' 

		enddate=enddate+'T23:59:59Z' 


		filterq=f"created_at:>='{startdate}' AND created_at:<='{enddate}'" 
		###################################
		
		try:
			url = f"https://{shop}/admin/api/2023-10/graphql.json"

			
			graphql_query = """
			query MyQuery($filter: String) {
			orders(
				first: 250
				reverse: true
				query: $filter
			) {
				edges {
				cursor
				node {
					createdAt
					totalPrice
					customer {
					id
					}
				}
				}
				pageInfo {
				endCursor
				hasNextPage
				}
			}
			}
			"""
			variables = {
					"filter": filterq
				}

			payload = {
				"query": graphql_query,
				"variables": variables
			}
			newheaders = {
			'X-Shopify-Access-Token':access,
			'Content-Type': 'application/json'
			}
			segment = requests.request("POST", url, headers=newheaders, json=payload)
			data=json.loads(segment.text)["data"]["orders"]
			next_page=str(data["pageInfo"]["hasNextPage"])
			cursor=str(data["pageInfo"]["endCursor"])
			rfm_data=pd.json_normalize(data['edges'])

			while len(rfm_data)<=30000 and next_page=='True':
				print(69)
				
				graphql_query = """
				query MyQuery($cursor: String,$filter: String) {
				orders(
					after: $cursor
					first: 250
					reverse: true
					query: $filter
				) {
					edges {
					cursor
					node {
						createdAt
						totalPrice
						customer {
						id
						}
					}
					}
					pageInfo {
					endCursor
					hasNextPage
					}
				}
				}
				"""
				variables = {
					"cursor": cursor,
					"filter": filterq

				}

				# JSON payload including the query and variables
				payload = {
					"query": graphql_query,
					"variables": variables
				}


				response = requests.request("POST", url, headers=newheaders, json=payload)
				data=json.loads(response.text)
				if 'data' not in data.keys():
					break
				data=data['data']['orders'] 
				next_page=str(data["pageInfo"]["hasNextPage"])
				cursor=str(data["pageInfo"]["endCursor"])
				df1=pd.json_normalize(data['edges'])
				rfm_data=pd.concat([rfm_data,df1],axis=0)


			rfm_data.rename(columns={'node.totalPrice':'Monetary'},inplace=True)
			print(rfm_data.head())
			rfm_data['node.createdAt']=pd.to_datetime(rfm_data['node.createdAt'],format='%Y-%m-%dT%H:%M:%SZ')
			rfm_data['node.createdAt']=rfm_data['node.createdAt'].dt.date
			rfm_data['Monetary']=rfm_data['Monetary'].astype('float')

			rfm_data=rfm_data.groupby('node.customer.id').agg({'cursor':'count',#Frequency
													'node.createdAt':'max',#recency
													'Monetary':'sum'#monetary
													}).reset_index().rename(columns={'node.customer.id':'user_id','cursor':'Frequency','node.createdAt':'Rscore'})      
			max_date=rfm_data['Rscore'].agg(['max'])['max']
			rfm_data['Rscore']=rfm_data['Rscore'].apply(lambda x:(max_date-x).days+1)
			rfm_data['Rscore'] = rfm_data['Rscore'].rank(ascending = False)
			rfm_data['Frequency'] = rfm_data['Frequency'].rank(ascending = True)
			rfm_data['Monetary'] = rfm_data['Monetary'].rank(ascending = True)
			rfm_data['Rscore'] = (rfm_data['Rscore'] / rfm_data['Rscore'].max())*100
			rfm_data['Frequency'] = (rfm_data['Frequency'] / rfm_data['Frequency'].max())*100
			rfm_data['Monetary'] = (rfm_data['Monetary'] / rfm_data['Monetary'].max())*100
			rfm_data['Rscore']=0.05*0.50 * rfm_data['Rscore']
			rfm_data['FMscore']=0.05*(0.30 * rfm_data['Frequency'] + 0.20 * rfm_data['Monetary'])
			print(f"before new column\n{rfm_data.head()}")
			rfm_data["Customer Segment NEW"] = np.where((rfm_data['Rscore'] >= 2.25) & (rfm_data['FMscore'] >= 1.5), "CHAMPIONS",
										(np.where((rfm_data['Rscore'] >=1)&(rfm_data['FMscore'] >= 1.5)&(rfm_data['Rscore'] <2.25), "LOYAL CUSTOMERS",
									(np.where((rfm_data['Rscore'] >=0)&(rfm_data['FMscore'] >= 2)&(rfm_data['Rscore']<1), "CAN'T LOSE THEM",
										(np.where((rfm_data['Rscore'] >=0)&(rfm_data['FMscore'] >= 1)&(rfm_data['Rscore'] <1)&(rfm_data['FMscore']<2), "HIBERNATING",
										(np.where((rfm_data['Rscore'] >=0)&(rfm_data['FMscore'] >= 0)&(rfm_data['Rscore']<1)&(rfm_data['FMscore']<1), "LOST",
										(np.where((rfm_data['Rscore'] >=1)&(rfm_data['FMscore'] >= 0)&(rfm_data['Rscore']<1.5)&(rfm_data['FMscore']<1), "ABOUT TO SLEEP",
											(np.where((rfm_data['Rscore'] >=1.5)&(rfm_data['FMscore'] >= 0)&(rfm_data['Rscore']<2)&(rfm_data['FMscore']<0.5), "PROMISING",
											(np.where((rfm_data['Rscore'] >=2)&(rfm_data['FMscore'] >= 0)&(rfm_data['FMscore']<0.5), "PRICE SENSITIVE",
										(np.where((rfm_data['Rscore'] >=2)&(rfm_data['FMscore'] >= 0.5)&(rfm_data['FMscore']<1), "RECENT USER",
						(np.where((rfm_data['Rscore'] >=2)&(rfm_data['FMscore'] >= 1)&(rfm_data['FMscore']<1.5), "POTENTIAL LOYALIST","NEED ATTENTION")))))))))))))))))))

			
			

			print(f"\n{rfm_data.head()}")
			t_orders=len(rfm_data)
			df=pd.DataFrame(rfm_data["Customer Segment NEW"].value_counts()).reset_index().rename(columns={'count':'no of customers','Customer Segment NEW':'segment'})

			df['no of customers'] = pd.to_numeric(df['no of customers'], errors='coerce')  # Convert to numeric, coerce errors to NaN if any
			total=df['no of customers'].sum()
			print(f"==\n{df.head()}\n")

			good=(df[df['segment'].isin(['CHAMPIONS','LOYAL CUSTOMERS',"NEED ATTENTION",'POTENTIAL LOYALIST'])]['no of customers'].sum()/total)*100

			
			bad=(df[df['segment'].isin(['PRICE SENSITIVE',"LOST","CAN'T LOSE THEM",'PROMISING'])]['no of customers'].sum()/total)*100

			print(f"good is {good}\nbad is {bad}")

			# if 50 <= good <= 100 and 0 <= bad <= 21:
			# 	print("came")
			# 	k = [90, 'EXCELLENT']
			# elif 40 < good <= 50 and 21 < bad <= 31:
			# 	k = [70, 'GOOD']
			# elif 30 < good <= 40 and 31 < bad <= 41:
			# 	k = [50, 'FAIR']
			# elif 20 < good <= 30 and 41 < bad <= 51:
			# 	k = [30, 'POOR']
			# else:
			# 	k = [10, 'BAD']

			k=np.where(good>50 and bad<21,[90,'EXCELLENT'],
			(np.where(good>40 and bad<31,[70,'GOOD'],
			(np.where(good>30 and bad<41,[50,'FAIR'],
			(np.where(good>20 and bad<51,[30,'POOR'],[10,'BAD'])))))))
			print(k)
			print("time is  ",time()-st)
			return JsonResponse(data=
				{
					'msg':"Recieved",
					'value':k[0],
					'label':k[1],
					'total_orders':t_orders
					}
				)
		except:
			return JsonResponse(data=
				{
					'msg':"No Data Available for the Dates",
				
				}
				)


# @csrf_exempt
# def return_customer_rate(request):
# 	st=time()
# 	pass
# 	# if request.method=='POST':

# 	# 	startdate=request.POST.get('startdate')
# 	# 	enddate=request.POST.get('enddate')
# 	# 	# st=time()
# 	# 	outletapikey=request.headers.get('outletapikey')
# 	# 	# print(f"\n{outletapikey}\n")
# 	# 	# # print(outletapikey,'lllllllllllllll')
# 	# 	# url=" https://api.demo.xircls.in/utility/api/v1/get_shopname_access_token/"
# 	# 	# headers = {
# 	# 	# 		'api-key': outletapikey,
# 	# 	# 		}
# 	# 	# response = requests.request("POST", url, headers=headers)
# 	# 	# data=json.loads(response.text)["response"]
# 	# 	# # print(data)
# 	# 	# shop=data["shop"]
# 	# 	# access=data["access_token"]
# 	# 	# print(access,shop)
# 	# 	# startdate=request.POST.get('startdate')
# 	# 	# enddate=request.POST.get('enddate')
# 	# 	shop,access=give_details(outletapikey)
# 	# 	filterq=[f"customer_date:>={startdate} AND customer_date:<{enddate}" if startdate not in['',None] and enddate not in['',None] else ''][0]
# 	# 	print(startdate,enddate,'llllllllllll')
# 	# 	url = f"https://{shop}/admin/api/2023-07/graphql.json"
# 	# 	print(f"\n====\nworked well\n==========\n")



# 	# 	# url = "https://quickstart-99171545.myshopify.com/admin/api/2023-07/graphql.json"
# 	# 	# payload = "{\"query\":\"query MyQuery {\\n  orders(first: 10) {\\n    edges {\\n      cursor\\n    }\\n    nodes {\\n      createdAt\\n      email\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n    \\n  }\\n}\",\"variables\":{}}"
# 	# 	graphql_query = """
# 	# 	query MyQuery($filter: String) {
# 	# 	orders(first: 250, query: $filter) {
# 	# 		edges {
# 	# 		cursor
# 	# 		}
# 	# 		nodes {
# 	# 		createdAt
# 	# 		email
# 	# 		}
# 	# 		pageInfo {
# 	# 		endCursor
# 	# 		hasNextPage
# 	# 		}
# 	# 	}
# 	# 	}
# 	# 	"""
# 	# 	variables = {
# 	# 		"filter": filterq
# 	# 	}

# 	# 	# JSON payload including the query and variables
# 	# 	payload = {
# 	# 		"query": graphql_query,
# 	# 		"variables": variables
# 	# 	}
# 	# 	newheaders = {
# 	# 		'X-Shopify-Access-Token': access,
# 	# 		'Content-Type': 'application/json'
# 	# 		}
# 	# 	response = requests.request("POST", url, headers=newheaders, json=payload)
# 	# 	print("\nResponse came fromshopify using dynamic access\n")
# 	# 	# print(json.loads(response.text))
# 	# 	data=json.loads(response.text)["data"]["orders"]
# 	# 	next_page = "True"

# 	# 	cursor=str(data["pageInfo"]["endCursor"])
# 	# 	print(data['edges'])
# 	# 	customers,return_customer_list,return_customer=[],[],0
# 	# 	for i in data["nodes"]:
# 	# 		# print(i)
# 	# 		# date=dt.datetime.strptime(i["createdAt"].split('T')[0],"%Y-%m-%d")
# 	# 		# if [date>=dt.datetime.strptime(startdate,"%Y-%m-%d") if startdate else True][0] and [date<=dt.datetime.strptime(enddate,"%Y-%m-%d") if enddate else True][0]:
# 	# 		if i["email"] not in customers:
# 	# 			customers.append(i["email"])
			
# 	# 		elif i["email"] not in return_customer_list:
# 	# 			return_customer_list.append(i["email"])
# 	# 			return_customer+=1

# 	# 	while next_page == "True":
# 	# 		print(69)
# 	# 		#payload = "{\"query\":\"query MyQuery {\\n  orders(after: \\\"%s\\\"\\n first: 10){\\n    edges {\\n      cursor\\n {\\n    nodes {\\n      createdAt\\n      email\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n  }\\n}\",\"variables\":{}}"
# 	# 		# payload = "{\"query\":\"query MyQuery {\\n  orders(after: \\\"%s\\\"\\n first: 10) {\\n    edges {\\n      cursor\\n    }\\n    nodes {\\n      createdAt\\n      email\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n    \\n  }\\n}\",\"variables\":{}}"%format(cursor)
# 	# 		#payload = "{\"query\":\"query MyQuery {\\n  orders(after: \\\"%s\\\"\\n first: 10) {\\n    edges {\\n      cursor\\n    }\\n    nodes {\\n      createdAt\\n      email\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\",\"variables\":{}}"
# 	# 		#payload = "{\"query\":\"query MyQuery {\\n  orders(\\n after: \\\"%s\\\"\\n first: 10) {\\n    edges {\\n      cursor\\n      node {\\n        returnStatus\\n        returns(first: 10) {\\n          nodes {\\n            totalQuantity\\n          }\\n        }\\n        lineItems(first: 10) {\\n          nodes {\\n            quantity\\n          }\\n        }\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n  }\\n}\",\"variables\":{}}"%format(cursor)

# 	# 		graphql_query = """
# 	# 		query MyQuery($cursor: String, $filter: String) {
# 	# 		orders(after: $cursor, first: 250, query: $filter) {
# 	# 			edges {
# 	# 			cursor
# 	# 			}
# 	# 			nodes {
# 	# 			createdAt
# 	# 			email
# 	# 			}
# 	# 			pageInfo {
# 	# 			endCursor
# 	# 			hasNextPage
# 	# 			}
# 	# 		}
# 	# 		}
# 	# 		"""
# 	# 		variables = {
# 	# 		"cursor": cursor,
# 	# 		"filter": filterq
# 	# 		}

# 	# 		# JSON payload including the query and variables
# 	# 		payload = {
# 	# 			"query": graphql_query,
# 	# 			"variables": variables
# 	# 		}

# 	# 		response = requests.request("POST", url, headers=newheaders, json=payload)
			
# 	# 		data=json.loads(response.text)["data"]["orders"]
# 	# 		# print(data)    
# 	# 		for i in data['nodes']:
# 	# 			# print(i)
# 	# 			# date=dt.datetime.strptime(i["createdAt"].split('T')[0],"%Y-%m-%d")
# 	# 			# if [date>=dt.datetime.strptime(startdate,"%Y-%m-%d") if startdate else True][0] and [date<=dt.datetime.strptime(enddate,"%Y-%m-%d") if enddate else True][0]:
# 	# 			if i["email"] not in customers:
# 	# 				customers.append(i["email"])
				
# 	# 			elif i["email"] not in return_customer_list:
# 	# 				return_customer_list.append(i["email"])
# 	# 				return_customer+=1
# 	# 		next_page=str(data["pageInfo"]["hasNextPage"])
# 	# 		cursor=str(data["pageInfo"]["endCursor"])

# 	# 	data={'rcr':{'totalcustomers':len(customers),'totalreturncustomer':return_customer,'returncustomerrate':[round((return_customer/len(customers))*100,2) if len(customers)!=0 else 0][0]}}

# 	# 	print(customers,return_customer_list,return_customer)
# 	# 	end=time()
# 	# 	print(f"time is {end-st}")
# 	# 	return JsonResponse(data)

# @csrf_exempt
# # @csrf_protect
# def monthlycohorts(request):
#     if request.method == 'POST':
#         url = "https://bombay-shaving.myshopify.com/admin/api/2023-10/orders.json?status=any"
#         dataset = requests.get(url, headers={'X-Shopify-Access-Token': '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'})
#         data = dataset.json()
#         monthlyco={}
#         #montnwise={"Total customers":0,"Total orders":0,"Average orders per customer":0,"Average spend per customer":0}
#         customer_id={}

#         #for i in date_list:
#         for i in data['orders']:
#             date=f"{dt.datetime.strptime(i['created_at'].split('T')[0],'%Y-%m-%d').month} {dt.datetime.strptime(i['created_at'].split('T')[0],'%Y-%m-%d').year}" 
#             if "customer" in i.keys() and i["customer"] not in [None,{}] and date not in monthlyco.keys():
#                 monthlyco[date]={}
#                 monthlyco[date]["Total orders"]=1
#                 monthlyco[date]["Total sales"]=float(i['current_total_price'])
#                 customer_id[date]=[]
#                 if i["customer"]["id"] not in customer_id[date]:
#                     customer_id[date].append(i["customer"]["id"])
#                     monthlyco[date]["Total customers"]=1
#                 monthlyco[date]["Average orders per customer"]=round(monthlyco[date]["Total orders"]/monthlyco[date]["Total customers"],2)
#                 monthlyco[date]["Average spend per customer"]=round(monthlyco[date]["Total sales"]/monthlyco[date]["Total customers"],2)
#             elif "customer" in i.keys() and i["customer"] not in [None,{}]:
#                 monthlyco[date]["Total orders"]=monthlyco[date]["Total orders"]+1
#                 monthlyco[date]["Total sales"]=monthlyco[date]["Total sales"]+float(i['current_total_price'])
#                 if i["customer"]["id"] not in customer_id[date]:
#                     customer_id[date].append(i["customer"]["id"])
#                     monthlyco[date]["Total customers"]=monthlyco[date]["Total customers"]+1
#                 monthlyco[date]["Average orders per customer"]=round(monthlyco[date]["Total orders"]/monthlyco[date]["Total customers"],2)
#                 monthlyco[date]["Average spend per customer"]=round(monthlyco[date]["Total sales"]/monthlyco[date]["Total customers"],2)
        
        
#         data={'monthlycohorts':[monthlyco]}
#         return JsonResponse(data)
