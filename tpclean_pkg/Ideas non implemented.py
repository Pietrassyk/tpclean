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

