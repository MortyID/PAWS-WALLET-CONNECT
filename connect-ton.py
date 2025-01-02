import json
import requests
import time
import urllib3
from colorama import init, Fore, Style
from mnemonic import Mnemonic
from nacl.signing import SigningKey
from hashlib import sha256
import base58
import tqdm
from tonsdk.contract.wallet import Wallets, WalletVersionEnum
import os
import sys
from urllib.parse import unquote,parse_qs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)





proxy = {
    "http": "https://username:password@ip:port",
    "https": "http://username:password@ip:port",
}

red = Fore.LIGHTRED_EX
blue = Fore.LIGHTBLUE_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
black = Fore.LIGHTBLACK_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL
magenta = Fore.LIGHTMAGENTA_EX

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
            response = requests.post('https://api.paws.community/v1/user/auth', headers=headers, json=json_data,proxies=proxy,verify=False , timeout=10)
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

def connectWallet(token, mywallet):
    headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'Bearer {token}',
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
        'wallet': f'{mywallet}',
    }
    start_time = time.time()
    while True:
        try:
            response = requests.post('https://api.paws.community/v1/user/wallet', headers=headers, json=json_data,proxies=proxy,verify=False , timeout=10)
            if response.status_code == 201:
                return response
            else:
                return None
        except requests.exceptions.RequestException as e:
            pass
        if time.time() - start_time > 30:
            print("Timeout reached after 30 seconds")
            return None
def main():
    try:
        file_path = 'query.txt'
        emails = load_accounts(file_path)
        if not emails:
            print(f"{red}No accounts found in the file.{reset}")
            sys.exit(1)
    
        os.system('cls' if os.name == 'nt' else 'clear')
    
        banner = f"""
        {magenta}┏┓┏┓┓ ┏┏┓  {white}PAWS Auto Connect Wallet
        {magenta}┃┃┣┫┃┃┃┗┓  {green}Author : {white}MortyID
        {magenta}┣┛┛┗┗┻┛┗┛  {white}Github : {green}https://github.com/MortyID
        """
        print(banner)
        total_balances = 0
        for i, query in enumerate(emails, start=1):
            decode_query = unquote(query)
            parse_query = parse_qs(decode_query)
            user_data = json.loads(parse_query["user"][0])
            username = user_data.get("username", None)
            print(f"{magenta}==================== {i} ====================")
            getdata = auth(query)
            if getdata != None:
                token = getdata["data"][0]
                user_data = next((item for item in getdata['data'] if isinstance(item, dict) and 'userData' in item), {})
                get_balance = next((item for item in getdata['data'] if isinstance(item, dict) and 'gameData' in item), {})
                firstname = user_data.get("userData", {}).get("firstname")
                balance = get_balance.get("gameData", {}).get("balance")
                wallet = user_data.get('userData', {}).get('wallet')
                print(f"{green}[ 😋 ] Name          : {firstname}")
                print(f"{green}[ 😋 ] Username      : {username}")
                print(f"{green}[ 💵 ] Balance       : {balance}")
                total_balances += balance
                if wallet is None or wallet == '':
                    mnemonics, pub_k, priv_k, wallet = Wallets.create(WalletVersionEnum.v4r2, workchain=0)
                    phrase = ' '.join(mnemonics)
                    mywallet = wallet.address.to_string(True, True, False)
                    konekin = connectWallet(token, mywallet)
                    account_info = f"""
    ---- User: Account #{i} {username} | {firstname} ----
    Mnemonic Phrase: {phrase}
    TON Wallet Address: {mywallet}
    """
                    save_text("pharse.txt",account_info)
                    save_text("wallet.txt",f"{mywallet}\n")
                    if konekin != None:
                        print(f"{green}[ 🔗 ] Status Wallet : Successfully Connect Wallet.")
                        print(f"{yellow}[ 💼 ] Wallet        : {yellow}{mywallet}{reset}")
                    else:
                        print(f"{green}[ 🔗 ] Status Wallet : Failed Connect Wallet.")
                        print(f"{yellow}[ 💼 ] Wallet        : {yellow}{mywallet}{reset}")
                else:
                    print(f"{green}[ 🔗 ] Status Wallet : Already Connected.")
                    print(f"{yellow}[ 💼 ] Wallet        : {yellow}{wallet}{reset}")
            else:
                print(f"{red}[#] Failed Auth Accounts.{reset}")
        formatted_balance = f"{total_balances:,.2f}"
        print(f"{magenta}[ 💵 ] Total Balance : {formatted_balance} PAWS")
        
    except KeyboardInterrupt:
        print(f"\n{magenta}========== Program Stopped =========={reset}")
    
if __name__ == "__main__":
    main()