#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of objects in storage. If cls is not None,
        returns only objects of the specified class.
        """
        if cls:
            class_name = cls.__name__
            return {k: v for k, v in FileStorage.__objects.items()
                    if class_name in k}
        else:
            return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = obj.__class__.__name__ + '.' + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in FileStorage.__objects.items()}, f)

    def delete(self, obj=None):
        """Deletes an object from storage if it exists"""
        if obj is None:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]

    def reload(self):
        """Loads storage dictionary from file"""
        classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
                   'State': State, 'City': City, 'Amenity': Amenity,
                   'Review': Review}
        try:
            with open(FileStorage.__file_path, 'r') as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    obj = classes[class_name](**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        """
        method for deserializing the JSON file to objects
        """
        self.reload()

