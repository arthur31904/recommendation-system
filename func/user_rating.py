import pandas as pd


class UserRating(object):
    def __init__(self,fpath):
        self.df = pd.read_csv(fpath)
    def get_user_watched_ids(self,user_id):
        # 資料庫取得 使用者觀看紀錄 轉Datafram
        return set(self.df[self.df['userId']==user_id]['movieId'])
