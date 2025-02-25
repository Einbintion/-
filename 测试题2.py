import ssl
import urllib.request
import json
import pandas as pd
from datetime import datetime

# 请求的 URL
url = "http://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN"

# 设置 SSL 上下文以支持旧版 TLS
ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT

# 请求头
headers = {
    'Host': 'iftp.chinamoney.com.cn',
    'Connection': 'keep-alive',
    'Content-Length': '119',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua-platform': '"Windows"',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'sec-ch-ua-mobile': '?0',
    'Origin': 'https://iftp.chinamoney.com.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://iftp.chinamoney.com.cn/english/bdInfo/',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '_ulta_id.ECM-Prod.ccc4=83e23fd70be13020; _ulta_ses.ECM-Prod.ccc4=13952a8154ccedc8; AlteonP10=BASlZSw/F6xu3PZPiljfAQ$$; apache=4a63b086221745dd13be58c2f7de0338; ags=b168c5dd63e5c0bebdd4fb78b2b4704a',
}

# 表单数据
data = {
    'pageNo': '1',
    'pageSize': '15',
    'isin': '',
    'bondCode': '',
    'issueEnty': '',
    'bondType': '100001',
    'couponType': '',
    'issueYear': '2023',
    'rtngShrt': '',
    'bondSpclPrjctVrty': '',
}

# 将表单数据转换为字节流
encoded_data = urllib.parse.urlencode(data).encode('utf-8')

# 创建请求对象
req = urllib.request.Request(url, headers=headers, data=encoded_data, method='POST')

try:
    # 发送请求并获取响应
    response = urllib.request.urlopen(req, context=ctx)
    response_data = response.read().decode('utf-8')
    print("响应数据：")
    print(response_data)

    # 尝试解析 JSON 数据
    result = json.loads(response_data)
    bond_data = result.get("data", {}).get("resultList", [])

    # 提取需要的字段
    parsed_data = []
    for bond in bond_data:
        parsed_data.append({
            "ISIN": bond.get("isin", ""),
            "Bond Code": bond.get("bondCode", ""),
            "Issuer": bond.get("entyFullName", ""),
            "Bond Type": bond.get("bondType", ""),
            "Issue Date": bond.get("issueStartDate", ""),
            "Latest Rating": bond.get("debtRtng", "")
        })

    # 创建 DataFrame
    df = pd.DataFrame(parsed_data)
    print("解析后的表格数据：")
    print(df)

    # 如果需要，可以保存为 CSV 文件
    df.to_csv("bond_data.csv", index=False)
    print("数据已保存到 bond_data.csv 文件中。")

except Exception as e:
    print(f"请求或解析失败：{e}")
