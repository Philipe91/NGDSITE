import urllib.request
import json

url = "https://api.telegram.org/bot8664876868:AAFpqSx2bzbf-G_mr3oqmrEDnK46nPCg-L0/getUpdates"
try:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
