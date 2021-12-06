import requests
import pandas as pd
#function to normalize json data
def Normalize(data):
    all_column = []
    selected_column = []

    for item in data:
        for key in item.keys():
            if isinstance(item[key], list):
                if key not in selected_column and item[key]:
                    selected_column.append(key)
            elif key not in selected_column:
                if key not in all_column:
                    all_column.append(key)
        if len(selected_column) + len(all_column) == len(item.keys()):
            break
    print("len of all column is {} and selected column is {}".format(len(all_column), len(selected_column)))
    pf = pd.json_normalize(data, record_path=selected_column[0], meta=all_column, errors='ignore',record_prefix=str(selected_column[0]+'-'))
    for i in range(1, len(selected_column)):
        pf1 = pd.json_normalize(data, record_path=selected_column[i], meta=all_column[0], errors='ignore',record_prefix=str(selected_column[i]+'-'))
        pf = pf.merge(pf1, on=all_column[0])
    return pf

#request to get object ids
object_ids = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects')
data = []
#fetching object details for first 50 objects
for id in object_ids.json()['objectIDs'][10000:10050]:
    obj_detail = requests.get('https://collectionapi.metmuseum.org/public/collection/v1/objects/'+str(id))
    data.append(obj_detail.json())
    print(id)
df = Normalize(data)
df.to_csv('C:/Users/Mohammad Touseef/Documents/Museum1.csv',index=False)

'''
index = 0
all_column = []
selected_column = []
for item in data:
    for key in item.keys():
        if isinstance(item[key],list):
            selected_column.append(key)
        if key not in selected_column and item[key]:
            all_column.append(key)
    break
pf = pd.json_normalize(data,record_path=selected_column[0],meta=all_column,errors='ignore')
for i in range(1,len(selected_column)):
    pf1 = pd.json_normalize(data,record_path=selected_column[i],meta=all_column[0])
    pf.merge(pf1,on=all_column[0])
pf.to_csv('C:/Users/Mohammad Touseef/Documents/MuseumAPI.csv')
pf = pd.json_normalize(data,record_path='constituents',meta=all_column,errors='ignore')
pf1 = pd.json_normalize(data,record_path='measurements',meta='objectID')
mer = pf1.merge(pf,on='objectID')
pf2 = pd.json_normalize(data,record_path='tags',meta='objectID')
mer = mer.merge(pf2,on='objectID')
mer.to_csv('C:/Users/Mohammad Touseef/Documents/MuseumAPI.csv')'''