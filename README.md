# Massive Data Project

Link of active server for ptoject [TinyInstagram](https://github.com/momo54/massive-gcp) : https://ue-donnees-massive-et-cloud.ey.r.appspot.com/

## How to start

* Set environment variable:
  ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="../pathFileCredential.json"
  ```

* Populate database (we use seed.py file):
  ```bash
    python seed.py --users 1000 --posts 50 --follows-min 1 --follows-max 20
  ```

## Step 1 : Scaling up the load

We need to measure the average execution time of a timeline request (ms) for the following configurations: 1, 10, 20, 50, 100, 1000 simultaneous distinct users

So we use a simple script to do that :
```bash
  python step1.py
```

We generate conc.csv

## Step 2 : Scaling up based on data size

Face 50 richest simultaneously:

* Set the number of followers to 20 and vary the number of posts: 10 , 100, 1000 posts per user
  ```bash
    python step2_post.py
  ```

* Set the number of posts per user to 100 and vary the number of followers: 10, 50, 100
  ```bash
    python step2_fanout.py
  ```