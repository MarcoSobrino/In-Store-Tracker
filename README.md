# In-Store-Tracker
Covered Under BSD-3 Clause Open Source License

Dependencies:
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

Set Up Instructions:

1) Verify Up-To-Date installation of python and pip.
2) Pull entire repository to local machine.
3) Navigate to repo directory on local machine.
4) Verify or download list of dependencies above (pip install can be used in project directory).
5) Run App.py
6) Follow Link returned by terminal to Local Host webpage.


Termination Instructions:
1) Verify current location is project directory
2a) If using an IDE, interact with Stop Process button
2b) If using terminal directly, kill running process using CTRL+C




Use Instructions:

1) Starting and stopping camera recording.
    A) Upon reaching the webpage, interact with start button to begin video.
    B) A seperate window showing camera view will appear.
    C) Video recording is ongoing.
    D) Interact with stop button to end video recording.

2) Querying database for heatmap.
    A) Input Valid date into textBox.
    B) Interact with Generate Heatmap button.
    C) A seperate window will appear displaying heatmap data for specified day.
    D) Close Window.
    E) Repeat from step A to view different Date's Heatmap data.

3) HeatMap Metric for most Recent Heatmap.
    A) Navigate to Heatmap page using Navigation bar at the top of the webpage.
    B) The webpage will display most recently queried heatmap page.
    C) The webpage will display total customers for given day.



Notes:
- If invalid format is entered into heatmap query, generate heatmap button will not be pressable.
Verify heatmap date is in correct mm/dd/yy format as requested
- If invalid date is entered into heatmap query and generate heatmap button is pressed, user will
be returned an error informing them that the requested date was not recorded.

