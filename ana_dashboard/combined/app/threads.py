from threading import Thread
import requests,json
import datetime as dt
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