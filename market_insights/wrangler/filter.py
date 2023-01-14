import pandas as pd
import os

dirname = os.path.dirname(__file__)
filename=dirname+"/au_postcode_full.csv"

def getUniqueStateCode():
    pd_record=pd.read_csv(filename)
    unique_state_codes=pd_record['state_code'].unique()
    return unique_state_codes

def main():
    g = pd.read_csv(filename).groupby('state_code')
    print(getUniqueStateCode())
    print(g.ngroups)
    g.apply(lambda x: x.to_csv(r'./{}_postcode.csv'.format(x.name),index=False))
    
if __name__ == "__main__":
    main()