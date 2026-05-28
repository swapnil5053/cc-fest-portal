from app.main import app
from starlette.testclient import TestClient

client = TestClient(app)
try:
    response = client.get("/")
    print("STATUS", response.status_code)
    print(response.text[:2000])
except Exception as e:
    import traceback
    traceback.print_exc()
