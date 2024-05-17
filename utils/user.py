import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from pymongo import MongoClient
import re

load_dotenv(".env")

class User(object):
    def __init__(self, app) -> None:
        self._bycrypt=Bcrypt(app=app)
        
        
    @classmethod
    def connectDB(cls, databaseName = 'Travelo', collectionName='Users'):
        try:
            client=MongoClient(os.getenv('MONGO_CLIENT'))
            db=client[databaseName]
            collection=db[collectionName]
            connectionStatus=True
        except:
            print("Database connection failed!")
            connectionStatus=False

        return client, collection, connectionStatus
    
    
    
        
    def addUser(self, username:str, emailAddress:str, phoneNumber:str, password:str):
        try:
            client, collection, connectionStatus=User.connectDB()
            
            if connectionStatus is True:
                _, user=self.getUserByEmail(emailAddress)
        
                
                if user is None:
                    password=self._bycrypt.generate_password_hash(password).decode('utf-8')
                    
                    collection.insert_one({"username" : username, "emailAddress" : emailAddress, "phoneNumber" : phoneNumber, "password" : password})
                    print("User successfully added")
                    status=True
                else:
                    print("Failed adding user.")
                    status=False
        finally:
            client.close()
        
        return status
    
          
    def getUserByEmail(self, emailAddress : str):
        try:
            client, collection, connectionStatus=User.connectDB()
            if connectionStatus is True:
                user=collection.find_one({"emailAddress" : emailAddress})
                if user is None:
                    status='User not found'
                else:
                    status='User was found'
                
        finally:
            client.close()
            
        return status, user
    
    
    def logInUser(self, emailAddress:str, password:str):
        try:
            client, collection, connectionStatus=User.connectDB()
        
            if connectionStatus is True:
                _, user=self.getUserByEmail(emailAddress)
            
                if user is None:
                    status="User not found"
                    print("User not found")
                else:
                    isValid =self._bycrypt.check_password_hash(user['password'], password)
                    
                    if isValid:
                        print("Login successful")
                        status="Login successful"
                    else:
                        print("Incorrect password")
                        status="Incorrect password"
        finally:
            client.close()
            
        return status, user
    
    def updateUser(self, emailAddress, username=None, emailAddressEdited=None, phoneNumber=None, gender=None, address=None, password=None):
        try:
            client, collection, connectionStatus=User.connectDB()
            
            if connectionStatus is True:
                if not username is None:
                    collection.update_one({'emailAddress' : emailAddress}, {'$set' : {'username' : username}})
                    status=True
                    
                if not emailAddressEdited is None:
                    collection.update_one({'emailAddress' : emailAddress}, {'$set' : {'emailAddress' : emailAddressEdited}})
                    status=True
            
                if not phoneNumber is None:
                    collection.update_one({'emailAddress' : emailAddress}, {'$set' : {'phoneNumber' : phoneNumber}})
                    status=True
            
                if not gender is None:
                    collection.update_one({'emailAddress' : emailAddress}, {'$set' : {'gender' : gender}})
                    status=True
        
                if not address is None:
                    collection.update_one({'emailAddress' : emailAddress}, {'$set' : {'address' : address}})   
                    status=True
                    
                if not password is None:
                    password=password=self._bycrypt.generate_password_hash(password).decode('utf-8')
                    collection.update_one({'emailAddress' : emailAddress}, {'$set' : {'password' : password}})
                    status=True
                             
            else:
                status=False
               
        finally:
            client.close()
            
        return status
            
    

    def deleteUser(self, emailAddress):
        try:
            client, collection, connectionStatus=User.connectDB()
            
            if connectionStatus is True:
                collection.delete_one({"emailAddress" : emailAddress})
                status=True
            else:
                status=False
        finally:
            client.close()
        
        return status
    
    def makeReservation(self):
        pass    
        


        


    
        