import requests
from requests.structures import CaseInsensitiveDict
import json
def success(status):
       if status == 200 or status == 201:
              return True
       else:
              return False


# STEP 1
STEPONEURL = "https://sandbox.smaapis.de/oauth2/token/"
step1payload = "POST%20sandbox.smaapis.de%2Foauth2%2Ftoken=&HTTP%2F1.1=&Host%3A%20smaapis.de=&Content-Type%3A%20application%2Fx-www-form-urlencoded=&client_id=unistrathyclyde_api&client_secret=a03cd85d-a7bf-4b59-affd-d2aba4534c56&grant_type=client_credentials&="
headers1 = CaseInsensitiveDict()
headers1["Content-Type"] = "application/x-www-form-urlencoded"
r1 = requests.post(STEPONEURL, data=step1payload,headers=headers1)
print("\n(STEP ONE) Status Code: {0}. Successful: {1}\n".format(r1.status_code,success(r1.status_code)))
TOKEN = r1.json()['access_token']
print("{0}\n".format(TOKEN))

# STEP 2
STEPTWOURL = "https://sandbox.smaapis.de/oauth2/v2/bc-authorize/"
headers2 = {'Content-Type': 'application/json','Authorization':'Bearer {0}'.format(TOKEN)}
step2payload = {'loginHint':'apiTestUser@apiSandbox.com'}

r2 = requests.post(STEPTWOURL, json=step2payload,headers=headers2)
print("\n(STEP TWO) Status Code: {0}. Successful: {1}\n".format(r2.status_code,success(r2.status_code)))
print(r2.json())


# STEP 2.5 (Simulation of button click of plant owner to initiate permission flow)
STEPTWOURL = "https://sandbox.smaapis.de/oauth2/v2/bc-authorize/apiTestUser@apiSandbox.com/state/"
headers2 = {'Content-Type': 'application/json','Authorization':'Bearer {0}'.format(TOKEN)}
step2payload = {'status':'accepted'}
r2 = requests.put(STEPTWOURL, json=step2payload,headers=headers2)


# STEP 3
STEPTHREEURL = "https://sandbox.smaapis.de/oauth2/v2/bc-authorize/apiTestUser@apiSandbox.com/"
headers2 = {'Host':'smaapis.de','Content-Type': 'application/json','Authorization':'Bearer {0}'.format(TOKEN)}
step3payload = {}

r3 = requests.get(STEPTHREEURL,data=step3payload,headers=headers2)
print("\n(STEP THREE) Status Code: {0}. Successful: {1}\n".format(r3.status_code,success(r3.status_code)))
print(r3.json())


# GET DATA DUMMY DATA VIA API FOR EXAMPLE
r = "https://sandbox.smaapis.de/monitoring/v1/plants"
headers2 = {'Host':'smaapis.de','Content-Type': 'application/json','Authorization':'Bearer {0}'.format(TOKEN)}
r = requests.get(r,headers=headers2)
print("\nStatus Code: {0}. Successful: {1}\n".format(r.status_code,success(r.status_code)))
print(r.json())
