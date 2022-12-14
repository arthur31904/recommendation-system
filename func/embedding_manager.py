import pandas as pd
import json
import numpy as np
import faiss

class EmbeddingManager(object):
    def __init__(self, fpath, key_name, value_name):
        self.df = pd.read_csv(fpath)

        self.dict_embedding = self.load_embedding_to_dict(key_name, value_name)

        self.faiss_index = self.load_embedding_to_faiss(key_name, value_name)

    def get_embedding(self, key):

        return self.dict_embedding[str(key)]

    def load_embedding_to_dict(self , key_name, value_name):


        return {
            str(row[key_name]):row[value_name] for index,row in self.df.iterrows()
        }

    def load_embedding_to_faiss(self , key_name, value_name):
        ids = self.df[key_name].values.astype(np.int64)

        datas = [json.loads(x) for x in self.df[value_name]]

        datas = np.array(datas).astype(np.float32)

        dimention = datas.shape[1]

        index = faiss.IndexFlatL2(dimention)
        index2 = faiss.IndexIDMap(index)
        index2.add_with_ids(datas,ids)

        return index2

    def search_ids_by_embedding(self, embedding_str, topk):
        input = np.array(json.loads(embedding_str))

        input = np.expand_dims(input,axis=0).astype(np.float32)

        D,I = self.faiss_index.search(input,topk)

        return list(I[0])

