from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""
    
    def __init__(self, USER='', PASS='', HOST='localhost', PORT=27017, DB='AAC', COL='animals'):
        """
        Initialize MongoDB connection
        
        Args:
            USER: MongoDB username (empty string for local MongoDB)
            PASS: MongoDB password (empty string for local MongoDB)
            HOST: MongoDB host (default: localhost)
            PORT: MongoDB port (default: 27017)
            DB: Database name (default: AAC)
            COL: Collection name (default: animals)
        """
        try:
            # Connection string for local MongoDB no authentication 
            if USER and PASS:
                self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
            else:
                self.client = MongoClient(f'mongodb://{HOST}:{PORT}')
            
            self.database = self.client[DB]
            self.collection = self.database[COL]
            
            # Test connection
            self.client.server_info()
            print(f"Successfully connected to MongoDB database: {DB}")
            
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    def create(self, data):
        """
        Create/Insert a document into the collection (C)
        
        Args:
            data: Dictionary containing animal data
            
        Returns:
            True if successful, False otherwise
        """
        if data is not None:
            try:
                self.collection.insert_one(data)
                return True
            except Exception as e:
                print(f"An error occurred during insertion: {e}")
                return False
        else:
            raise Exception("Nothing to save, because the data parameter is empty")
    
    def read(self, query):
        """
        Read/Query documents from the collection (R)
        
        Args:
            query: Dictionary containing search criteria
            
        Returns:
            List of matching documents
        """
        if query is not None:
            try:
                results = self.collection.find(query)
                return list(results)
            except Exception as e:
                print(f"An error occurred during query: {e}")
                return []
        else:
            raise Exception("Query parameter is empty or invalid")
    
    def update(self, query, update_data):
        """
        Update a document in the collection (U)
        
        Args:
            query: Dictionary containing search criteria
            update_data: Dictionary containing fields to update
            
        Returns:
            Number of documents modified
        """
        if query is not None and update_data is not None:
            try:
                result = self.collection.update_one(query, {'$set': update_data})
                return result.modified_count
            except Exception as e:
                print(f"An error occurred while updating: {e}")
                return 0
        else:
            raise Exception("Nothing to update, because query parameter is empty or invalid")
    
    def delete(self, query):
        """
        Delete a document from the collection (D)
        
        Args:
            query: Dictionary containing search criteria
            
        Returns:
            Number of documents deleted
        """
        if query is not None:
            try:
                result = self.collection.delete_one(query)
                return result.deleted_count
            except Exception as e:
                print(f"An error occurred while deleting: {e}")
                return 0
        else:
            raise Exception("Nothing to delete, because query parameter is empty or invalid")