# In-Store-Tracker

**Covered Under BSD-3 Clause Open Source License**

## Dependencies:
- Python 3.12
- Pip
- Flask
- SQLite
- Pickle
- Pandas
- Numpy
- Seaborn
- Matplotlib
- OpenCV

## Set Up Instructions:
1. Verify an up-to-date installation of Python and pip.
2. Pull the entire repository to the local machine.
3. Navigate to the repository directory on the local machine.
4. Verify or download the list of dependencies above (running ${pip install -r requirements.txt} should download all needed dependencies).
5. Run `App.py`. (can be located from root as ./LiveTracking/dashboard/app.py)
6. A webpage should open for use.

## Termination Instructions:
1. Verify the current location is the project directory.
   - If using an IDE, interact with the Stop Process button.
   - If using the terminal directly, kill the running process using `CTRL+C`.

## Use Instructions:

1. **Starting and stopping camera recording:**
   - Upon reaching the webpage, interact with the start button to begin the video.
   - A separate window showing the camera view will appear.
   - Video recording is ongoing.
   - Interact with the stop button to end video recording.

2. **Querying database for heatmap:**
   - Input a valid date into the textBox.
   - Interact with the Generate Heatmap button.
   - A separate window will appear displaying heatmap data for the specified day.
   - Close the window.
   - Repeat from step A to view different Date's Heatmap data.

3. **HeatMap Metric for the most Recent Heatmap:**
   - Navigate to the Heatmap page using the Navigation bar at the top of the webpage.
   - The webpage will display the most recently queried heatmap page.
   - The webpage will display total customers for the given day.

## Notes:
- If an invalid format is entered into the heatmap query, the Generate Heatmap button will not be pressable. Verify heatmap date is in the correct mm/dd/yy format as requested.
- If an invalid date is entered into the heatmap query and the Generate Heatmap button is pressed, the user will be returned an error informing them that the requested date was not recorded.
