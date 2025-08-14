import time
import signal
from fetch_btc import fetch_btc_usd

INTERVAL = 300 # every 5 minutes
ERROR_BACKOFF_SEC = 30 #short delay on error
RUN = True

def stop_handler(sig, frame): #set RUN to false (stop loop)
    global RUN
    RUN = False
    print("Stopping loop")

# Handle CRTL-C and service stop | registers stop_handler with the OS
signal.signal(signal.SIGINT, stop_handler) #whenever CTR+C pressed, run stop_handler
try:
    signal.signal(signal.SIGTERM, stop_handler) #whenever stop signal (SIGTERM), run stop_handler
except AttributeError:
    pass

def sleep_check(seconds: int): # check if RUN is still TRUE every 1 second
    # Sleep in 1s chunks so CTRL-C stops quickly
    for _ in range(seconds): # _ is throwaway var
        if not RUN:
            break
        time.sleep(1)

while RUN:
    price = fetch_btc_usd()
    if price is not None:
        print(f"BTC (USD): ${price:,.2f}")
        sleep_check(INTERVAL)
    else:
        print("BTC fetch failed; retrying in 30 seconds...")
        sleep_check(ERROR_BACKOFF_SEC)