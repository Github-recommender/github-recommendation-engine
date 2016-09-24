import pymongo, csv
from pymongo import MongoClient
from github3 import login as glin
from github3 import iter_user_repos
from bson.json_util import dumps
import numpy as np


client = MongoClient()
db = client.github
users = db.users
users.ensure_index('username',unique=True)

def build_model(user):
    #with open('languages.csv','rb') as f:
        #reader = csv.reader(f)
        #languages_list = list(reader)
    languages_list = ['', 'Shell', 'Java', 'HTML', 'Python', 'JavaScript', 'CSS', 'C']
    client = MongoClient()
    db = client.github
    repositories = db.repositories
    repoTable = np.empty((0,len(languages_list)))
    for repo in repositories.find():
        langArray = np.empty(len(languages_list))
        #langArray[0] = repo['repoName']
        i=0
        for language in languages_list:

            for key,value in repo['languages'].items():
                if key == language:
                    langArray[i]=value
            i=i+1
        np.append(repoTable,langArray)
        print langArray

    print repoTable
    np.savetxt("out.csv",repoTable,delimiter= ',')



def insert_train_data(user):
    kill = 0
    KILL = 24
    client = MongoClient()
    db = client.github
    repositories = db.repositories
    Languages = db.languages
    user1 = user.user()
    my_followers = (list(user1.iter_followers()))
    for f in my_followers:
        if kill == KILL:
            break
        user2=user.user(f)
        follower_followeres = (list(user2.iter_followers()))
        for ff in follower_followeres:
            if kill == KILL:
                break
            user3 = user.user(ff)

            #if ff not in my_followers:
            repo = list(user.iter_user_repos(user3))
            for rep in repo:
                kill = kill + 1
                print 'repo:', kill
                if kill == KILL:
                    break
                languages = list(rep.iter_languages())
                summ=0
                dictrepo = {
                    "repoName" : rep.full_name,
                    "languages":{}
                }
                no_of_stars = len(list(rep.iter_stargazers()))
                for l in languages:
                    summ=summ+int(l[1])

                langs = {}
                
                for l in languages:
                        langs.update({l[0]:str(l[1]/float(summ))})
                dictrepo["languages"] = langs
                dictrepo["stars"] = no_of_stars
                repositories.insert_one(dictrepo)
    #build_model(user)

def insert_repos(user, repos):
    username = user.user().login
    dictRepos = {}
    dictLang = {}
    for r in repos:
        #print r.full_name
        repo = {
            r.full_name:{}
        }
        repoDetails = {
            "languages":{}
        }
        languages = list(r.iter_languages())
        no_of_stars = len(list(r.iter_stargazers()))
        sum=0
        Lang = {}
        for l in languages:
            sum=sum+int(l[1])
        for l in languages:
            Lang = {l[0]:float(l[1])/sum}
            dictLang.update(Lang)
        repoDetails["languages"] = dictLang
        repoDetails["stars"] = no_of_stars
        repo[r.full_name] = repoDetails
        dictLang = {}
        #print repo
        dictRepos.update(repo)
    users.update({'username':username},{'username':username,'repos':dictRepos} , True)
    insert_train_data(user)



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
