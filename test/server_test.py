import requests as req
import pytest

base_url = 'http://localhost:5000'


#@pytest.mark.skip('pending')
def test_server_home():
    response = req.get(base_url)
    assert response.status_code == 200
    assert '<a href="/cow">cowsay</a>' in str(response.text)


#@pytest.mark.skip('pending')
def test_server_msg():
    response = req.get(base_url + '/cows?msg=heeeey')
    assert response.status_code == 200
    assert 'heeeey' in str(response.text)


#@pytest.mark.skip('pending')
def test_server_no_msg():
    response = req.get(base_url + '/cows')
    assert response.status_code == 400


#@pytest.mark.skip('pending')
def test_server_bad_params():
    response = req.get(base_url + '/cows?nth=bam&wut=hey')
    assert response.status_code == 400


#@pytest.mark.skip('pending')
def test_server_bad_route():
    response = req.get(base_url + '/horses')
    assert response.status_code == 404


#@pytest.mark.skip('pending')
def test_server_post():
    #import pdb; pdb.set_trace()
    params = {'msg': 'We are doing this thing!'}
    response = req.post(base_url + '/cows', params=params)
    assert response.status_code == 200
    assert '< We are doing this thing! >' in str(response.text)


#@pytest.mark.skip('pending')
def test_server_post_bad_route():
    params = {'msg': 'We are doing this thing!'}
    response = req.post(base_url + '/pigs', params=params)
    assert response.status_code == 404
