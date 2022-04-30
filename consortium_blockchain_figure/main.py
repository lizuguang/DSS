import requests
import json
import time
import hashlib
import wr_excel
import leader_follower_game
from datetime import datetime, timedelta
# 获取token
def userlogin():
  url1 = 'http://172.18.101.184/login'
  user = {
    "email": "zuguang_li@nuaa.edu.cn",
    "password": "lizuguang1996+"
  }
  user2 = {
    "email": "123456@qq.com",
    "password": " Nj@123456"
  }
  # 添加UA头
  header1 = {"Content-Type":"application/json"}
  respose = requests.post(url1, json=user, headers=header1)
  access_token = respose.json().get("access_token", None)
  return access_token
# 写入区块链
def post_evidence(transaction):
  url ="http://172.18.101.184/network/SpectrumSharing/evidence/create"
  payload = json.dumps({
  "channelId":"spectrumtrading",
  "evidenceData": transaction,
  "networkName": "SpectrumSharing"
  })
  #start_time = time.time()
  headers = {
   'role_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdOYW1lIjoib3JnMSIsImlhdCI6MTYzOTQ3NTAwMCwiZXhwIjoxNjM5NTYxNDAwfQ.baxH_DBggqIvpVvaHCj14Sw2ANziJRl3y_w2orB4oPc',
   'Authorization': 'Bearer ' + access_token,
   'Content-Type': 'application/json'
  }
  start_time0 = time.time()
  response = requests.request("POST", url, headers = headers, data = payload)
  print(str(response))
  while str(response) == '<Response [500]>':
    print("写入区块失败：%s，正在重新写入。", str(response))
    response = requests.request("POST", url, headers=headers, data=payload)
  end_time0 = time.time()
  latency_update = end_time0 - start_time0
  # end_time1为计算平均时延的结束时间，仿真2
  end_time1 = datetime.now()
  #print("start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
  #print("end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
  return response, end_time1, latency_update
def product_tran(data):
  # -----------模拟生成交易信息-----------
  tran_time = int(time.time())
  str1 = '"CreateMirror","{"docType":"product","ID":"118","Version":"1","Timestamp":'
  str2 = ',"Admin":"","Title":"spectrum sharing strategy","Responsibility":"spectrum sources","Files":[{"ID":"118","Title":"spectrum sharing strategy","Hash":'
  hash = hashlib.sha256()
  hash.update(data.encode('utf-8'))
  str3 = ',"IPFS":"IPFS"}],"from":"eDUwOTo6Q049YWNjb3VudEUsT1U9Y2xpZW50OjpDTj1jYS5kZXNpbmVtZWNoYW5pc20ubnVhYW5ldHdvcmssTz1kZXNpbmVtZWNoYW5pc20ubnVhYW5ldHdvcmssTD1OYW5qaW5nLFNUPUppYW5nc3UsQz1DTg=="}"'
  transaction = str1 + str(tran_time) + str2 + hash.hexdigest() + str3
  #transaction = transaction + data   #此时blocksize = 10
  #transaction = "b" + str(n_tran) 此时blocksize = 6
  # ------------------------------------
  # 写入区块中
  response, end_time1, latency_update = post_evidence(transaction)
  return response, end_time1, latency_update
# 获取区块链中区块的总数
def get_totalCount(access_token):
  url = "http://172.18.101.184/network/SpectrumSharing/blocks/totalCount"
  payload = json.dumps({
    "networkName": "SpectrumSharing"
  })
  headers = {
    'role_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcmdOYW1lIjoib3JnMSIsImlhdCI6MTYzOTQ3NTAwMCwiZXhwIjoxNjM5NTYxNDAwfQ.baxH_DBggqIvpVvaHCj14Sw2ANziJRl3y_w2orB4oPc',
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  totalCount = response.json().get("count", None)
  return totalCount
if __name__ == '__main__':
  access_token = userlogin()
  #print(access_token)
  #access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbk5hbWUiOiJsaXp1Z3VhbmciLCJyb2xlIjoiYWRtaW4iLCJjb250YWN0RW1haWwiOiJ6dWd1YW5nX2xpQG51YWEuZWR1LmNuIiwiY29tcGFueU5hbWUiOiJsaXp1Z3VhbmciLCJpbnNwZWN0b3IiOmZhbHNlLCJpYXQiOjE2NDAzMjYxNzgsImV4cCI6MTY0MDQxMjU3OH0.vxB2hQPHeaDRPQ_RLua0KoEuBCtuYE4fnSETclJmurU'
  # start_time0为系统开始时间
  #start_time0 = datetime.now()
  # system_time计算每次写入区块成功后的时间与start_time0的时间差，以实现仿真1
  #system_time =[]
  response_list = []
  # 计算主节点计算交易策略开始到写入区块的时间，以实现仿真2
  Time_list = []
  # 初始区块链中的区块数
  totalCount_0 = get_totalCount(access_token)
  # Count记录不同时间点，频谱策略写入区块的数量
  #Count = []
  # EndTime_list记录每次主节点提交频谱策略完成的时间戳
  EndTime_list = []
  latency_update_list = []
  num = 12
  for n_tran in range(50):
    # start_time1为计算平均时延的开始时间，仿真2
    start_time1 = datetime.now()
    b_m_n = leader_follower_game.game(num)
    data = str(b_m_n)
    response, end_time1, latency_update = product_tran(data)
    #print(response.text)
    # end_time0为完成一次区块上传的结束时间
    #totalCount_1 = get_totalCount(access_token)
    #end_time0 = datetime.now()
    #Count.append(totalCount_1 - totalCount_0)
    response_list.append(response.text)
    Time_list.append(timedelta.total_seconds(end_time1 - start_time1))
    #system_time.append(str(end_time0 - start_time0))
    EndTime_list.append(str(end_time1))
    #time.sleep(180)
    #latency_update_list.append(latency_update)

  #wr_excel.w_excel1(latency_update_list, response_list)
  wr_excel.w_excel2(response_list, EndTime_list, Time_list, num)