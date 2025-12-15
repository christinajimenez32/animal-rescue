#Shelter
from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        USER = 'aacuser'
        PASS = 'SNHU1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 32907
        DB = 'AAC'
        COL = 'animals'

    def __init__(self, USER, PASS, HOST, PORT, DB, COL):
        # Initialize Connection
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
        self.database = self.client[DB]
        self.collection = self.database[COL]

    def create(self, data):
        if data is not None :
            try:
                self.database.animals.insert_one(data)  # data should be a dictionary
                return True
            except Exception as e:
                print(f"An error occurred during insertion: {e}")
                return False
        else:
            raise Exception("Nothing to save, because the data parameter is empty")

    # Create method to implement the R in CRUD.
    def read(self, query):
        if query is not None:
            try:
                results = self.database.animals.find(query)  # query should be a dictionary
                return list(results)  # Convert the cursor to a list
            except Exception as e:
                print(f"An error occurred during query: {e}")
                return []
        else:
            raise Exception("Query parameter is empty or invalid")
        
    # Create method to implement the U in CRUD.
        def updateOne(self, query, update_data):
            if query is not None and update_data is not None:
                try:
                    results = self.database.animals.update_one(query,{'$set': update_data}) # 
                    return result.modified_count
                except Exception as e:
                    print(f"An error occured while updating: {e} ")
                    return 0
                else:
                    raise Exception("Nothing to update, because query parameter is empty or invalid")
    # Create method to implemeny the D in CRUD
        def delete(self, query):
            if query is not None:
                try:
                    result = self.database.animals.delete_one(query)  #deletes 
                    return result.deleted_count
                except Exception as e:
                    print(f"An error occured while deletion: {e} ")
                    return 0
                else:
                    raise Exception("Nothing to delete, because query parameter is empty or invalid")
                    