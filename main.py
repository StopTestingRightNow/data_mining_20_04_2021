import os
import dotenv
from instagrapi import Client


def get_mut_following(init_username: str, client: Client, amount=20):

    user_id = cl.user_id_from_username(init_username)
    followers_dict = client.user_followers(user_id, amount=amount)
    following_dict = client.user_following(user_id, amount=amount)

    followers_set = set()
    following_set = set()

    for pk, follower in followers_dict.items():
        followers_set.add(follower.username)

    for pk, follower in following_dict.items():
        following_set.add(follower.username)

    return followers_set.intersection(following_set)


def find_chain(start_username: str, finish_username: str, client: Client, steps_limit=6, followers_limit=20):

    users_passed_set = set()
    users_working_set = {start_username, }

    for i in range(1, steps_limit):
        next_step_set = set()
        for username in users_working_set:
            new_batch = get_mut_following(username, client=cl, amount=followers_limit)
            if finish_username in new_batch:
                return i
            next_step_set.update(new_batch)
        users_passed_set.update(users_working_set)
        next_step_set = next_step_set - users_passed_set
        users_working_set = next_step_set

    return None


if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    username = os.getenv("INST_LOGIN")
    password = os.getenv("INST_PSWORD")

    start = "ligapodlecov1"
    finish = "ginstaboy"

    cl = Client()
    cl.login(username, password)

    result = find_chain("ligapodlecov1", "ginstaboy", client=cl, steps_limit=6, followers_limit=30)

    if result is not None:
        print(f"Chain found in {result} steps")
    else:
        print("Chain not found")
