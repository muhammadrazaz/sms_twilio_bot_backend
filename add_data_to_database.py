import requests
import pandas as pd
import numpy as np





def add_states(base_url : str,headers:dict, states : list[str])->None:
    for state in states:
        state_data = {
            "state_name" : state
        }
        response = requests.post(base_url+'/bot/states/',json=state_data,headers=headers)
        if response.status_code !=201:
            print(response.json())
            # break
    # print('all states added')

def add_in_town(base_url : str,headers:dict , data)->None:
    for index,row in data.iterrows():
        # print(row['Username'])
        row = row.fillna('')
        in_town_data = {
            "user_id" : row['User ID'],
            'username' : row['Username'],
            'user_states' : row['States'],
            'whatsapp': row['WhatsApp'],
            'sms':row['SMS'],
            'email':row['Email'],
            'discord':row['Discord'],
            'instagram':row['Instagram'],
            'snapchat':row['Snapchat'],
            'status':'not_verified',


        }
        
       
        response = requests.post(base_url+'/bot/leads/',json=in_town_data,headers=headers)

        if response.status_code != 201:
            print(response.json(),'========')
        

def add_shipping(base_url : str,headers:dict , data)->None:
    for index,row in data.iterrows():
        # print(row['Username'])
        row = row.fillna('')
        shipping_data = {
            "user_id" : row['User ID'],
            'username' : row['Username'],
            'whatsapp': row['WhatsApp'],
            'sms':row['SMS'],
            'email':row['Email'],
            'discord':row['Discord'],
            'instagram':row['Instagram'],
            'snapchat':row['Snapchat'],
            'status':'not_verified',


        }
        response = requests.post(base_url+'/bot/shippings/',json=shipping_data,headers=headers)

        if response.status_code != 201:
            print(response.json(),'========')

# def add_agent(base_url : str,headers:dict , data)->None:
#     for index,row in data.iterrows():
#         # print(row['Username'])
#         row = row.fillna('')
       
#         agent_data = {
#             "username" : row['States'],
#             'password' : '12345678',
#             'email': row['Email'],
#             'channel_id':row['Channel ID'],
#             'uan':row['UAN'],
#             'states':[row['States']],
#             'telegram_username':row['Telegram Username'],
            


#         }
        
#         response = requests.post(base_url+'/agent/',json=agent_data,headers=headers)

#         if response.status_code != 201:
#             print(response.json(),'========')
      



if __name__ == "__main__":



    token = 'test'
    headers = {
        'Authorization': f'{token}'
    }

    base_url = "http://127.0.0.1:8000/api"

    state_df = pd.read_excel("Telegram_redirect.xlsx")
    states_series = state_df['States'].dropna()
    all_states = states_series.str.split(',').apply(lambda x: [state.strip() for state in x]).sum()
    unique_states = set(all_states)

    # add_states(base_url=base_url, headers=headers, states=unique_states)

    in_town_df = pd.read_excel("Telegram_redirect.xlsx",sheet_name="Location")
    add_in_town(base_url=base_url,headers=headers,data=in_town_df)

    shipping_df = pd.read_excel("Telegram_redirect.xlsx",sheet_name="Shipping")
    add_shipping(base_url=base_url,headers=headers,data=shipping_df)


    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjE5NjI1LCJpYXQiOjE3MzExMzk2MjUsImp0aSI6IjAzMDUxM2EwN2U4ZTQ2MThiMWI1ZDE5ZjU0YWVjYzUzIiwidXNlcl9pZCI6MX0.hiVsanP63lGbh9jDLOGC3x3gObH4zybi9lFmDtPSlC0'
    # headers = {
    #     'Authorization': f'Bearer {token}'
    # }

    # agent_df = pd.read_excel("Telegram_redirect.xlsx",sheet_name="Agents")

    # add_agent(base_url=base_url,headers=headers,data=agent_df)