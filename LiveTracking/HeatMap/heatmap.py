# library
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

csv_file = (r".\LiveTracking\HeatMap\test.csv")
xldata = pd.read_csv(csv_file, index_col=0)
xl_clean = xldata.fillna(0) 


#excel_file = (r".\LiveTracking\HeatMap\testData.xlsx")
#xldata = pd.read_excel(excel_file, sheet_name="test", index_col=0)
#xl_clean = xldata.replace(np.NaN, 0)

# print(xl_clean)

heatmap_data = xl_clean

sns.heatmap(heatmap_data, annot=True)
#sns.heatmap(xldata, annot=True, cmap='coolwarm', fmt='d', cbar=False, square=True)
plt.tight_layout()

largest_value = heatmap_data.values.max()
#largest_value_position = np.unravel_index(heatmap_data.values.argmax(), heatmap_data.shape)
largest_value_position = np.unravel_index(xldata.values.argmax(), xldata.shape)

largest_value_row = largest_value_position[0] + 1
largest_value_col = largest_value_position[1] + 1

#save to the static directory of the dashboard directory
savePath = (r"C:\Users\senti\Desktop\Senior Project\Repo\In-Store-Tracker\LiveTracking\dashboard\static\heatmap.png")

plt.savefig(savePath)

plt.show()

print("Largest Value: ", largest_value)
print("Section with the Largest Value (1-based index): Row", largest_value_row, "Column", largest_value_col)

with open("heatmap_data.pkl", "wb") as f:
    pickle.dump((largest_value, largest_value_row, largest_value_col), f)
