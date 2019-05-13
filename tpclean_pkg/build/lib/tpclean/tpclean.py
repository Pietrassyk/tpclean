"""tpclean Library by Tino Pietrassyk Version 0.6"""

# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Plotting

def plot_hists(df, nrows=1, ncols=1, figsize=(4, 4), columns=None):
    """Plots histograms given a Dataframe, Num Rows, Num Cols and a Size opt. for each subplot. You can pass a List of Column postions or names to slice the Dataframe"""
    df = df.copy()
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(figsize[1] * nrows, figsize[0] * ncols))
    for n, c in enumerate(df[[(df.columns[x] if type(x) == int else str(x)) for x in columns]] if columns else df):
        row = n // ncols
        col = n % ncols
        if nrows > 1 and ncols > 1:
            ax = axes[row][col]
        elif nrows > 1:
            ax = axes[row]
        elif ncols > 1:
            ax = axes[col]
        else:
            ax = axes
        if n > ncols * nrows:
            break
        sns.distplot(df[c], ax=ax).set(title=c);


# SQL Connectivity

def sql_connect(database):
    global c
    import sqlite3
    conn = sqlite3.connect(database)
    c = conn.cursor()
    print(f"Connection to {database} successfull. with curser {c}")


def sql(querry, cursor=None , df_return = True, verbose = False):
    """Runs a SQL querry and returns results as a Dataframe. cursor Variable is set to 'c' by default. Make sure your run sql_connect before using or set cursor manually
        df_return: (Bool) returns Pandas Dataframe of the Querry. If false just execute Querry
        verbose : (Bool) Prints Querry Statement"""
    if cursor:
        d = cursor
    try:
        global c
        d = c
    except UnboundLocalError:
        print(
            "Provide cursor variable or Run tp.sql_conncet('database') to define cursor and make sure you dont have a Variable called <c>")
        return
    d.execute(querry)
    df = pd.DataFrame(d.fetchall())
    if df_return and len(df):
        df.columns = [x[0] for x in d.description]
        return df
    if verbose:
        print(querry)
    print("Executed Querry")
    return d.fetchall()

def sql_make_table(tablename, columns=[], datatypes=[], primary_key=None):
    """Runs Querry for Creating a new table:
    columns: (List) Name of the Columns for the table
    datatypes: (List) can be df.dtype or samplevalues in the desired datatype  (currently supportet : int, float, string)
    primary_key: columns name that is set to be the primary key. if empty, a column ID will be created"""
    # convert python datatypes into sql datatypes

    ###the list of datatypes should be extended
    table_datatypes = ["NUMBER" if isinstance(x, int) or x == "int64" or x == "int32" else "REAL" if isinstance(x,
                                                                                                                float) or x == "float" else "TEXT"
                       for x in datatypes]
    columns = list(columns)

    # check whether we need a new primary key (ID)
    if not primary_key:
        # create new column ID and set it as Primary Key
        columns.append("id")
        table_datatypes.append("INTEGER PRIMARY KEY AUTOINCREMENT")
    else:
        # set called column as primary key
        table_datatypes[columns.index(primary_key)] += " PRIMARY KEY"

    # build sql statement
    ## connect names and datatypes
    cols_with_dtypes = []
    for n, col in enumerate(columns):
        cols_with_dtypes.append(col + " " + table_datatypes[n])
    ## concatenate
    querry = "CREATE TABLE " + tablename + "( " + ", ".join(cols_with_dtypes) + " )"
    sql(querry)

def table_from_df(df, tablename, primary_key=None):
    """Takes a Dataframe and writes it as a table into a SQL Database"""
    global c
    # get existing tablenames from database
    db_tablenames = list(sql("""select * from sqlite_master""").tbl_name.values)
    # define

    table_columns = "(" + (", ".join(df.columns)) + " )"

    # check whether table already exists
    if not tablename in db_tablenames:
        # create new table
        print("Creating a new Table")
        sql_make_table(tablename, df.columns, df.dtypes, primary_key)

    for i in range(len(df)):
        insert = "INSERT INTO " + tablename + "(" + (", ".join(df.columns)) + " )"
        insert += " VALUES " + str(tuple(df.iloc[i].values)) + ";"
        c.execute(insert)
    c.fetchall()
    return sql(f"select * from {tablename}")

# Transformations

def log_transform(df, columns):
    """Takes in DataFrame and a List of column names, will return Dataframe with
    log transformation applied to selected columns"""
    df = df.copy()
    for col in columns:
        df[col] = df[col].apply(lambda x: np.log(x))
    return df


def log(df, columns):
    """ Takes in a Dataframe and a List of column names and runs log_transform. See help(tp.log_transform) for
    further information"""
    return log_transform(df, columns)


def dummy_transformation(df, col_kwargs, one_hot=True):
    """Run one_hot transformation on target column(s). Columns must be passed as a list of dicts
    providing the following parameters: name(str), bins(list), labels(list), abr(str).
    one_hot: if False columns are just binned not transformed into columns representing each bin as a 1 or 0

     Example for col_kwargs:
     col_dict=[{"name":"col1","bins":[0,1,2,3,99],"labels":[0,1,2,"3+"],"abr":"c_"}]
     """
    df = df.copy()
    for col in col_kwargs:
        df[col["name"]] = pd.cut(df[col["name"]], bins=col["bins"], labels=col["labels"])
        if one_hot:
            dummy = pd.get_dummies(data=df[col["name"]], prefix=col["abr"], drop_first=True)
            df = pd.concat([df, dummy], axis=1)
            df = df.drop(col["name"], axis=1)
    return df
