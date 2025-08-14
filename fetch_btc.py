from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv # load CMC api key into env vars
import os

from urllib3.exceptions import HTTPError

load_dotenv() # read .env once when the module loads
api_key = os.getenv('CMC_API_KEY')
url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
headers = { 'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key,} # standard CMC headers

def fetch_btc_usd() -> float:
    """
        Return current BTC spot price in USD as a float.
        Raises requests.HTTPError on HTTP failures (e.g., 401/429/500).
        """
    parameters = {'symbol':'BTC', 'convert':'USD'}
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        # Extract the BTC price
        btc_price = float(data["data"]["BTC"][0]["quote"]["USD"]["price"])
        return btc_price
    except (HTTPError, ConnectionError, Timeout, TooManyRedirects) as e:
        print('Error fetching BTC price:',e)
        return None


print(f"BTC (USD): ${fetch_btc_usd():,.2f}")
