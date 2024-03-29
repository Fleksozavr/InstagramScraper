import json
import os
from instagrapi import Client
from concurrent.futures import ThreadPoolExecutor


def process_profile(account):
    cl = Client()
    try:
        cl.login(account["login"], account["password"])
        print(f'Успешный вход в аккаунт {account["login"]}!')

        media_pk = cl.media_pk_from_url(account["post_url"])
        media_info = cl.media_info(media_pk)

        matching_users = set()

        likers = cl.media_likers(media_pk)
        likers_info = [cl.user_info_by_username(liker_info.username) for liker_info in likers]

        for user_info in likers_info:
            if account["keyword"].lower() in user_info.biography.lower():
                matching_users.add(user_info.username)

        comments = cl.media_comments(media_pk)
        comments_info = [cl.user_info_by_username(comment.user.username) for comment in comments]

        for user_info in comments_info:
            if account["keyword"].lower() in user_info.biography.lower():
                matching_users.add(user_info.username)

        result_filename = os.path.join('results', f'{account["login"]}_results.txt')
        with open(result_filename, 'w') as result_file:
            if matching_users:
                print("\nНайдены совпадения среди лайкнувших или комментаторов. (В каталоге results)")
                for username in matching_users:
                    result_file.write(f"Найдено совпадение, никнейм: {username}\n")
            else:
                print("\nСовпадений среди лайкнувших и комментаторов не найдено.")
                result_file.write("Совпадений среди лайкнувших и комментаторов не найдено.\n")

    except Exception as e:
        print(f'Ошибка для аккаунта {account["login"]}: {e}')
        result_filename = f'{account["login"]}_results.txt'
        with open(result_filename, 'w') as result_file:
            result_file.write(f"Ошибка для аккаунта {account['login']}: {e}\n")


def read_accounts_from_file(filename):
    accounts = []
    file_path = os.path.join(os.path.dirname(__file__), filename)
    with open(file_path, 'r') as file:
        for line in file:
            account_info = line.strip().split(',')
            account = {
                "login": account_info[0],
                "password": account_info[1],
                "keyword": account_info[2],
                "post_url": account_info[3]
            }
            accounts.append(account)
    return accounts


def main():
    filename = 'data/accounts.txt'
    accounts = read_accounts_from_file(filename)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_profile, account) for account in accounts]

        for future in futures:
            future.result()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'Ошибка: {e}')