from flask import Flask,flash,render_template,redirect,url_for,json,make_response,request
from github3 import login as glin
from helpers import create_user_profile
from multiprocessing import Pool


app = Flask(__name__)
app.secret_key = 'aBcDeFg1@3$5'




@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html'), 500

@app.route("/")
def mainInit():
	return render_template('home.html', title='Home')


@app.route("/login", methods = ['POST'])
def login():
    if request.method == 'POST':
        username = str(request.form['user'])
        password = str(request.form['password'])
        user = glin(username, password=password)
        create_user_profile(user)
        return render_template("recommendation.html")


@app.route("/api/recommendation")
def apiRecommendation():
    pass


@app.route("/recommendation")
def recommendation():
    return render_template("recommendation.html")

if __name__ == "__main__":
    app.run(debug = True)
