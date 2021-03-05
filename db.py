import pymongo

def SaveDatainMongo(tableName,data):
    try:
        conectionString=f"mongodb+srv://vivek:vivek@cluster0.jaon8.mongodb.net/Reviews?retryWrites=true&w=majority"
        client = pymongo.MongoClient(conectionString)
        db = client["Reviews"]
        table=db[tableName]
        table.insert_many(data)
    except Exception as e:
        print(e)
    finally:
        client.close()

def getDataFromMongo(searchString):
    try:
        conectionString=f"mongodb+srv://vivek:vivek@cluster0.jaon8.mongodb.net/Reviews?retryWrites=true&w=majority"
        client = pymongo.MongoClient(conectionString)
        db = client["Reviews"]
        reviews= db[searchString].find({})
        return reviews
    except Exception as e:
        print(e)
    finally:
        client.close()