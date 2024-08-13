import sys

import pandas as pd

files = sys.argv[1:-1]

save = sys.argv[-1]

print(files)
print(save)

df = [pd.read_csv(f, names=['f', 'cik', 'cusip','comnam_sec']).dropna() for f in files]
df = pd.concat(df)

df['leng'] = df.cusip.map(len)

df = df[(df.leng == 6) | (df.leng == 8) | (df.leng == 9)]

df['cusip6'] = df.cusip.str[:6]

df = df[df.cusip6 != '000000']
df = df[df.cusip6 != '0001pt']

df['cusip8'] = df.cusip.str[:8]

df.cik = pd.to_numeric(df.cik)

df['ym'] = df['f'].str.split("/").str[1].str.split("_")
df['year'] = pd.to_numeric(df['ym'].str[0])
df['month'] =  pd.to_numeric(df['ym'].str[1])

df = df[['cik'] + [x for x in df.columns if 'cusip' in x] + ['comnam_sec','year','month']]
df = df.drop_duplicates(subset = ['cik','year','month','cusip8'])
df = df.sort_values(by = ['cik','year','month']).reset_index(drop=True)



df.to_csv(save)