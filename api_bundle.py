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
    return jsonify(fetch.nepseIndex(), fetch.sensitiveIndex())


############# Nepse api url
@app.route('/index/nepse')
def nepse_index():
    return jsonify(fetch.nepseIndex())


# Sensitive api url
@app.route('/index/sensitive')
def sensitive_index():
    return jsonify(fetch.sensitiveIndex())


# Live data
@app.route('/live_data')
def live_data():
    return fetch.live_data()

#Live data of individual company
@app.route('/company_details/<string:name>')
def company_detail(name):
    return fetch.get_company_detail(name)

if __name__ == '__main__':
    app.run(debug=True)
