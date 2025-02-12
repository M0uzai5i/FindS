import os
import re
import sys

# 定义正则表达式
patterns = {
    "大陆手机号": r"\b1[3456789]\d{9}\b",
    "身份证": r"\b\d{17}[\dXx]\b",
    "邮箱": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "银行卡": r"\b\d{16,19}\b",
    "域名": r"(?i)\b(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|io|co|edu|gov|mil|biz|info|me|us|ca|uk|de|fr|it|es|au|nz|jp|kr|cn|ru|br|in|mx|nl)\b",
    "路径": r"(?:https?://|/|\.\./|\./|/[\w-]+)/(?:[\w/.?%&=-]*|[\w-]+)",
    "URL": r"(?i)\b((?:https?|ftp|file):\/\/[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,63}\b(?:[-a-zA-Z0-9@:%_\+.~#?&\/=]*))\b",
    "JWT": r"\bey[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\b",
    "JDBC": r"jdbc:[a-zA-Z]+:\/\/[^\s]*",
    "authHeader": r"(?i)\bAuthorization:\s*(?:Bearer|Basic|Digest)\s+(?:[A-Za-z0-9-._~+/]+=*|[\w%]{2}==)\b",
    "账户密码": r"(?:username|user|account)\s*[:=]\s*['\"](.*?)['\"]\s*,\s*(?:password|pass)\s*[:=]\s*['\"](.*?)['\"]",
    "ticket": r"\bjsapi_ticket\b",
    "加密算法": r"(?i)\b(AES|DES|3DES|RC4|RSA|ECC|SM2|SM3|SM4|Blowfish|HMAC)\b",
    "密钥": r"(?i)(?:encryption|secret|private|api|auth|access|key)\s*[:=]\s*['\"]?([0-9a-fA-F]{32,})['\"]?",
    "偏移量": r"(?i)(?:iv|offset|init_vector)\s*[:=]\s*['\"]?([0-9a-fA-F]{8,})['\"]?",
    "swagger": r"(?i)\b((?:https?://)?(?:[a-zA-Z0-9-\.]+)\/(?:v1|v2|v3|docs|swagger|apidocs|api-docs|open-api)?\/?(swagger|api-docs)(?:\.json)?)\b",
    "oss": r"https?://[^\'\")\s]*oss[^\'\")\s]+",
    "access_key": r"(?i)\baccess[_]?key\s*[:=]\s*['\"]([^'\"]+)['\"]",
    "oss_key": r"(?i)\boss\s*[_\s]*(?:key)?\s*[=:]\s*['\"]([A-Z0-9]+)['\"]",
    "apikey": r"(?i)\bapi[_]?key\s*[=:]\s*['\"]([^'\"]+)['\"]",
    "apisecret": r"(?i)\bapi[_]?secret\s*[=:]\s*['\"]([^'\"]+)['\"]",
    "app_key": r"(?i)\bAppKey\s*:\s*['\"]([^'\"]+)['\"]",
    "app_secret": r"(?i)\bAPPSECRET\s*:\s*['\"]([^'\"]+)['\"]",
    "rsa_public_keys": r"-----BEGIN(?:\s+\w+)?\s+PUBLIC\s+KEY-----\s*(.*?)\s*-----END(?:\s+\w+)?\s+PUBLIC\s+KEY-----",
    "rsa_private_keys": r"-----BEGIN(?:\s+RSA)?\s+PRIVATE\s+KEY-----\s*(.*?)\s*-----END(?:\s+RSA)?\s+PRIVATE\s+KEY-----"
}

# 遍历文件夹并查找匹配
def search_files(directory):
    results = set()  # 使用集合来存储结果以去重
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for name, pattern in patterns.items():
                    matches = re.findall(pattern, content)
                    for match in matches:
                        # 添加文件路径信息
                        results.add(f"{name}: {match}               in {file_path}")
    return results

# 将结果写入result.txt
def write_results(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for result in sorted(results):  # 排序后写入文件
            f.write(result + "\n")

if __name__ == "__main__":
    # 从命令行参数获取目录
    if len(sys.argv) > 1:
        directory_to_search = sys.argv[1]
    else:
        directory_to_search = "."  # 默认当前目录

    output_file = "result.txt"
    results = search_files(directory_to_search)
    write_results(results, output_file)
