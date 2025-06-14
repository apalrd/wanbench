#!/usr/bin/python3
#Simulation for DS-Lite
from utils import wan_type, route, ipr

class dslite(wan_type):
    # Validate arguments
    def __new__(cls, args):
        print("New DS-Lite, args are",args)
        #Validate arguments, return None on error
        #Validation successful
        return super().__new__(cls)

    # Init DS-Lite object from args
    def __init__(self,args):
        print("In DS-Lite, args are",args)

    def setup(self):
        # Set link IP on wan if
        print("In DS-Lite setup")

    # Teardown DS-Lite tunnel
    def __del__(self):
        print("Del DS-Lite")