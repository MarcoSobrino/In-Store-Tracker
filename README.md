# In-Store-Tracker

**Covered Under BSD-3 Clause Open Source License**

## Dependencies:

- Python 3.12
- pip
- Flask
- SQLite
- Pickle
- Pandas
- Numpy
- Seaborn
- matplotlib
- OpenCV

## Set Up Instructions:

1. Verify an up-to-date installation of Python and pip.
2. Pull the entire repository to the local machine.
3. Navigate to the repository directory on the local machine.
4. Verify or download the list of dependencies above (`pip install` can be used in the project directory).
5. Run `App.py`.
6. Follow the link returned by the terminal to the Local Host webpage.

## Termination Instructions:

1. Verify the current location is the project directory.
2a. If using an IDE, interact with the Stop Process button.
2b. If using the terminal directly, kill the running process using `CTRL+C`.

## Use Instructions:

1. **Starting and stopping camera recording:**
    A. Upon reaching the webpage, interact with the start button to begin the video.
    B. A separate window showing the camera view will appear.
    C. Video recording is ongoing.
    D. Interact with the stop button to end video recording.

2. **Querying database for heatmap:**
    A. Input a valid date into the textBox.
    B. Interact with the Generate Heatmap button.
    C. A separate window will appear displaying heatmap data for the specified day.
    D. Close the window.
    E. Repeat from step A to view different Date's Heatmap data.

3. **HeatMap Metric for the most Recent Heatmap:**
    A. Navigate to the Heatmap page using the Navigation bar at the top of the webpage.
    B. The webpage will display the most recently queried heatmap page.
    C. The webpage will display total customers for the given day.

## Notes:

- If an invalid format is entered into the heatmap query, the Generate Heatmap button will not be pressable. Verify heatmap date is in the correct mm/dd/yy format as requested.
- If an invalid date is entered into the heatmap query and the Generate Heatmap button is pressed, the user will be returned an error informing them that the requested date was not recorded.
