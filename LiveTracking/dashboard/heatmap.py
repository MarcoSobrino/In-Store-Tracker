# library
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import os
import sqlite3


def generateHeatmap(dateParameter):
    #set var csv_file to the file test.csv in the same directory as this file
    csv_file = os.path.join(os.path.dirname(__file__), 'test.csv')

    xldata = pd.read_csv(csv_file, index_col=0)
    xl_clean = xldata.fillna(0) 

    heatmap_data = xl_clean

    sns.heatmap(heatmap_data, annot=True)
    plt.tight_layout()


    #entriesVsPresses = registerData(dateParameter)

    totalEntries = total(dateParameter)

    entriesVsPresses = 5

    date = dateParameter

    #save to the static directory of the dashboard directory
    #set var savePath to directory up one directory then down 2 directories using os
    savePath = os.path.join(os.path.dirname(__file__), '..\dashboard\static\heatmap.png')


    plt.savefig(savePath)

    plt.show()

    #print("Largest Value: ", largest_value)
    #print("Section with the Largest Value (1-based index): Row", largest_value_row, "Column", largest_value_col)

    with open("heatmap_data.pkl", "wb") as f:
        pickle.dump((totalEntries, entriesVsPresses, date), f)

#generateHeatmap()

#def registerData(date)
    #get value of total - button press from data base
    #return that value

def total(date):
    # Connect to the local SQLite database
    conn = sqlite3.connect('LiveTracking.db')

    if not conn:
        print("Error connecting to the database.")
        return

    # Query the database to retrieve the data for the specified date
    query = f"SELECT Total FROM RegisterData WHERE Date = '{date}'"
    
    return query