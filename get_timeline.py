import requests
import time
import csv
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://ue-donnees-massive-et-cloud.ey.r.appspot.com/api/timeline"
USER_PREFIX = "user"

# Configuration STEP1
#CONCURRENT_LIST = [1, 10, 20, 50, 100, 1000]

# Configuration STEP2
CONCURRENT_LIST = [50]

# repetition
REPEATS = 3

# CSV file name STEP1
#CSV_FILE = "conc.csv"

# CSV file name STEP2 POST
#CSV_FILE = "post1000.csv"
# CSV file name STEP2 FANOUT
CSV_FILE = "fanout100.csv"

def run_test(concurrent):
    users = [f"{USER_PREFIX}{i}" for i in range(1, concurrent+1)]
    failed = 0
    times = []

    def fetch(user):
        nonlocal failed
        try:
            start = time.time()
            r = requests.get(BASE_URL, params={"user": user})
            r.raise_for_status()
            return (time.time() - start) * 1000
        except:
            failed = 1
            return 0

    with ThreadPoolExecutor(max_workers=concurrent) as executor:
        results = list(executor.map(fetch, users))
    
    avg_time = sum(results)/len(results)
    return avg_time, failed

with open(CSV_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["PARAM", "AVG_TIME", "RUN", "FAILED"])
    writer.writeheader()

    for param in CONCURRENT_LIST:
        for run in range(1, REPEATS+1):
            avg_time, failed = run_test(param)
            writer.writerow({"PARAM": param, "AVG_TIME": f"{avg_time:.0f}ms", "RUN": run, "FAILED": failed})
            print(f"Concurrent={param}, Run={run}, AVG_TIME={avg_time:.0f}ms, FAILED={failed}")
