import requests
import json
import wr_excel
from datetime import datetime, timedelta
# 获取token
def userlogin():
    url1 = 'http://172.18.101.184/login'
    user = {
        'email': 'zuguang_li@nuaa.edu.cn',
        'password': 'lizuguang1996+'
    }
    # 添加UA头
    header1 = {'Content-Type': 'application/json'}
    respose = requests.post(url1, json=user, headers=header1)
    access_token = respose.json().get('access_token', None)
    return access_token
# 查询区块
def query_evidence(access_token):
    url = "http://172.18.101.184/network/SpectrumSharing/transactions/query"
    payload = json.dumps(
        {
            "channelId": "spectrumtrading",
            "offset": 0,
            "limit": 100,
            "ascend": False,
            "filter": {},
            "from": {},
            "networkName": "SpectrumSharing"
        })
    # 备注：offset，limit是数字，filter和from是对象，ascend是布尔类型
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.request('POST', url, headers=headers, data = payload)
    return response
def query_blocks(blockHash):
    url = "http://172.18.101.184/network/SpectrumSharing/blocks/" + str(blockHash)
    payload = json.dumps(
        {
            "networkName": "SpectrumSharing"
        })
    # 备注：offset，limit是数字，filter和from是对象，ascend是布尔类型
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response2 = requests.request('GET', url, headers=headers, data = payload)
    return response2
if __name__ == '__main__':
    access_token = userlogin()
    #access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbk5hbWUiOiJsaXp1Z3VhbmciLCJyb2xlIjoiYWRtaW4iLCJjb250YWN0RW1haWwiOiJ6dWd1YW5nX2xpQG51YWEuZWR1LmNuIiwiY29tcGFueU5hbWUiOiJsaXp1Z3VhbmciLCJpbnNwZWN0b3IiOmZhbHNlLCJpYXQiOjE2NDAzMjYxNzgsImV4cCI6MTY0MDQxMjU3OH0.vxB2hQPHeaDRPQ_RLua0KoEuBCtuYE4fnSETclJmurU'
    response = query_evidence(access_token)
    response_json = response.json()
    items = response_json['items']
    createTimestamp_list = []
    updatedAt_list = []
    blockHash_list = []
    transaction_completion_time_list = []
    for items_i in items:
        # 获取哈希值
        blockHash = items_i['blockHash']
        response2 = query_blocks(blockHash)
        response2_json = response2.json()
        createTimestamp = response2_json['createTimestamp']
        updatedAt = response2_json['updatedAt']
        createTimestamp = datetime.strptime(createTimestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        updatedAt = datetime.strptime(updatedAt, '%Y-%m-%dT%H:%M:%S.%fZ')
        # 将UTC国际标注时间转为北京时间
        #createTimestamp = createTimestamp + timedelta(hours=8)
        createTimestamp_list.append(str(createTimestamp))
        updatedAt_list.append(str(updatedAt))
        blockHash_list.append(blockHash)
        # 计算交易时间
        transaction_completion_time = (updatedAt - createTimestamp).total_seconds()
        transaction_completion_time_list.append(str(transaction_completion_time))

    wr_excel.w_excel3(blockHash_list, createTimestamp_list, updatedAt_list, transaction_completion_time_list)

