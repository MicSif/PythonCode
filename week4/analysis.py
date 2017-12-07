import json
import pandas as pd
def analysis(json_file,user_id):
    df=pd.read_json(json_file)
    if len(df[df['user_id']==int(user_id)]) != 0:
        result=df[df['user_id']==int(user_id)]['minutes']
        return len(result),result.sum()
    else:
        return 0,0
if __name__=='__main__':
    times,minutes=analysis('user_study.json','4567657')
    print(times,minutes)
