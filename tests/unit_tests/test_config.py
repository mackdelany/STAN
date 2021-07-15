
from fixtures import app, dev_client, prod_client

def test_dev_config(dev_client):
    assert app.config['TESTING'] == True
    assert app.config['DEBUG'] == True

def test_prod_config(prod_client):
    assert app.config['TESTING'] == True
    assert app.config['DEBUG'] == False