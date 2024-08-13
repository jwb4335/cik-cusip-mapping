import os
os.chdir("/Users/johnbarry/Documents/Github/cik-cusip-mapping/")

import subprocess

# subprocess.run(['python3','dl_idx.py'])

# subprocess.run(['python3','dl.py',"13G","13G"])

# subprocess.run(['python3','dl.py',"13D","13D"])

subprocess.run(['python3','parse_cusip.py',"13D"])

subprocess.run(['python3', 'post_proc.py', '13G.csv', "13D.csv", 'cik_cusip_year_month.csv'])