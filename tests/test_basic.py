import pytest
import sys
import os
import concurrent.futures

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

long_url = "https://www.thehindu.com/sport/other-sports/sindhu-downs-miyazaki-satwik-chirag-duo-advances-at-china-open/article69845738.ece?cx_testId=11&cx_testVariant=cx_1&cx_artPos=1&cx_experienceId=EXKWL3XAQS9E&cx_experienceActionId=showRecommendationsJFMEXHRNTMNR11#cxrecs_s"

def test_shorten_url(client):
    res = client.post("/api/shorten", json={"url": long_url})
    assert res.status_code == 201
    assert "short_code" in res.get_json()

def test_invalid_url(client):
    res = client.post("/api/shorten", json={"url": "invalid-url"})
    assert res.status_code == 400

def test_redirect(client):
    res = client.post("/api/shorten", json={"url": long_url})
    short_code = res.get_json()["short_code"]
    redirect_res = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.location == long_url

def test_stats(client):
    res = client.post("/api/shorten", json={"url": long_url})
    short_code = res.get_json()["short_code"]
    client.get(f"/{short_code}")  # simulate a click
    stats_res = client.get(f"/api/stats/{short_code}")
    data = stats_res.get_json()
    assert data["clicks"] == 1
    assert data["url"] == long_url

def test_not_found(client):
    res = client.get("/api/stats/notexist")
    assert res.status_code == 404

def test_real_hindu_article(client):
    res = client.post("/api/shorten", json={"url": long_url})
    assert res.status_code == 201
    data = res.get_json()
    assert "short_code" in data
    short_code = data["short_code"]
    assert len(short_code) == 6
    assert short_code.isalnum()

    redirect_res = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.location == long_url

    stats_res = client.get(f"/api/stats/{short_code}")
    stats = stats_res.get_json()
    assert stats_res.status_code == 200
    assert stats["url"] == long_url
    assert stats["clicks"] == 1
    assert "created_at" in stats

def test_concurrent_redirects():
    app.config['TESTING'] = True
    with app.test_client() as client:
        res = client.post("/api/shorten", json={"url": long_url})
        assert res.status_code == 201
        short_code = res.get_json()["short_code"]

    def simulate_click():
        with app.test_client() as thread_client:
            return thread_client.get(f"/{short_code}", follow_redirects=False)

    NUM_CLICKS = 20
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(simulate_click) for _ in range(NUM_CLICKS)]
        results = [f.result() for f in futures]

    for r in results:
        assert r.status_code == 302

    with app.test_client() as stats_client:
        stats_res = stats_client.get(f"/api/stats/{short_code}")
        stats = stats_res.get_json()
        assert stats["clicks"] == NUM_CLICKS
