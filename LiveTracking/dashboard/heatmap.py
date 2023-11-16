# library
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import os


def generateHeatmap():
    #set var csv_file to the file test.csv in the same directory as this file
    csv_file = os.path.join(os.path.dirname(__file__), 'test.csv')

    xldata = pd.read_csv(csv_file, index_col=0)
    xl_clean = xldata.fillna(0) 


    #excel_file = (r".\LiveTracking\HeatMap\testData.xlsx")

    #excel_file = os.path.join(os.path.dirname(__file__), 'testData.xlsx')
    #xldata = pd.read_excel(excel_file, sheet_name="test", index_col=0)
    #xl_clean = xldata.replace(np.NaN, 0)

    # print(xl_clean)

    heatmap_data = xl_clean

    sns.heatmap(heatmap_data, annot=True)
    #sns.heatmap(xldata, annot=True, cmap='coolwarm', fmt='d', cbar=False, square=True)
    plt.tight_layout()


    #toBeDisplayed = registerData(dateParameter)



    largest_value = heatmap_data.values.max()
    #largest_value_position = np.unravel_index(heatmap_data.values.argmax(), heatmap_data.shape)
    largest_value_position = np.unravel_index(xldata.values.argmax(), xldata.shape)

    largest_value_row = largest_value_position[0] + 1
    largest_value_col = largest_value_position[1] + 1

    #save to the static directory of the dashboard directory
    #set var savePath to directory up one directory then down 2 directories using os
    savePath = os.path.join(os.path.dirname(__file__), '..\dashboard\static\heatmap.png')


    plt.savefig(savePath)

    plt.show()

    print("Largest Value: ", largest_value)
    print("Section with the Largest Value (1-based index): Row", largest_value_row, "Column", largest_value_col)

    with open("heatmap_data.pkl", "wb") as f:
        pickle.dump((largest_value, largest_value_row, largest_value_col), f)

#generateHeatmap()

#def registerData(date)
    #get value of total - button press from data base
    #return that value