
class Task:
    def __init__(self, data) -> None:
        
        self.id = data['_id']
        self.description = data['description']
        self.status = data['status']
       

    def to_mongo(self):
        return {
            "_id": self.id,
            "description": self.description,
            "status": self.status
        }