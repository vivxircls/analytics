from threading import Thread
import requests,json
import datetime as dt
import json
import pandas as pd
class SalesThread(Thread):
    def __init__(self,request,datacount,filterq,shop,newheaders):
        Thread.__init__(self)
        self.data=None
        self.request=request
        self.datacount=datacount
        self.filterq=filterq
        self.shop=shop
        self.headers=newheaders

    def run(self):
        url = f"https://{ self.shop}/admin/api/2023-07/graphql.json"

        cursor=''
        graphql_query = """ 
                    query MyQuery($filter: String) {
                    orders(
                        reverse: true
                        first: 25
                        query: $filter
                    ) {
                        edges {
                        cursor
                        node {
                            name
                            createdAt
                            displayFinancialStatus
                            displayFulfillmentStatus
                            totalPrice
                            email
                            subtotalPrice
                            currencyCode
                            customer {
                            addresses {
                                country
                                province
                                city
                                lastName
                                firstName
                            }
                            }
                            totalDiscounts
                            fulfillments(first: 10) {
                            createdAt
                            }
                            discountApplications(first: 10) {
                            edges {
                                cursor
                                node {
                                value {
                                    ... on PricingPercentageValue {
                                    __typename
                                    percentage
                                    }
                                    ... on MoneyV2 {
                                    __typename
                                    amount
                                    }
                                }
                                }
                            }
                            }
                            shippingAddress {
                            city
                            country
                            province
                            }
                            customer {
                            addresses {
                                country
                                province
                                city
                            }
                            displayName
                            }
                            currencyCode
                            discountCode
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
            "filter": self.filterq
        }

        # JSON payload including the query and variables
        payload = {
            "query": graphql_query,
            "variables": variables
        }

        response = requests.request("POST", url, headers=self.headers, json=payload)
        data=json.loads(response.text)["data"]["orders"]
        # print(data['edges'])
        if data["edges"]!=[]:
            next_page =str(data["pageInfo"]["hasNextPage"])
            cursor=str(data["pageInfo"]["endCursor"])
            rlocation=[self.request.GET.get('location') if self.request.GET.get('location') not in [None,''] else True][0]
            dic=[]
            for i in data["edges"]:
                data=i["node"]
                if data["customer"] not in [None,{}] and 'addresses' in data["customer"].keys() and data["customer"]['addresses'] not in [None,{}] and rlocation!=True:location=data["customer"]["addresses"][0]["country"]
                else:location=True
                if rlocation==location :
                    d=dict()
                    d['created_at'],d['currency'],d["current_subtotal_price"],d["current_total_discounts"],d["current_total_price"],d["email"],d["financial_status"],d["fulfillment_status"],d["order_number"]=data['createdAt'],data['currencyCode'],data["subtotalPrice"],data["totalDiscounts"],data["totalPrice"],data["email"],data["displayFinancialStatus"],data["displayFulfillmentStatus"],data["name"]
                    if data["customer"] not in [None,{}] and 'addresses' in data["customer"].keys() and data["customer"]['addresses'] not in [None,{}]:d["customer"]=[data["customer"]["addresses"][0]]
                    if data["discountApplications"]["edges"] not in [[],None]:
                        value=data["discountApplications"]["edges"][0]["node"]["value"]
                        d["value"],d["value_type"]=value["amount"]  if 'amount' in value.keys() else value["percentage"],value["__typename"]
                        d['code']=data["discountCode"]
                    if data["shippingAddress"] not in [{},None]:d["shipping_address"]=[data["shippingAddress"]]
                    d["timetofulfill"]=(dt.datetime.strptime(data["fulfillments"][0]["createdAt"],"%Y-%m-%dT%H:%M:%SZ")-dt.datetime.strptime(data["createdAt"], "%Y-%m-%dT%H:%M:%SZ")).days if data["fulfillments"]!=[] else 'unfulfilled'
                    dic.append(d)
            alltime_sales_data={'orders':dic,'next_page':next_page,'cursor':cursor,'count':self.datacount['count']}
        else:
            alltime_sales_data={'orders':[],'next_page':'False','cursor':"",'count':self.datacount['count']}
        # print("alltime sales data=>",alltime_sales_data)
        self.data=alltime_sales_data
            
class CustomerThread(Thread):
    def __init__(self,request,datacount_for_customers,filterq,shop,newheaders):
        Thread.__init__(self)
        self.data=None
        self.request=request
        self.datacount=datacount_for_customers
        self.filterq=filterq
        self.shop=shop
        self.headers=newheaders

    def run(self):
        url = f"https://{self.shop}/admin/api/2023-07/graphql.json"
        payload = "{\"query\":\"query MyQuery {\\n  customers(reverse: true, \\n    query: \\\"%s\\\"\\n first: 25) {\\n    edges {\\n      cursor\\n      node {\\n        acceptsMarketing\\n        createdAt\\n        email\\n        displayName\\n              numberOfOrders\\n        addresses {\\n          country\\n          city\\n          province\\n        }\\n        amountSpent {\\n          amount\\n        }\\n      }\\n    }\\n    pageInfo {\\n      endCursor\\n      hasNextPage\\n    }\\n   \\n  }\\n}\",\"variables\":{}}"%(self.filterq)

        response = requests.request("POST", url, headers=self.headers, data=payload)
        data=json.loads(response.text)['data']['customers']
        cursor=str(data["pageInfo"]["endCursor"])
        next_page=str(data["pageInfo"]["hasNextPage"])
        if data["edges"]!=[]:
            #cursor=str(data["pageInfo"]["endCursor"])
            cust=[]
            for i in data["edges"]:
                custdata={}
                custdata['email'],custdata['name'],custdata['created_at'],custdata['accept_email_marketing'],custdata['orders_count'],custdata['total_spent'],custdata['country'],custdata['average_order_value']=i["node"]['email'],i["node"]['displayName'],i["node"]["createdAt"],i["node"]['acceptsMarketing'],i["node"]['numberOfOrders'],float(i["node"]['amountSpent']['amount']),i["node"]['addresses'][0]['country'] if i["node"]['addresses']!=[] else None,[round(float(i["node"]['amountSpent']['amount'])/int(i['node']['numberOfOrders']),2) if int(i['node']['numberOfOrders'])!=0 else 0][0]
                cust.append(custdata)
            data={'data':cust,'next_page':next_page,'cursor':cursor,'count':self.datacount["count"]}
        else:
            data={'data':[],'next_page':'False','cursor':'','count':self.datacount["count"]} 
        
        self.data=data
        
        
class InsightsThread(Thread):
    def __init__(self,filterq,shop,newheaders):
        Thread.__init__(self)
        self.filterq=filterq
        self.shop=shop
        self.newheaders=newheaders
        self.data=None
    
    def give_graphql_query_for_while(self,filterq,cursor):
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
    
    def run(self):
        url = f"https://{self.shop}/admin/api/2023-10/graphql.json"
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
            "filterq": self.filterq
        }

        # JSON payload including the query and variables
        payload = {
            "query": graphql_query,
            "variables": variables
        }

        response = requests.request("POST", url, headers=self.newheaders, json=payload)
        data=json.loads(response.text)["data"]["orders"]
        next_page =str(data["pageInfo"]["hasNextPage"])
        cursor=str(data["pageInfo"]["endCursor"])
        df=pd.json_normalize(data['edges'])

        while next_page == "True":
            print(69)
            payload=self.give_graphql_query_for_while(self.filterq,cursor)
            response = requests.request("POST", url, headers=self.newheaders, json=payload)
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
                'returned_users':returned_users,
                'unique_users':unique_users

            }
        self.data=data
			# print(len(df))
			# print(len(df[df['node.email'].duplicated()])/len(df))
			# df=pd.DataFrame([data])
			# df.to_csv("insights1.csv",index=False)
			# return JsonResponse(data=
			# 	data.update({'mssg':'data processed successfully'}),
			# 	safe=False,
			# 	status=HTTP_200_OK
			# )
		# except:
			# return JsonResponse(data=
			# 	{
			# 		'mssg':'Error occurred from shopify.com'
			# 		# 'total_quantity':total_quantity,
			# 		# 'total_price':total_price,
			# 		# 'total_order':total_order,
			# 		# 'total_return_quantity':total_return_quantity,
			# 		# 'return_rate':return_rate,
			# 		# 'average_order_value':average_order_value,
			# 		# 'average_units_ordered':average_units_ordered

			# 	},
			# 	safe=False,
			# 	status=HTTP_204_NO_CONTENT
			# )

class ProductsThread(Thread):
    def __init__(self,filterq,shop,newheaders):
        Thread.__init__(self)
        self.filterq=filterq
        self.shop=shop
        self.newheaders=newheaders
        self.data=None
        self.df=None
    
    # def give_data(self,url,newheaders, payload):
    #     response = requests.request("POST", url, headers=newheaders, json=payload)
    #     data=response.json()["data"]["orders"]
    #     next_page=str(data["pageInfo"]["hasNextPage"])
    #     cursor=str(data["pageInfo"]["endCursor"])
    #     return data,next_page,cursor
    
    def run(self):
        url = f"https://{self.shop}/admin/api/2023-07/graphql.json"
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
            "filter": self.filterq
        }

        # JSON payload including the query and variables
        payload = {
            "query": graphql_query,
            "variables": variables
        }

        response = requests.request("POST", url, headers=self.newheaders, json=payload)
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
                "filterq": self.filterq
            }
            
            # JSON payload including the query and variables
            payload = {
                "query": graphql_query,
                "variables": variables
            }
        
            # data,next_page,cursor=self.give_data(url,self.newheaders, payload)
            response = requests.request("POST", url, headers=self.newheaders, json=payload)
            data=response.json()["data"]["orders"]
            next_page=str(data["pageInfo"]["hasNextPage"])
            cursor=str(data["pageInfo"]["endCursor"])
            df_inner=pd.json_normalize(data['edges'][0]['node']['lineItems']['edges'])
            for i in range(1,len(data['edges'])):
                df_inner1=pd.json_normalize(data['edges'][i]['node']['lineItems']['edges'])
                df_inner=pd.concat([df_inner,df_inner1],axis=0)
            

            df_list.append(df_inner)

        df=pd.concat(df_list,axis=0)
        # df.to_csv("top_products.csv",index=False)
        df['node.originalTotal']=df['node.originalTotal'].apply(pd.to_numeric)
        df=df.groupby(by='node.title').sum()
        df.reset_index(inplace=True)
        df.rename(
        columns={
            'node.title':'name',
            'node.quantity':'quantity',
            'node.originalTotal':'total_price'
        },
            inplace=True
        )
        self.df=df
        
from time import sleep             
class ReturnProductsThread(Thread):
    def __init__(self,filterq,shop,newheaders):
        Thread.__init__(self)
        self.filterq=filterq
        self.shop=shop
        self.newheaders=newheaders
        self.data=None
        self.df=None
        
    def run(self):
        url = f"https://{self.shop}/admin/api/2023-07/graphql.json"
        graphql_query = """
            query MyQuery($filter: String) {
            orders(first: 76, query: $filter) {
                edges {
                
                node {
                    createdAt
                    returnStatus
                    name
                    lineItems(first: 10) {
                    edges {
                        
                        node {
                        name
                        currentQuantity
                        quantity
                        
                    
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

        variables = {
            "filter": self.filterq
        }
        payload = {
            "query": graphql_query, 
            "variables": variables
        }

        response = requests.request("POST", url, headers=self.newheaders, json=payload)
        data=json.loads(response.text)["data"]["orders"]
        next_page = "True"
        cursor=str(data["pageInfo"]["endCursor"])
        # print(data['edges'])

        edges=data['edges'][0]['node']['lineItems']['edges']
        # dummy_return_list=[data['edges'][0]['node']['returnStatus']]*len(edges)
        df_inner=pd.json_normalize(edges)
        # return_list=return_list+dummy_return_list
        for i in range(1,len(data['edges'])):
            # return_list.append(data['edges'][i]['node']['returnStatus'])
            
            edges=data['edges'][i]['node']['lineItems']['edges']
            # dummy_return_list=[data['edges'][i]['node']['returnStatus']]*len(edges)
            # return_list=return_list+dummy_return_list
            df_inner1=pd.json_normalize(edges)
            df_inner=pd.concat([df_inner,df_inner1],axis=0,ignore_index=True)


        # print(df_inner)
        df_list=[df_inner]
        sleep(2)

        while next_page == "True":
            print(69)
            graphql_query = """
            query MyQuery($filter: String, $cursor: String) {
            orders(first: 76, query: $filter, after: $cursor) {
            
                edges {
                
                node {
                    createdAt
                    returnStatus
                    name
                    lineItems(first: 10) {
                    edges {
                        
                        node {
                        name
                        currentQuantity
                        quantity
                
                        
                    
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
        
            variables = {"filter": self.filterq, "cursor": cursor}
            payload = {"query": graphql_query, "variables": variables}



            
            response = requests.request("POST", url, headers=self.newheaders, json=payload)
            data=json.loads(response.text)["data"]["orders"]
            next_page=str(data["pageInfo"]["hasNextPage"])
            cursor=str(data["pageInfo"]["endCursor"])

            edges=data['edges'][0]['node']['lineItems']['edges']
            # dummy_return_list=[data['edges'][0]['node']['returnStatus']]*len(edges)
            df_inner=pd.json_normalize(edges)
            # return_list=return_list+dummy_return_list
            
            for i in range(1,len(data['edges'])):
                # return_list.append(data['edges'][i]['node']['returnStatus'])
                
                edges=data['edges'][i]['node']['lineItems']['edges']
                # dummy_return_list=[data['edges'][i]['node']['returnStatus']]*len(edges)
                # return_list=return_list+dummy_return_list
                df_inner1=pd.json_normalize(edges)
                df_inner=pd.concat([df_inner,df_inner1],axis=0,ignore_index=True)

            df_list.append(df_inner)
            

        df_final=pd.concat(df_list,axis=0,ignore_index=True)

        df_final.fillna({
            'node.currentQuantity':0,
            'node.quantity':0
        },inplace=True)

        df_final=df_final[   df_final['node.currentQuantity'] < df_final['node.quantity'] ]
        df_final['diff']=df_final['node.quantity']-df_final['node.currentQuantity']
        # print(df_final.head(20))
        # df_final=df_final[df_final['diff']>0]
        df_ret_products=df_final.groupby('node.name').sum()
        # print(df_ret_products)
        print("=========================================")
        # df_ret_products['date']=startdate
        df_ret_products.reset_index(inplace=True)
        # df.to_csv("top_return_products.csv",index=False)
        # print(df)
        df_ret_products.rename(
        columns={
            'node.name':'name',
            'diff':'return_quantity'
        },
        inplace=True
                )
        df_ret_products.drop(columns=['node.currentQuantity','node.quantity'],inplace=True)
        # print(df_ret_products)
        self.df=df_ret_products
        # print(df.head())
        # print(df.sort_values('diff',ascending=False).tail())
        # print(df.shape)
        # return_products=list(df.sort_values('diff',ascending=False).index[1:10])
        # print(return_products)
     
class ChannelsThread(Thread):
    def __init__(self,filterq,shop,newheaders):
        Thread.__init__(self)
        self.filterq=filterq
        self.shop=shop
        self.newheaders=newheaders
        self.data=None
        self.df=None     
    
    def run(self):
        url = f"https://{self.shop}/admin/api/2023-07/graphql.json"

	
	
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
            "filter": self.filterq
        }

        # JSON payload including the query and variables
        payload = {
            "query": graphql_query,
            "variables": variables
        }
        response = requests.request("POST", url, headers=self.newheaders, json=payload)
        data=json.loads(response.text)["data"]["orders"]
        next_page = "True"
        cursor=str(data["pageInfo"]["endCursor"])

        df=pd.json_normalize(data['edges'])

        while next_page == "True":
            print(69)
            
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
                "filter": self.filterq,
                "cursor": cursor
            }
            
            # Payload
            payload = {
                "query": graphql_query,
                "variables": variables
            }
            

            response = requests.request("POST", url, headers=self.newheaders, json=payload)
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
        # print(counts)
        # print(variants)
        zipped_data=dict(zip(variants,counts))
        # print(zipped_data)
        df=pd.DataFrame(zipped_data.items(),columns=['channel_name','sold_quantity'])
        # df.to_csv("top_channels.csv",index=False)
        # print(df)
        self.df=df


            
            