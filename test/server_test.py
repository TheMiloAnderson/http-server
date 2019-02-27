import requests as req
import pytest

base_url = 'http://localhost:5000'


def test_server_home():
    response = req.get(base_url)
    assert response.status_code == 200
    assert '<a href="/cow">cowsay</a>' in str(response.text)


def test_server_msg():
    response = req.get(base_url + '/cows?msg=heeeey')
    assert response.status_code == 200
    assert 'heeeey' in str(response.text)


def test_server_no_msg():
    response = req.get(base_url + '/cows')
    assert response.status_code == 400


def test_server_bad_params():
    response = req.get(base_url + '/cows?nth=bam&wut=hey')
    assert response.status_code == 400


def test_server_bad_route():
    response = req.get(base_url + '/horses')
    assert response.status_code == 404


def test_server_post():
    # import pdb; pdb.set_trace()
    data = {b'msg', b'We are doing this thing!'}
    thing = base_url + '/cows'
    response = req.post(thing.encode(), data)
    assert response.status_code == 200
    assert '< We are doing this thing! >' in str(response.text)

@pytest.mark.skip('pending')
def test_server_post_bad_route():
    data = {'msg', 'We are doing this thing!'}
    response = req.post(base_url + '/pigs', data)
    assert response.status_code == 404
