import requests as req
import pytest


def test_server_home():
    response = req.get('localhost:5000/')
    assert response.status_code == 200
