

# Function to clean data based on tree or planting site

def tree_clean(exist,data):
    df = data.loc[data['present']==exist,["X","Y","genus", "species", "commonname", "coremoved_ozperyr", "carbonstorage_lb", 'diameterin','plantingdate']].fillna("not available")
    return df