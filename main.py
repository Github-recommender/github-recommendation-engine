from flask import Flask,flash,render_template,redirect,url_for,json,make_response,request


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

if __name__ == "__main__":
    app.run(debug = True)
