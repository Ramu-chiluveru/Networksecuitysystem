import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import pickle


def read_yaml_file(file_path):
  try:
    with open(file_path,"rb") as yaml_file:
      return yaml.safe_load(yaml_file)
  except Exception as e:
    raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path,content,replace):
  try:
    if replace:
      if os.path.exists(file_path):
        os.remove(file_path)
      os.makedirs(os.path.dirname(file_path),exist_ok=True)

      with open(file_path,"w") as file:
        yaml.dump(content,file)
  except Exception as e:
    raise NetworkSecurityException(e,sys)
  

def save_numpy_array_data(file_path,array):
  """
    save numpy array data to file
    file_path:  str location of file to save
    array : np.array data to save
  """

  try:
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path,exist_ok=True)

    with open(file_path,"wb") as file_obj:
      np.save(file_obj,array)
  
  except Exception as e:
    raise NetworkSecurityException(e,sys)
  

def save_object(file_path,obj):
  try:
    logging.info("Entered the save object method of mainutils class")
    os.makedirs(os.path.dirname(file_path),exist_ok=True)

    with open(file_path,"wb") as file_obj:
      pickle.dump(obj,file_obj)
    
    logging.info("Exited the save_object method of the mainutils class")
  except Exception as e:
    raise NetworkSecurityException(e,sys)