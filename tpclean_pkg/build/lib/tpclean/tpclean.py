"""tpclean Library by Tino Pietrassyk Version 0.6"""

#Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Plotting

def plot_hists(df,nrows=1,ncols=1, figsize=(4,4), columns = None):
    """Plots histograms given a Dataframe, Num Rows, Num Cols and a Size opt. for each subplot. You can pass a List of Column postions or names to slice the Dataframe"""
    df = df.copy()
    fig , axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figsize[1]*nrows,figsize[0]*ncols))
    for n,c in enumerate(df[[df.columns[x] if type(x)==int else x for x in columns]] if columns else df):
        row = n//ncols
        col = n%ncols
        if nrows <1 and ncol<1:
            ax = axes[row][col]
        elif nrows>1:
            ax = axes[row]
        elif ncols>1:
            ax = axes[col]
        else:
            ax = axes
        sns.distplot(df[c],ax=ax).set(title = c);


# Transformations

def log_transform(df,columns):
    """Takes in DataFrame and a List of column names, will return Dataframe with
    log transformation applied to selected columns"""
    df=df.copy()
    for col in columns:
        df[col]=df[col].apply(lambda x: np.log(x))
    return df

def dummy_transformation(df,col_kwargs,one_hot = True):
    """Run one_hot transformation on target column(s). Columns must be passed as a list of dicts
    providing the following parameters: name(str), bins(list), labels(list), abr(str).
    one_hot: if False columns are just binned not transformed into columns representing each bin as a 1 or 0

     Example for col_kwargs:
     col_dict=[{"name":"col1","bins":[0,1,2,3,99],"labels":[0,1,2,"3+"],"abr":"c_"}]
     """
    df=df.copy()
    for col in col_kwargs:
        df[col["name"]]=pd.cut(df[col["name"]],bins=col["bins"],labels=col["labels"])
        if one_hot:
            dummy = pd.get_dummies(data=df[col["name"]],prefix=col["abr"],drop_first=True)
            df = pd.concat([df,dummy], axis=1)
            df = df.drop(col["name"], axis=1)
    return df