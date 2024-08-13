#!/bin/python
import argparse
import csv
import os

import pandas as pd
import requests

user_agent = {"User-agent": "Rice University jb235@rice.edu",'Accept-Encoding':'gzip, deflate','Host':'www.sec.gov'}


with open(f"master.idx", "wb") as f:
    for year in range(2023, 2024):
        for q in range(1, 5):
            print(year, q)
            content = requests.get(
                f"https://www.sec.gov/Archives/edgar/full-index/{year}/QTR{q}/master.idx",
                headers=user_agent,
            ).content
            f.write(content)

with open("full_index.csv", "w", errors="ignore") as csvfile:
    wr = csv.writer(csvfile)
    wr.writerow(["cik", "comnam", "form", "date", "url"])
    with open("master.idx", "r", encoding="latin1") as f:
        for r in f:
            if ".txt" in r:
                wr.writerow(r.strip().split("|"))
