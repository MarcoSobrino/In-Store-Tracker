# library
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

excel_file = "C:\\Users\\asus\\Desktop\\SENIOR PROJECT\\Repository\\In-Store-Tracker\\LiveTracking\\HeatMap\\testData.xlsx"
xldata = pd.read_excel(excel_file, sheet_name="test", index_col=0)
xl_clean = xldata.replace(np.NaN, 0)

# print(xl_clean)

heatmap_data = xl_clean

sns.heatmap(heatmap_data, annot=True)
plt.tight_layout()
plt.show()

