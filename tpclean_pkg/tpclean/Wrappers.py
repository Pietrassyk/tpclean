import pandas as pd

class Listener(pd.DataFrame):
    actions = []
    def __init__(self,df):
        self.actions = []

    def __setattr__(self, name, value):
        print(f"Access: {name}")
        self.actions.append({name:value}) # assigning to the dict of names in the class

    def __getattr__(self,name):
        print("Nothing here")