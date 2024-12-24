import os
from app import app, authenticate
import pytest

@pytest.fixture(scope='class')
def setup_method():
    header={'Authorization':os.getenv('API_KEY')}
    testclient=app.test_client()
    yield testclient,header


class Test_app:
    
    @pytest.mark.app
    def test_coins_empty_header(self, setup_method):
        testclient,header=setup_method
        response=testclient.post('/coins', headers={})
        print(response.json)
        assert response.status_code==401
        assert response.json == {'error': 'Unauthorized'}
        response=testclient.get('/categories', headers={})
        print(response.json)
        assert response.status_code==401
        assert response.json == {'error': 'Unauthorized'}
        response=testclient.get('/coin/canada-ecoin', headers={})
        print(response.json)
        assert response.status_code==401
        assert response.json == {'error': 'Unauthorized'}
        response=testclient.post('/coin/market', headers={})
        print(response.json)
        assert response.status_code==401
        assert response.json == {'error': 'Unauthorized'}

    @pytest.mark.app
    def test_coins(self, setup_method):
        testclient,header=setup_method
        response=testclient.post('/coins', headers=header)
        print(response.json)
        assert response.status_code==200
        assert len(response.json)>=1

    @pytest.mark.app
    def test_coins_with_formdata(self, setup_method):
        testclient,header=setup_method
        data={'per_page':2,'page':1}
        response=testclient.post('/coins', headers=header, data=data)
        print(response.json)
        assert response.status_code==200
        assert len(response.json)>=1

    @pytest.mark.app
    def test_categories(self, setup_method):
        testclient,header=setup_method
        response=testclient.get('/categories', headers=header)
        print(response.json)
        assert response.status_code==200
        assert len(response.json)>=1
    
    @pytest.mark.app
    def test_coin_id(self, setup_method):
        testclient,header=setup_method
        response=testclient.get('/coin/canada-ecoin', headers=header)
        print(response.json)
        assert response.status_code==200
        assert len(response.json)>=1

    @pytest.mark.app
    def test_coin_id_market(self, setup_method):
        testclient,header=setup_method
        response=testclient.post('/coin/market', headers=header)
        print(response.json)
        assert response.status_code==400
        assert response.json == {'message': 'Please provide coin id'}

    @pytest.mark.app
    def test_coin_id_market_formdata(self, setup_method):
        testclient,header=setup_method
        data={'coin_id':'canada-ecoin','days':1,'vs_currency':'cad'}
        response=testclient.post('/coin/market', headers=header, data=data)
        print(response.json)
        assert response.status_code==200
        assert 'market_caps' in response.json.keys() and 'total_volumes' in response.json.keys() and 'prices' in response.json.keys()

