import json
import os
from instagrapi import Client


def login_and_get_post(cl, account):
        cl.login(account["login"], account["password"])
        print(f'Successful account login {account["login"]}!')

        media_pk = cl.media_pk_from_url(account["post_url"])

        return(media_pk)


def process_likers(account, cl):
    try:
        matching_users = set()
        
        media_pk = login_and_get_post(cl=Client() , account=account)

        likers = cl.media_likers(media_pk)
        likers_info = [cl.user_info_by_username_v1(liker_info.username) for liker_info in likers]

        for user_info in likers_info:
            if account["keyword"].lower() in user_info.biography.lower():
                matching_users.add(user_info.username)

        with open(result_filename, 'w') as result_file:
            if matching_users:
                print("\nНайдены совпадения среди лайкнувших. (В каталоге results)")
                for username in matching_users:
                    result_file.write(f"Найдено совпадение, никнейм: {username}\n")
            else:
                print("\nСовпадений среди лайкнувших не найдено.")
                result_file.write("Совпадений среди лайкнувших не найдено.\n")

    except Exception as err:
        error_text = (f'Error for account {account["login"]}: {err}')
        print(error_text)
        result_filename = f'{account["login"]}_results.txt'

        with open(result_filename, 'w') as result_file:
            result_file.write("error_text\n")


def process_comments(account, cl):
    try:
        matching_users = set()

        media_pk = login_and_get_post(cl=Client() , account=account)

        comments = cl.media_comments(media_pk)
        comments_info = [cl.user_info_by_username(comment.user.username) for comment in comments]

        for user_info in comments_info:
            if account["keyword"].lower() in user_info.biography.lower():
                matching_users.add(user_info.username) 

        with open(result_filename, 'w') as result_file:
            if matching_users:
                print("\nНайдены совпадения среди комментаторов. (В каталоге results)")
                for username in matching_users:
                    result_file.write(f"Найдено совпадение, никнейм: {username}\n")
            else:
                print("\nСовпадений среди комментаторов не найдено.")
                result_file.write("Совпадений среди комментаторов не найдено.\n")
        

    except Exception as err:
        error_text = (f'Error for account {account["login"]}: {err}')
        print(error_text)
        result_filename = f'{account["login"]}_results.txt'

        with open(result_filename, 'w') as result_file:
            result_file.write("error_text\n")


def process_profile(account, cl):
    try:
        cl.login(account["login"], account["password"])
        print(f'Успешный вход в аккаунт {account["login"]}!')

        media_pk = cl.media_pk_from_url(account["post_url"])
        media_info = cl.media_info(media_pk)

        matching_users = set()

        likers = cl.media_likers(media_pk)
        likers_info = [cl.user_info_by_username_v1(liker_info.username) for liker_info in likers]

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
    with open(filename, 'r') as accounts_file:
        data = json.load(accounts_file)
        for account_data in data:
            account = {
                "login": account_data.get("login"),
                "password": account_data.get("password"),
                "keyword": account_data.get("keyword"),
                "postlink": account_data.get("postlink")
            }
            accounts.append(account)
            return accounts


def main():
    filename = 'data/accounts.json'
    accounts = read_accounts_from_file(filename)


    print("=================================")
    print('Выберите действие:\n 1 - Поиск лайкнувших\n 2 - Поиск комментаторов\n 3 - 1 и 2 пункт (unstable) ')
    print("=================================")
    choice = int(input('Your choice: '))
    if choice == 1:
        print('The process_likers function has been run.')
        for account in accounts: process_likers(account, cl=Client())
    elif choice == 2:
        print('The process_comments function has been run.')
        for account in accounts: process_comments(account, cl=Client())
    elif choice == 3:
        print('The process_profile function has been run.')
        for account in accounts: process_profile(account, cl=Client())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'Ошибка: {e}')