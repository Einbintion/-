import csv
import ssl
import urllib.request
import urllib.parse
import json

# 目标URL
url = 'https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN'

# 定义Cookies
cookies = {
    '_ulta_id.ECM-Prod.ccc4': '83e23fd70be13020',
    'ags': 'b168c5dd63e5c0bebdd4fb78b2b4704a',
    'apache': 'bbfde8c184f3e1c6074ffab28a313c87',
    '_ulta_ses.ECM-Prod.ccc4': '8c32d2e45c7a8b03',
    'AlteonP10': 'CdZpLyw/F6zXyStaKUWoUQ$$',
}

# 构造Cookie字符串
cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])

# 定义Headers
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://iftp.chinamoney.com.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://iftp.chinamoney.com.cn/english/bdInfo/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Cookie': cookie_str,
}

# 设置SSL上下文以允许旧版TLS连接
ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT

# 初始化变量
total_pages = 8  # 总页数
all_parsed_data = []

# 循环获取每一页的数据
for page_no in range(1, total_pages + 1):
    # 定义POST数据
    data = {
        'pageNo': str(page_no),
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

    # 编码POST数据
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')

    # 创建请求对象
    req = urllib.request.Request(url, data=encoded_data, headers=headers)

    try:
        # 发送请求并获取响应
        with urllib.request.urlopen(req, context=ctx) as response:
            res_data = response.read().decode('utf-8')

        # 解析JSON响应
        js_res = json.loads(res_data)
        result_list = js_res["data"]["resultList"]

        # 解析数据
        for item in result_list:
            parsed_item = {
                "ISIN": item.get("isin", ""),
                "Bond Code": item.get("bondCode", ""),
                "Issuer": item.get("entyFullName", ""),
                "Bond Type": item.get("bondType", ""),
                "Issue Date": item.get("issueStartDate", ""),  # 使用发行起始日期作为 Issue Date
                "Latest Rating": item.get("debtRtng", "")
            }
            all_parsed_data.append(parsed_item)

        print(f"已成功获取第 {page_no} 页数据")
    except Exception as e:
        print(f"获取第 {page_no} 页数据时发生错误: {e}")

# 定义CSV文件路径和列名
csv_file_path = "bonds_data_all.csv"
fieldnames = ["ISIN", "Bond Code", "Issuer", "Bond Type", "Issue Date", "Latest Rating"]

# 写入CSV文件
with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # 写入表头
    writer.writerows(all_parsed_data)  # 写入数据行

print(f"所有数据已成功保存到 {csv_file_path}")
