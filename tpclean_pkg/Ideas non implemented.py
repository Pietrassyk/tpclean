def ols_select_features (model,alpha = 0.05, get_df = False, verbose = True):
    """Get Features of a Statsmodels linear Model, that do not yield significant p values
    ------------
    Inputs
    model: sm.OLS Object
    alpha: [float] alpha threshold for p value comparison
    get_df : [bool] if True results table will be outputed as pandas Dataframe
    verbose: [bool] whether or not to print unsignificant features while running
    ------------
    Outputs:
    [list] of unsignificant Features"""
    value_table = pd.DataFrame(model.summary().tables[1])
    value_table = value_table.applymap(lambda x: x.data)
    value_table.columns=value_table.iloc[0]
    value_table = value_table.drop(0,axis = "index")
    value_table = value_table.set_index("")
    value_table = value_table.applymap(lambda x: float(x))
    if get_df:
        return value_table
    else:
        out = list(value_table.loc[value_table[value_table.columns[3]] > alpha].index)
        if verbose:
            print(f"The following Features have p_values higher then aplha: {alpha}")
            for item in out:
                print(item)
        return out

def heatmap_corr(dataframe):
    """ Plots a heatmap of correlation between features with masking.
    ------------
    Inputs
    dataframe: Pandas DataFrame Object
    ------------
    Outputs:
    None"""
    #Thanks to Jon Keller for contributing
    fig, ax = plt.subplots(figsize=(20,20))
    mask=np.zeros_like(dataframe.corr(), dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    color_map = sns.color_palette("hot_r")
    ax = sns.heatmap(dataframe.corr(), cmap = color_map, mask=mask, square=True, annot=True)

#TODO Put in Confusion Matrix PLot from Sklearn