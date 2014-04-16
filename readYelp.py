####################################
# This file provides a function to read the any Yelp file
####################################
import json
from pprint import pprint

""" Read function:
-linesNumb determines how many lines to read (0 = all).
returns the numbers of lines and the data in an array.
"""
def readY(name,linesNumb = 0):
    json_data=open(name)
    lines0 = json_data.readlines()
    #Only read the first linesNumb entries of the data
    if linesNumb==0:
        lines = lines0
    else:
        lines = lines0[:linesNumb]

    #Pass them to a list
    smart_lines = [json.loads(line) for line in lines]

    #Get the length
    length = len(lines)

    return (length, smart_lines)
