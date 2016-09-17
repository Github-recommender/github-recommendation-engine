import pymongo
from pymongo import MongoClient
from github3 import login as glin
from github3 import iter_user_repos
def create_user_profile(user):
    client = MongoClient()
    db = client.github
    db.users.ensure_index('username',unique=True)
    repos = list(user.iter_user_repos(user.user()))
    print repos
