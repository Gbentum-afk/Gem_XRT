import pandas as pd
import sys

basename, ext = sys.argv[1].split('.')[-2:]
start = int(sys.argv[2])
end = int(sys.argv[3])
pd.read_csv(sys.argv[1]).iloc[start:end + 1, :].to_csv(f"{basename}_{start}_{end}.{ext}")
