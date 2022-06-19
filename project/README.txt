--------------------------------------------------------------------------------------
FOLDERS										-
--------------------------------------------------------------------------------------
- The main folder contains 5 python scripts, 2 folders, and 1 readme file
- "data" folder contains the original CSV file and is the suggested folder for output
- "test_data" contains data needed to run tests
--------------------------------------------------------------------------------------
TO DO											-
--------------------------------------------------------------------------------------
- Decompress this archive in a new folder
- Import the libraires listed below in a new virtual python environment
- Open a new terminal window in the main folder (as described above)
  OR
  Navigate to and open the main folder (as described above) in the terminal
- Run the suggested commands listed below
--------------------------------------------------------------------------------------
LIBRAIRIES USED									-
--------------------------------------------------------------------------------------
- re
- math
- argparse
- unittest
- pandas
- numpy
- operator
- matplotlib.pyplot
--------------------------------------------------------------------------------------
SUGGESTED COMMANDS									-
--------------------------------------------------------------------------------------
- python3 monkey_classif.py knn data/monkeys.csv data/results.csv
  AND
- python3 monkey_classif.py visualize data/results.csv size weight
  OR
- python3 monkey_classif.py visualize data/results.csv weight size
--------------------------------------------------------------------------------------
GOOD TO KNOW										-
--------------------------------------------------------------------------------------
- If the visualization plot isn't displayed:
  - comment plt.show() at line 20 of monkey_visualize.py
  - uncomment plt.savefig("data/scatter_plot.jpg") at line 18 of monkey_visualize.py 
--------------------------------------------------------------------------------------
WORK DONE										-
--------------------------------------------------------------------------------------
- Exercise 1		YES
- Exercise 2		YES
- Exercise 3		YES
- Exercise 4		YES
- Exercise 5		YES
- Bonus exercices	NO
- Exercise 1 tests	YES
- Exercise 2 tests	YES
- Exercise 3 tests	YES
- Exercise 4 tests	NO
- Exercise 5 tests	NO
--------------------------------------------------------------------------------------
IF I HAD MORE TIME									-
--------------------------------------------------------------------------------------
- Implement tests for exercices 4 and 5
- Raise errors to make CLI inputs idiot-proof
- Optimize the knn algorithm by not iterating over a pandas dataframe with for loops
