"""
  The setup.py file is an essential part of packaging and distributing python projects. It is used by setup tools to define the configuration of the project such as metadata , dependencies and more
"""

from setuptools import find_packages,setup
from typing import List


def get_requirements() -> List[str]:
  """
    This function will return list of requirements
  """

  requirement_list:List[str] = []
  try:
    with open("./requirements.txt","r") as file:
      # read lines from the file
      lines = file.readlines()

      # process each line
      for line in lines:
    
        #remove spaces
        requirement = line.strip()

        ## ignore empty lines and -e .
        if(requirement and requirement != '-e .'):
          requirement_list.append(requirement)
      return requirement_list
  except FileNotFoundError:
    print("Requirements.txt file is not found")

setup(
  name="Networksecurity",
  version="0.0.1",
  author="Ramu chiluveru",
  author_email="ramuchiluveru.cr@gmail.com",
  packages=find_packages(),
  install_requires = get_requirements()
)