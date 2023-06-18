
'''from application.extensions import mongo


class MongoHandler(mongo):

    def __init__ (self):
        super()


if __name__ == "__main__":
    host = 'mongodb+srv://kenan:Yyecgaa123123@cluster0.s0aykgz.mongodb.net/?retryWrites=true&w=majority'
    db = MongoHandler(host)

    database = db.get_database()
    coll = database.get_collection("test")
    print(coll.count_documents({}))

    docs = coll.find()
    for item in docs:
        print(item)'''