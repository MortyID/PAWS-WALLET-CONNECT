import base58
import nacl.signing
import nacl.encoding
import requests
import time
import urllib3
from colorama import init, Fore, Style
import os
import sys
from urllib.parse import unquote,parse_qs
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)
red = Fore.LIGHTRED_EX
blue = Fore.LIGHTBLUE_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
black = Fore.LIGHTBLACK_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL
magenta = Fore.LIGHTMAGENTA_EX
proxy = {
    "http": "https://username:password@ip:port",
    "https": "http://username:password@ip:port",
}

def get_message(token):
    url = "https://api.paws.community/v1/wallet/solana/payload"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    start_time = time.time()
    while True:
        try:
            response = requests.get(url, headers=headers,proxies=proxy,verify=False , timeout=10)
            response.raise_for_status()
            data = response.json()
            return data['data']
        except requests.exceptions.RequestException as e:
            pass
        if time.time() - start_time > 30:
            print("Timeout reached after 30 seconds")
            return None 

def bind_wallet_sol(signature_base58, public_key, payload_token, header_token):
    url = "https://api.paws.community/v1/wallet/solana/check_proof"
    payload = {
        "signature": signature_base58,
        "publicKey": public_key,
        "token": payload_token
    }
    headers = {
        "Authorization": f"Bearer {header_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    start_time = time.time()
    while True:
        try:
            response = requests.post(url, json=payload, headers=headers,proxies=proxy,verify=False , timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            pass
        if time.time() - start_time > 30:
            print("Timeout reached after 30 seconds")
            return None    

def auth(query):
    url = "https://api.paws.community/v1/user/auth"
    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://app.paws.community',
    'priority': 'u=1, i',
    'referer': 'https://app.paws.community/',
    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    }

    json_data = {
        'data': f'{query}',
    }
    start_time = time.time()
    while True:
        try:
            response = requests.post('https://api.paws.community/v1/user/auth', headers=headers, json=json_data,proxies=proxy,verify=False)
            if response.status_code == 201:
                response = response.json()
                return response
            else:
                return None
        except requests.exceptions.RequestException as e:
            pass
        if time.time() - start_time > 30:
            print("Timeout reached after 30 seconds")
            return None 
def load_accounts(file_path):
    try:
        with open(file_path, 'r') as f:
            data = [line.strip() for line in f if line.strip()]
        return data
    except FileNotFoundError:
        print(f"{red}Error: File '{file_path}' not found.{reset}")
        sys.exit(1)
def save_text(filename, text):
    try:
        with open(filename, 'a') as file:
            file.write(text)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def main():
    file_path = 'query.txt'
    emails = load_accounts(file_path)
    if not emails:
        print(f"{red}No accounts found in the file.{reset}")
        sys.exit(1)

    os.system('cls' if os.name == 'nt' else 'clear')

    banner = f"""
    {magenta}┳┓┏┓┏┓┏┓┏┳┓┳┳┓┏┓┏┳┓┏┓  {white}NextMate.ai Auto Spin
    {magenta}┃┃┣  ┃┃  ┃ ┃┃┃┣┫ ┃ ┣   {green}Author : {white}MortyID
    {magenta}┛┗┗┛┗┛┗┛ ┻ ┛ ┗┛┗ ┻ ┗┛  {white}Github : {green}https://github.com/MortyID
    """
    print(banner)
    total_balances = 0
    for i, query in enumerate(emails, start=1):
        decode_query = unquote(query)
        parse_query = parse_qs(decode_query)
        user_data = json.loads(parse_query["user"][0])
        username = user_data.get("username", None)
        print(f"{magenta}==================== {i} ====================")
        signing_key = nacl.signing.SigningKey.generate()
        verify_key = signing_key.verify_key
        public_key = base58.b58encode(verify_key.encode()).decode('utf-8')
        private_key = base58.b58encode(signing_key.encode()).decode('utf-8')
        getdata = auth(query)
        if getdata != None:
            user_data = next((item for item in getdata['data'] if isinstance(item, dict) and 'userData' in item), {})
            get_balance = next((item for item in getdata['data'] if isinstance(item, dict) and 'gameData' in item), {})
            firstname = user_data.get("userData", {}).get("firstname")
            balance = get_balance.get("gameData", {}).get("balance")
            wallet = user_data.get('userData', {}).get('wallet')
            print(f"{green}[ 😋 ] Name          : {firstname}")
            print(f"{green}[ 😋 ] Username      : {username}")
            print(f"{green}[ 💵 ] Balance       : {balance}")
            account_info = f"""
    ---- User: Account #{i} {username} | {firstname} ----
    Private Key : {private_key}
    Solana Address : {public_key}
    """
            save_text("privatekey.txt",account_info)
            save_text("walletsol.txt",f"{public_key}\n")
            
            header_token = getdata["data"][0]
            message = get_message(header_token)
            if message != None:
                message_bytes = message.encode('utf-8')
                signature = signing_key.sign(message_bytes).signature
                signature_base58 = base58.b58encode(signature).decode('utf-8')
                verify_key = nacl.signing.VerifyKey(base58.b58decode(public_key))
                result = verify_key.verify(message_bytes, signature)
                bind_response = bind_wallet_sol(signature_base58, public_key, message, header_token)
                if bind_response.get('success') and bind_response.get('data'):
                    print(f"{green}[ 🔗 ] Status Wallet : Successfully Connect Wallet.")
                    print(f"{yellow}[ 💼 ] Wallet        : {yellow}{public_key}{reset}")

if __name__ == "__main__":
    main()