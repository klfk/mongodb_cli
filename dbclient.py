import pymongo as pm

class DBClient:
   
    def search(self, criteria):
        result = self.col.find(criteria)
        return result

    def update_one(self, filter_dict, update_dict):
        result = self.col.update_one(filter_dict, update_dict)
        return result
    
    def delete_one(self, filter_dict):
        result = self.col.delete_one(filter_dict)
        return result
    
    def create(self, data): #data = {field: value}
        result = self.col.insert_one(data)
        return result

    def __init__(self):
        self.myclient = pm.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["kinofilme"]
        self.col = self.mydb["dvd_sammlung"]
