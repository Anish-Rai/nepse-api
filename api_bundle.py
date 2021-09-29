from flask import Flask, jsonify, request, render_template
import data_scrapper as fetch

app = Flask(__name__)

####### Home page url
@app.route('/')
def home():
    return render_template('index.html')


####### Nepse and Sensitive api Index url
@app.route('/index')
def index():
    return fetch.indices()


# Live data
@app.route('/live_data')
def live_data():
    return fetch.live_data()

#Live data of individual company
@app.route('/company/<string:name>')
def company_detail(name):
    return fetch.get_company_detail(name)

#Closing prices of Nepse Listed Companies
@app.route('/today_price')
def today_price():
    return fetch.today_price()


#Market Status
@app.route('/market_status')
def market_status():
    return fetch.market_status()


@app.route('/loser_gainer')
def gainer_loser():
    return fetch.gainer_loser()


@app.route('/sub_indices')
def sub_indices():
    return fetch.sub_indices()



if __name__ == '__main__':
    app.run(debug=True)

'''############# Nepse api url
@app.route('/index/nepse')
def nepse_index():
    return jsonify(fetch.nepseIndex())

'''
'''# Sensitive api url
@app.route('/index/sensitive')
def sensitive_index():
    return jsonify(fetch.sensitiveIndex())'''