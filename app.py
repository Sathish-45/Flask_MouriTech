import os
import requests
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

BASE_URL=os.getenv('BASE_URL')
API_KEY=os.getenv('API_KEY')

# Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Crypto API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# Helper function for authentication
def authenticate():
    key = "Bearer "+str(request.headers.get("Authorization"))
    if not key or key != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/coins', methods=['POST'])
def list_all_coins():
    auth_reponse=authenticate()
    if auth_reponse:
        return auth_reponse
    per_page=request.form.get('per_page',10, type=int)
    page=request.form.get('page',1,type=int)
    
    list_coins=requests.get(url=f"{BASE_URL}/coins/list", params={'per_page':per_page,'page':page})
    return jsonify(list_coins.json()),200

@app.route('/categories', methods=['GET'])
def list_coins_categories():
    auth_reponse=authenticate()
    if auth_reponse:
        return auth_reponse
    list_categories=requests.get(url=f"{BASE_URL}/coins/categories")
    return jsonify(list_categories.json()),200

@app.route('/coin/<id>', methods=['GET'])
def coin(id):
    auth_reponse=authenticate()
    if auth_reponse:
        return auth_reponse
    list_categories=requests.get(url=f"{BASE_URL}/coins/{id}")
    return jsonify(list_categories.json()),200

@app.route('/coin/market', methods=['POST'])
def market_data():
    auth_reponse=authenticate()
    if auth_reponse:
        return auth_reponse
    
    vs_currency=request.form.get('vs_currency','cad')
    days=request.form.get('days',10,type=int)
    coin_id=request.form.get('coin_id')

    if coin_id:
        market_data=requests.get(url=f'{BASE_URL}/coins/{coin_id}/market_chart',params={'vs_currency':vs_currency,'days':days})
        return jsonify(market_data.json()),200
    else:
        return jsonify(message='Please provide coin id'), 400

if __name__=='__main__':
    app.run(debug=True)