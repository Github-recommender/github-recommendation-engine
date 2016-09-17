import pymongo
from pymongo import MongoClient
from github3 import login as glin
from github3 import iter_user_repos
from bson.json_util import dumps




client = MongoClient()
db = client.github
users = db.users
users.ensure_index('username',unique=True)
'''
'''


def insert_repos(user, repos):
    username = user.user().login
    dictRepos = {}
    dictLang = {}
    for r in repos:
        #print r.full_name
        repo = {
            r.full_name:{

            }
        }
        languages = list(r.iter_languages())
        sum=0
        Lang = {}
        for l in languages:
            sum=sum+int(l[1])
        for l in languages:
            Lang = {l[0]:float(l[1])/sum}
            dictLang.update(Lang)
        repo[r.full_name] = dictLang
        dictLang = {}
        #print repo
        dictRepos.update(repo)
    users.update({'username':username},{'username':username,'repos':dictRepos} , True)
    print type(dictRepos)
def create_user_profile(user):
    client = MongoClient()
    db = client.github
    users = db.users

    try:
        users.insert_one({'username':user.user().login})
    except:
        pass
    repos = list(user.iter_user_repos(user.user()))
    insert_repos(user,repos)
