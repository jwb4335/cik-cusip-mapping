#!/usr/bin/python
import argparse
import csv
import os
from pathlib import Path

import pandas as pd
import requests



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filing", type=str)
    parser.add_argument("folder", type=str)

    user_agent = {"User-agent": "Mozilla/5.0"}

    args = parser.parse_args()
    filing = args.filing
    folder = args.folder

    to_dl = []
    with open("full_index.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if filing in row["form"]:
                to_dl.append(row)

    iss_cik = pd.read_stata("/Users/johnbarry/Dropbox/ceo_pay_competition/input_data/incentive_lab/US/CompanyFY.dta")
    
    iss_cik = iss_cik.drop_duplicates(subset = ['cik'])
    
    cik_list = pd.to_numeric(iss_cik['cik']).tolist()
    
    cik_list_sec = [(i,int(row["cik"].strip())) for (i,row) in enumerate(to_dl)]

    to_keep = [to_dl[i] for i in [i for (i,row) in enumerate(cik_list_sec) if row[1] in cik_list]]
    
    len_ = len(to_keep)
    
    for n, row in enumerate(to_keep):
        print(f"{n} out of {len_}")
        cik = row["cik"].strip()
        date = row["date"].strip()
        year = row["date"].split("-")[0].strip()
        month = row["date"].split("-")[1].strip()
        url = row["url"].strip()
        accession = url.split(".")[0].split("-")[-1]
        Path(f"./{folder}/{year}_{month}").mkdir(parents=True, exist_ok=True)
        file_path = f"./{folder}/{year}_{month}/{cik}_{date}_{accession}.txt"
        if os.path.exists(file_path):
            continue
        try:
            txt = requests.get(
                f"https://www.sec.gov/Archives/{url}", headers=user_agent, timeout=60
            ).text
            with open(file_path, "w", errors="ignore") as f:
                f.write(txt)
        except:
            print(f"{cik}, {date} failed to download")