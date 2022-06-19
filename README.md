# Labs 9 & 10: The wider python ecosystem

## Overview

Last time, we've had a deep look at Python's OOP paradigm. With that, we have covered most of the basics: the toolbox at your disposal should be enough to tackle most issues you'll encounter.

On the other hand, basics are just that: basics. Learning more about the python ecosystem will help you be more efficient. Knowing what exists in third-party libraries will help you not reinvent the wheel for well-trodden problems. We'll be giving you pointers to existing libraries to get you started, as well as explore the functional programming style.

The second goal is to familiarize you with good practices when working with python scripts. We'll be covering TDD (test-driven development), as well as debugging using `pdb`, and python code modularity.

To meet these two goals, we'll focus on a **project**: implementing a small classification script to distinguish apes species based on features such as weight, height, fur color... To be precise, you will have to produce multiple python scripts:
1. `monkey_classif.py`, which will be responsible for running our classification algorithm
2. `monkey_visualize.py`, which will contain all the logic for producing visualizations
3. `monkey_model.py`, which will contain all the object-oriented logic for constructing our monkey representations
4. `utils.py`, which will contain all the utility functions and "glue code"
5. `tests.py`, which will correspond to tests

**Data**: the csv file that you will need is called `monkeys.csv`, which contains 3K lines of 3 types of monkeys. Roughly 25% of the datapoints are missing labels, and about 1% of the data per column is malformed, meaning missing value. You will need to download the file.

This jupyter notebook is mostly here as an instructions file, as well as a convenient place for us to put reviews and such. It's structured as follows:
1. Part #1 gives the precise instructions as to what you need to implement
2. Part #2 contains information about how to debug and write test cases. It also contains a bunch of bonus exercises to make sure you understand the concepts we're presenting here. This part teaches you the best practices to python project development.
3. Part #3 gives you pointers on functionnal programming.
4. Part #4 gives you pointers to the standard libraries you'll be using for this project.

**NB:** *Like the previous mini and mega-labs, this lab will be corrected by hand. It is crucial that you make sure everything runs smoothly and without error before submitting your work!*

For this lab, we'll expect a **different format of submission**: you'll have to submit all your source files in a ZIP archive file. We expect the submission to be named `tp9_fname_lname.zip`, with `fname` your first name and `lname` your last name. The archive must contain _everything needed to run your code_, and _only that_.

The main goal of this lab is to confront you to an actual python project. It might seem overwhelming at first! Break down the full process into little steps, and you'll see that it's actually not so big of a deal. Start by writing this instruction notebook in its entirety!

Part of what we'll evaluate in this lab is your ability to produce clean, coherent, consistent, commented code. If you have the time, try to make your code as efficient as possible. Feel free to add supplementary files, functions and functionalities. Organize your archive in an obvious manner. Don't hesitate to add a README file.

## Part #1: Instructions

### Exercise #1: Implement a `Monkey` class

1. In your file `monkey_model.py`, declare a class named `Monkey`. `Monkey` objects are to have four attributes: `species`, `fur_color`, `size`, `weight`. The `species` should default to an empty string, passing a value to the constructor for the three other attributes is mandatory. The `fur_color` will be represented as an hexadecimal color value string.
2. Add `__str__` and `__repr__` methods to make things more readable. Both methods should return `str` containing informations on all four attribtues of the `Monkey` object. 
3. In your file `utils.py`, write a function `check_hexacolor(color_str)` that verify whether a string is a valid hexadecimal color code. In short, a string representing a color starting with a hashtag `#`, followed by six hexadecimal integers. See [here](https://www.w3schools.com/html/html_colors_hex.asp) for details.
4. Import the function `check_hexacolor` in your file `monkey_model.py`. Modify your `Monkey` class constructor: raise a ValueError if the value provided for `fur_string` is not a hexadecimal color string.

Implement tests for this `Monkey` class. This instruction is intentionally left vague: the aim is to have you think as to what the tests should be! Make sure your code passes **all** your tests. **Read Part #2 carefully beforehand!**  All your tests should be in the file `tests.py`.

### Exercise #2: Produce a `dataframe` of monkeys

1. In your class `Monkey`, add a method `compute_bmi` that returns the body mass index of a monkey. As a reminder, the BMI is defined as: $$BMI = \frac{weight}{size^2}$$
3. In your file `monkey_classif.py`, add a function called `read_monkeys_from_csv(csv_path)` that loads the CSV file `monkeys.csv` using the pandas library. **Read Part #4 carefully beforehand!**.
  1. Make sure the header contains only the following keys: `fur_color`, `size`, `weight`, `species`, and raise a `ValueError` otherwise.
  1. Drop any row that contains invalid data: negative size and weights values, invalid hexadecimal color strings, rows with missing values...
  1. add a column `monkey` of `Monkey` objects for each valid row. Use the `dataframe.apply` with a `lambda` function **Read Part #3 carefully beforehand!**.
  1. add a column `fur_color_int`, where you convert hexadecimal color code strings into integers.
  1. add a column `bmi`, where you store body mass indices for all your data point.


Implement tests for these features. This instruction is intentionally left vague: the aim is to have you think as to what the tests should be! Make sure your code passes **all** your tests. **Read Part #2 carefully beforehand!**  All your tests should be in the file `tests.py`.

### Review #1.1: The KNN algorithm

KNN stands for `$k$ nearest neighbors`. It is a rather straightforward classification algorithm, where items are assigned labels based on the most common label of their $k$ nearest neighbors.

The KNN presupposes a distance function between all items (Monkeys, in our case). In practice, this means that we need to be able to convert any item into a point in an Euclidean space with $d$ dimensions. Once we have that, we can use the standard euclidean distance between two points to determine which already classified items are the nearest neighbors of the current item to classify.

The pseudocode for a simple KNN classification is as follows:
```
for each unlabelled item I; do
    for each labelled item J; do 
        compute the distance between I and J
    neighbors <- select the k items J with minimal distance to I
    label for I <- select the most common label for the neighbors
```

Variants of the algorithm may or may not append the classified item `I` to the set of labelled items. Doing so may have consequences in terms of stability, depending on the distribution of the data and the labels.

Another point where the algorithm may vary consists in how to select the label once the neighbors have been computed. In the standard approach, a simple "plurality vote" among neighbors is used to determine the label. In other approaches, the relative importance of each neighbor's label may be weighted by the inverse of its distance to `I`.


### Exercise #3: Implement a Monkey classification KNN function

The third exercise consists in implementing a KNN classification algorithm to retrieve the `species` attribute of `Monkey` objects whenever it is missing.

1. In your file `monkey_classif.py`, add a function `compute_knn(dataframe, k=5)`. **Read Part #4 carefully beforehand!**
  1. We'll consider that monkey datapoints are represented on a 2D plane, where the x-axis corresponds to the BMI, and the y-axis corresponds to the fur color.
  1. In your `utils.py` file, write a function `euclidean_distance`, which takes the coordinates of two points and returns their Euclidean distance. As a reminder, in the 2D plane, the Euclidean distance between points $p=\langle p_x, p_y \rangle$ and $q=\langle q_x, q_y \rangle$ is given by: $$d(p,q)=\sqrt{(p_x - q_x)^2 + (p_y - q_y)^2}$$.
  1. Add a test for `euclidean_distance` in `tests.py`. Make sure your code passes **all** your tests.
  1. Separate the monkeys into two groups: those which have an empty `str` for their `species` attribute, and those which haven't.
  1. Classify each monkey `m` in the first group (which have an empty `str` for their `species` attribute):
     1. compute the Euclidean distance of `m` to all monkeys in the second group (which don't have an empty `str` for their `species` attribute), using your `euclidean_distance` function 
     1. retrieve the species attributes of the `k` monkeys which are the nearest to the monkey `m` you're currently classifying
     1. assign the most frequent species among the `k` nearest neighbors as the species of monkey `m`(or ponder the importance based on the inverse of the distance, depending on the variant of the algorithm you wish to implement)
     1. optionnally (depending on the variant of the algorithm you wish to implement), add monkey `m` to the second group of monkeys (corresponding to those which have a non-empty species attribute)
  1. update the dataframe column `species`. 
  
  
Implement tests for this KNN classification function. This instruction is intentionally left vague: the aim is to have you think as to what the tests should be! **Read Part #2 carefully beforehand!**  All your tests should be in the file `tests.py`.


 
**Bonus #1**: Rewrite your function to use a functional programming style. **Read Part #3 carefully beforehand!** All your code should be written without `if`,`for` or `while` keywords. Here's a breakdown of how you can do it to guide you:

1. You can start by separating monkeys based on whether they have an empty `species` attribute or not using `filter` statements.
1. The core of the algorithm consists in removing monkeys one by one from the list of monkeys with empty `species`, and adding them to the list of monkeys with non-empty `species` attributes instead. This is equivalent to performing a `reduce ` over the first group (unspecied monkeys), using the second group (specied monkeys) as your initial value and accumulator.
1. If you use this `reduce` pattern, you will need to define a function that classifies one monkey: it needs to take as arguments a) the current list of specied monkeys and b) the current unspecied monkey, and returns the list of specied monkeys (a), potentially with an added element corresponding to the now-specied monkey (b) depending on the variant of the algorithm you implement.
1. Retrieving the $k$ nearest neighbors can be done using the `sorted` function, supplied with a sorting `key` based on Euclidean distance. 
1. To determine the most common species amongst neighbors, you might find [`collections.Counter.most_common()`](https://docs.python.org/3/library/collections.html#collections.Counter.most_common) to be helpful.

**Bonus #2**: Parametrize your code so that the end user can decide which monkey attributes to use for the KNN algorithm. The user must be able to choose any number ($\ge$ 2) of attributes among size, weight, BMI, fur color, fur color red value, fur color blue value, fur color green value and fur color intensity.


### Exercise #4: Add a command-line interface and save results

1. In your file `monkey_classif.py`, add a function `save_to_csv(dataframe, csv_filename)`, which takes a pandas dataframe and saves the values of the columns `species`, `fur_color`, `size` and `weight` to a CSV whose name should match the value of the argument `csv_filename`.
2. In your file `utils.py`, add a function `get_cli_args()`:
  1. Create an argument parser, which accepts as arguments a path to an input CSV, and a path to an output CSV. **Read Part #4 carefully beforehand!**
  2. parse and return the arguments 
3. In your file `monkey_classif.py`, add a `main()` function:
  1. Retrieve command-line interface arguments using your function `get_cli_args()`.
  1. Use the CSV file argument to compute the dataframe from exercise #2.
  1. Use this dataframe to compute the KNN classification from exercise #3.
  1. Save the results using the function `save_to_csv`


Implement tests for this command-line interface and save feature. This instruction is intentionally left vague: the aim is to have you think as to what the tests should be!  Make sure your code passes **all** your tests. **Read Part #2 carefully beforehand!**  All your tests should be in the file `tests.py`.


### Exercise #5: Add a visualization scatterplot

1. In your file `utils.py`, modify your function `get_cli_args()`. **Read Part #4 carefully beforehand!** 
  1. Transform the current arguments into arguments for a sub-command `knn`
  2. Add a new sub-command `visualize`. This sub-command must take as argument:
      1. a path to a CSV file as well
      2. two strings representing features for which we'll produce a visualization. Use the keywords`nargs` to ensure the user passes the correct number of strings, and the keywords `choices` to make sure the user passes only valid column names from the dataframe.
2. Modify the function `read_monkeys_from_csv` from your file `monkey_classif.py`. 
  1. Add a keyword `strict`, defaulting to `False`.
  2. Modify he behavior of this function so that when in `strict` mode, it raises a `ValueError`if any row is missing any value (including for the column `species`). 
3. In your file `monkey_visualize.py`, write a function `scatter_plot(X, Y, labels)` that produces a scatter plot using matplotlib. **Read Part #4 carefully beforehand!**.
  1. All three arguments should have the same length (or be `numpy` `ndarray` of the same 1D shape). Use an `assert` statement to verify this.
  2. `X` should correspond to the x-axes of all datapoints to be scattered.
  3. `Y` should correspond to the y-axes of all datapoints to be scattered.
  4. `labels` should indicate which group each datapoint should belong to. Datapoints with the same labels belong to the same group.
  5. Datapoints of the same group should appear in the same color
  6. Add a legend to the visualization, mapping colors to group labels.
4. Modify the function `main()` from your file `monkey_classif.py`.
  1. make sure the original behavior is only executed of the command-line arguments specify the sub-command `knn`.
  2. when the command-line arguments specify the sub-command `visualize`:
      1. load a CSV file in `strict` mode
      2. retrieve the two column sequences corresponding to the two features selected by the user, to use as `X` and `Y` coordinates for the scatterplot.
      3. retrieve the species column, to use as the `labels` of your scatter plot.
      4. call the `scatter_plot` function accordingly.

Implement unit tests for the visualization. This instruction is intentionally left vague: the aim is to have you think as to what the tests should be!  Make sure your code passes **all** your tests. **Read Part #2 carefully beforehand!**  All your tests should be in the file `tests.py`.

## Part #2: Debugging & TDD

Everyone makes mistakes when coding. It's normal to fumble and stumble. On the other hand, a good developper knows how to correct their mistakes quickly, and not be bogged down by bugs. 

This second part of the notebook is dedicated to tools and practices that you should adopt to reach that goal.

### Review #2.1: `pdb`

`pdb` stands for [Python Debugger](https://docs.python.org/3/library/pdb.html). It's a tool that comes shipped in with most Python installations. It allows you to run your code interactively, inspect the values of variables at a specific point of the execution process, and follow step-by-step what your code is actually doing. It's an extremely useful tool, that can help you fix and improve your code. We strongly encourage you to start using it. Even if it seems a bit daunting at first, being fluent with `pdb` will speed up your debugging by all lot.


#### Firing up the debugger

There are two ways to start the debugger:

1. From the terminal, instead of running `python my_script.py`, run `python -m pdb my_script.py`. This will start the debugger and halt for user input before executing your code.
2. Within your script, add the line `import pdb; pdb.set_trace()` wherever. When this line is encountered, this will start the debugger and halt for user input at the current step of the execution. **When using this solution, be careful to remove this instruction once you're done with debugging!**

When halting for user input, the debugger gives ytou access to a full Python interactive interpreter, populated with the variables at the current point in the execution process.

**NB:** *If you're coding using Jupyter, do note that you wouldneed a different tool, [`ipdb`](https://pypi.org/project/ipdb/). We encourage you to use a proper IDE to handle complex, multi-file projects such as this one.*


#### Breakpoints

The main feature of the debugger is to add **breakpoints**. A breakpoint is a marker that tells the debugger where to pause execution and wait for user input.

- In `pdb`, you can set a breakpoint using `b` (or `break`), followed by a line number: e.g., typing `b 42` will halt execution whenever your code tries to execute the 42nd line of your code.
- If you want to set a breakpoint on an instruction in a different file, you can type `b other_file.py:l`, where `other_file.py` is a path to the other python file you're targetting, and `l` is the line number in that file.
- You can also use qualified function names to set breakpoints: `b my_module.MyClass.my_method` will halt execution whenever the method `my_method` of the class `MyClass` in the module `my_module` is called. 
- You can list all current breakpoints by typing `b`, without arguments. You can remove all existing breakpoints using `cl` (or `clear`), and you can remove one specific breakpoint by typing `cl B`, where `B` is the breakpoint number for the breakpoint you want to remove.


#### Major commands

There are many debugger commands. Here are a few useful ones, but we strongly encourage you to read through [the official documentation](https://docs.python.org/3.9/library/pdb.html#debugger-commands)
- `n` or `next` performs the next instruction
- `s` or `step` "steps into" the current instruction: if it's a function call, for instance, it will move the debugger to this function.
- `w` or `where`prints a stack trace: it tells you what functions have indirectly called the function you're currently in.
- `c` or `continue` just resumes the execution process, until you hit another breakpoint
- `q` or `quit` quits the debugger and stops the execution process
- `p` or `print` prints the value of the argument statement.


#### Example run

Here's a small example of a `pdb`debugging session. We're using the correction of lab1 in this demo, so go retrieve it on Arche to follow along. 
```
tmickus@sleipnir:~/Documents/lectures/prog/lab1$ python3 -m pdb lab1_lab1-getting-you-started_sol.py 
> /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(33)<module>()
-> something_very_important = 42
(Pdb) b fizzbuzz
Breakpoint 1 at /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py:102
(Pdb) b 107
Breakpoint 2 at /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py:107
(Pdb) c
42
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
Hello, world!
> /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(104)fizzbuzz()
-> total = 0
(Pdb) n
> /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(105)fizzbuzz()
-> for i in range(n):
(Pdb) n
> /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(106)fizzbuzz()
-> if i % 3 == 0 or i % 5 == 0:
(Pdb) n
> /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(107)fizzbuzz()
-> total += i
(Pdb) p total
0
(Pdb) p i
0
(Pdb) c
> /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(107)fizzbuzz()
-> total += i
(Pdb) p total, i
(0, 3)
(Pdb) c
> /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(107)fizzbuzz()
-> total += i
(Pdb) p total, i
(3, 5)
(Pdb) c
> /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(107)fizzbuzz()
-> total += i
(Pdb) p total, i
(8, 6)
(Pdb) where
  /usr/lib/python3.6/bdb.py(434)run()
-> exec(cmd, globals, locals)
  <string>(1)<module>()
  /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(110)<module>()
-> fizzbuzz(1001)
> /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py(107)fizzbuzz()
-> total += i
(Pdb) b
Num Type         Disp Enb   Where
1   breakpoint   keep yes   at /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py:102
	breakpoint already hit 1 time
2   breakpoint   keep yes   at /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py:107
	breakpoint already hit 3 times
(Pdb) cl 1
Deleted breakpoint 1 at /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py:102
(Pdb) cl 
Clear all breaks? y
Deleted breakpoint 2 at /home/tmickus/Documents/lectures/prog/lab1/lab1_lab1-getting-you-started_sol.py:107
(Pdb) q
tmickus@sleipnir:~/Documents/lectures/prog/lab1$
```

Here's a summary of what the above corresponds to:

- We start by setting two breakpoints, one when calling the function `fizzbuzz` the other at line 107
- We resume execution until hitting a breakpoint
- We use a series of `next` commands to move through the function
- We evaluate the values of variables `total` and `i`, and run through a couple of loops 
- We call the `where` command to have a small stack trace of which functions brought us here
- we call `b` to have a list of all current breakpoints, and then clear those manually using `cl`
- We quit using `q`.

In short, `pdb` can help you navigate through your code, and check what it is that your code is doing exactly. As such, you can have a finer understanding of what you actually coded, and have an interactive debugging process, instead of blindly trying out patches one by one until you've hit on something that seems to work. 

### Review #2.2 & Bonus Exercises: TDD & Unit-tests

This part of the lab is a jupyter adaption of https://diveintopython3.problemsolving.io/unit-testing.html (under Creative Commons Attribution Share-Alike license).

**Note that the exercises in this section  are entirely optional. This section of the lab is here to teach you how TDD works.** The idea is to give you an interactive apporach to TDD and unit-test that you can apply to your monkey classification KNN later on.

In this section, you’re going to write and debug a set of utility functions to convert to and from Roman numerals. 
Mechanics of constructing and validating Roman numerals can be seen in [“Case study: roman numerals”](https://diveintopython3.problemsolving.io/regular-expressions.html#romannumerals).
In the following, such mechanisms are recalled and usually provided, you only need to focus on writing tests.


Recall that: in Roman numerals, there are seven characters that are repeated and combined in various ways to represent numbers.

* I = 1
* V = 5
* X = 10
* L = 50
* C = 100
* D = 500
* M = 1000 

The following are some general rules for constructing Roman numerals:

* Sometimes characters are additive. I is 1, II is 2, and III is 3. VI is 6 (literally, “5 and 1”), VII is 7, and VIII is 8.
* The tens characters (I, X, C, and M) can be repeated up to three times. At 4, you need to subtract from the next highest fives character. You can't represent 4 as IIII; instead, it is represented as IV (“1 less than 5”). 40 is written as XL (“10 less than 50”), 41 as XLI, 42 as XLII, 43 as XLIII, and then 44 as XLIV (“10 less than 50, then 1 less than 5”).
* Sometimes characters are… the opposite of additive. By putting certain characters before others, you subtract from the final value. For example, at 9, you need to subtract from the next highest tens character: 8 is VIII, but 9 is IX (“1 less than 10”), not VIIII (since the I character can not be repeated four times). 90 is XC, 900 is CM.
* The fives characters can not be repeated. 10 is always represented as X, never as VV. 100 is always C, never LL.
* Roman numerals are read left to right, so the order of characters matters very much. DC is 600; CD is a completely different number (400, “100 less than 500”). CI is 101; IC is not even a valid Roman numeral (because you can't subtract 1 directly from 100; you would need to write it as XCIX, “10 less than 100, then 1 less than 10”). 

The rules for Roman numerals lead to a number of interesting observations:

1. There is only one correct way to represent a particular number as a Roman numeral.
2. The converse is also true: if a string of characters is a valid Roman numeral, it represents only one number (that is, it can only be interpreted one way).
3. There is a limited range of numbers that can be expressed as Roman numerals, specifically 1 through 3999. The Romans did have several ways of expressing larger numbers, for instance by having a bar over a numeral to represent that its normal value should be multiplied by 1000. For the purposes of this chapter, let’s stipulate that Roman numerals go from 1 to 3999.
4. There is no way to represent 0 in Roman numerals.
5. There is no way to represent negative numbers in Roman numerals.
6. There is no way to represent fractions or non-integer numbers in Roman numerals. 

Let’s start mapping out what our code should do. It will have two main functions, ``to_roman()`` and ``from_roman()``. The ``to_roman()`` function should take an integer from 1 to 3999 and return the Roman numeral representation as a string.

Stop right there. Now let’s do something a little unexpected: write a test case that checks whether the ``to_roman()`` function does what you want it to. You read that right: you’re going to write code that tests code that you haven’t written yet.

This is called **test-driven development**, or TDD. The set of two conversion functions — ``to_roman()``, and later ``from_roman()`` — can be written and tested as a unit, separate from any larger program that imports them. Python has a framework for unit testing, the appropriately-named ``unittest`` module.

Unit testing is an important part of an overall testing-centric development strategy. If you write unit tests, it is important to write them early and to keep them updated as code and requirements change. Many people advocate writing tests before they write the code they’re testing, and that’s the style we're going to adopt in this lab. But unit tests are beneficial no matter when you write them.

* Before writing code, writing unit tests forces you to detail your requirements in a useful fashion.
* While writing code, unit tests keep you from over-coding. When all the test cases pass, the function is complete.
* When refactoring code, they can help prove that the new version behaves the same way as the old version.
* When maintaining code, having tests will help you cover your ass when someone comes screaming that your latest change broke their old code. (“But sir, all the unit tests passed when I checked it in...”)
* When writing code in a team, having a comprehensive test suite dramatically decreases the chances that your code will break someone else’s code, because you can run their unit tests first. (I’ve seen this sort of thing in code sprints. A team breaks up the assignment, everybody takes the specs for their task, writes unit tests for it, then shares their unit tests with the rest of the team. That way, nobody goes off too far into developing code that doesn’t play well with others.) 

#### Bonus Exercise #6 A Single Question

A test case answers a single question about the code it is testing. A test case should be able to...

* ...run completely by itself, without any human input. Unit testing is about automation.
* ...determine by itself whether the function it is testing has passed or failed, without a human interpreting the results.
* ...run in isolation, separate from any other test cases (even if they test the same functions). Each test case is an island. 

Given that, fill the following code to test:

1. The ``to_roman()`` function should return the Roman numeral representation for all integers 1 to 3999. 

It is not immediately obvious how this code does... well, anything. It defines a class which has no __init__() method. The class does have another method, but it is never called. The entire script has a __main__ block, but it doesn’t reference the class or its method. But it does do something, we promise. 


```python
import unittest

# Add to_roman function here -- See Explanation 6

class KnownValues(unittest.TestCase): # See Explanation 1.              
    known_values = ()  # Fill this with tuples of (input, expected output) -- See Explanation 2.
    
    def test_to_roman_known_values(self):  # See Explanation 3       
        '''test that to_roman should give known result with known input'''
        pass  # See Explanations 4 and 5

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)  # Special call; different from slides to be able to run unittest in jupyter notebooks
```

1. To write a test case, first we need to subclass the ``TestCase`` class of the unittest module. This class provides many useful methods which you can use in your test case to test specific conditions.
2. ``known_values`` consists in a tuple of integer/numeral pairs that you verified manually. It can include the lowest ten numbers, the highest number, every number that translates to a single-character Roman numeral, and a random sampling of other valid numbers. You don’t need to test every possible input, but you should try to test all the obvious edge cases.
3. Every individual test is its own method. A test method takes no parameters, returns no value, and must have a name beginning with the four letters test. If a test method exits normally without raising an exception, the test is considered passed; if the method raises an exception, the test is considered failed.
4. Here you should call the actual ``to_roman()`` function for every known value. (Well, the function hasn’t been written yet, but once it is, this is the line that will call it.) Notice that you have now defined the API for the ``to_roman()`` function: it must take an integer (the number to convert) and return a string (the Roman numeral representation). If the API is different than that, this test is considered failed. Also notice that you are not trapping any exceptions when you call ``to_roman()``. This is intentional. ``to_roman()`` shouldn’t raise an exception when you call it with valid input, and these input values are all valid. If ``to_roman()`` raises an exception, this test is considered failed.
5. Assuming the ``to_roman()`` function was defined correctly, called correctly, completed successfully, and returned a value, the last step for every known value is to check whether it returned the right value. This is a common question, and the ``TestCase`` class provides a method, ``assertEqual``, to check whether two values are equal. If the result returned from ``to_roman()`` does not match the known value you were expecting (numeral), ``assertEqual`` will raise an exception and the test will fail. If the two values are equal, ``assertEqual`` will do nothing. If every value returned from ``to_roman()`` matches the known value you expect, ``assertEqual`` never raises an exception, so ``test_to_roman_known_values`` eventually exits normally, which means ``to_roman()`` has passed this test. 
6. Once you have a test case, you can start coding the ``to_roman()`` function. First, you should stub it out as an empty function and make sure the tests fail. If the tests succeed before you’ve written any code, your tests aren’t testing your code at all! Unit testing is a dance: tests lead, code follows. Write a test that fails, then code until it passes. At this stage, you want to define the API of the ``to_roman()`` function, but you don’t want to code it yet. (Your test needs to fail first.) To stub it out, use the Python reserved word ``pass``, which does precisely nothing. 


When executing your code, you should get something like:

```
test_to_roman_known_values (__main__.KnownValues)                    (1)  
to_roman should give known result with known input ... FAIL          (2)  

======================================================================
FAIL: to_roman should give known result with known input
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest1.py", line 73, in test_to_roman_known_values
    self.assertEqual(numeral, result)
AssertionError: 'I' != None                                          (3)  

----------------------------------------------------------------------
Ran 1 test in 0.016s                                                 (4)  

FAILED (failures=1)                                                  (5)
```

1. Running the cell runs ``unittest.main()``, which runs each test case. Each test case is a method within a test class. There is no required organization of these test classes; they can each contain a single test method, or you can have one class that contains multiple test methods. The only requirement is that each test class must inherit from ``unittest.TestCase``.
2. For each test case, the ``unittest`` module will print out the docstring of the method and whether that test passed or failed. As expected, this test case fails.
3. For each failed test case, unittest displays the trace information showing exactly what happened. In this case, the call to ``assertEqual()`` raised an ``AssertionError`` because it was expecting to_roman(1) to return 'I', but it didn’t. (Since there was no explicit return statement, the function returned ``None``, the Python null value.)
4. After the detail of each test, ``unittest`` displays a summary of how many tests were performed and how long it took.
5. Overall, the test run failed because at least one test case did not pass. When a test case doesn’t pass, ``unittest`` distinguishes between failures and errors. A failure is a call to an ``assertXYZ`` method, like ``assertEqual`` or ``assertRaises``, that fails because the asserted condition is not true or the expected exception was not raised. An error is any other sort of exception raised in the code you’re testing or the unit test case itself. 

*Now*, finally, you can complete the ``to_roman()`` function.

Hint: you can use:

```python
roman_numeral_map = (('M',  1000),
                     ('CM', 900),
                     ('D',  500),
                     ('CD', 400),
                     ('C',  100),
                     ('XC', 90),
                     ('L',  50),
                     ('XL', 40),
                     ('X',  10),
                     ('IX', 9),
                     ('V',  5),
                     ('IV', 4),
                     ('I',  1)) 
```

It is a tuple of tuples which defines three things: the character representations of the most basic Roman numerals; the order of the Roman numerals (in descending value order, from M all the way down to I); the value of each Roman numeral. Each inner tuple is a pair of (numeral, value). It’s not just single-character Roman numerals; it also defines two-character pairs like CM (“one hundred less than one thousand”). This makes the ``to_roman()`` function code simpler. 

If you run again the cell, will the ``to_roman()`` function pass the test case you wrote?

```
test_to_roman_known_values (__main__.KnownValues)
to_roman should give known result with known input ... ok               (1)

----------------------------------------------------------------------
Ran 1 test in 0.016s

OK
```

1. Hooray! The ``to_roman()`` function passes the “known values” test case. It’s not comprehensive, but it does put the function through its paces with the inputs you provided. If you included, e.g., inputs that produce every single-character Roman numeral, the largest possible input (3999), and the input that produces the longest possible Roman numeral (3888), at this point, you can be reasonably confident that the function works for any good input value you could throw at it.

“Good” input? Hmm. What about bad input? 

#### Bonus Exercise #7: “Halt And Catch Fire”

It is not enough to test that functions succeed when given good input; you must also test that they fail when given bad input. And not just any sort of failure; they must fail in the way you expect. 

```python
to_roman(4000)  # Returns 'MMMM' for now; bad
to_roman(5000)  # Returns 'MMMMM' for now; bad
to_roman(9000)  # Returns 'MMMMMMMMM'? for now; bad
```

That’s definitely not what you wanted — that’s not even valid Roman numerals! Each of these numbers is outside the range of acceptable input, but the function returns a bogus value anyway. **Silently returning bad values is baaaaaaad**; if a program is going to fail, it is far better if it fails quickly and noisily. “Halt and catch fire,” as the saying goes. The Pythonic way to halt and catch fire is to raise an exception.

The question to ask yourself is, “How can I express this as a testable requirement?” How’s this for starters:

* The ``to_roman()`` function should raise an ``OutOfRangeError`` when given an integer greater than 3999. 

In the following code cell, follow instructions:

1. Copy-paste your code from the previous section
2. Create a class ``ToRomanBadInput`` that inherits from ``unittest.TestCase``. 

You can have more than one test per class (as you’ll see later in this lab), but we chose to create a new class here because this test is something different than the last one. We’ll keep all the good input tests together in one class, and all the bad input tests together in another. 

Like the previous test case, the test itself should be a method of the class, with a name starting with ``test``. 

To write the test, use the ``assertRaises`` method, which takes the following arguments: the exception you’re expecting, the function you’re testing, and the arguments you’re passing to that function. (If the function you’re testing takes more than one argument, pass them all to ``assertRaises``, in order, and it will pass them right along to the function you’re testing.) 


```python
# 1. Here, copy-paste your code (to_roman function and KnownValues class) from the previous section

# 2. Here, create a new test class ToRomanBadInput

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)  # Special call; different from slides to be able to run unittest in jupyter notebooks
```

Pay close attention to thie ``assertRaises``. Instead of calling ``to_roman()`` directly and manually checking that it raises a particular exception (by wrapping it in a ``try...except`` block), the ``assertRaises`` method has encapsulated all of that for us. All you do is tell it what exception you’re expecting (``OutOfRangeError``), the function (``to_roman()``), and the function’s arguments (4000). The assertRaises method takes care of calling ``to_roman()`` and checking that it raises ``OutOfRangeError``.

Also note that you’re passing the ``to_roman()`` function itself as an argument; you’re not calling it, and you’re not passing the name of it as a string. Have we mentioned how handy it is that everything in Python is an object?

So what happens when you run the test suite with this new test? 

```
test_to_roman_known_values (__main__.KnownValues)
to_roman should give known result with known input ... ok
test_too_large (__main__.ToRomanBadInput)
to_roman should fail with large input ... ERROR                         (1)

======================================================================
ERROR: to_roman should fail with large input                          
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest2.py", line 78, in test_too_large
    self.assertRaises(roman2.OutOfRangeError, roman2.to_roman, 4000)
AttributeError: 'module' object has no attribute 'OutOfRangeError'      (2)

----------------------------------------------------------------------
Ran 2 tests in 0.000s

FAILED (errors=1)
```

1. You should have expected this to fail (since you haven’t written any code to pass it yet), but... it didn’t actually “fail,” it had an “error” instead. This is a subtle but important distinction. A unit test actually has three return values: pass, fail, and error. Pass, of course, means that the test passed — the code did what you expected. “Fail” is what the previous test case did (until you wrote code to make it pass) — it executed the code but the result was not what you expected. “Error” means that the code didn’t even execute properly.
2. Why didn’t the code execute properly? The traceback tells all. The module you’re testing doesn’t have an exception called ``OutOfRangeError``. Remember, you passed this exception to the ``assertRaises()`` method, because it’s the exception you want the function to raise given an out-of-range input. But the exception doesn’t exist, so the call to the ``assertRaises()`` method failed. It never got a chance to test the ``to_roman()`` function; it didn’t get that far. 

To solve this problem, you need to define the ``OutOfRangeError`` exception.
An “out of range” error is a kind of value error — the argument value is out of its acceptable range. So this exception should inherit from the built-in ``ValueError`` exception. This is not strictly necessary (it could just inherit from the base Exception class), but it feels right.

Now run the test suite again. 

```
test_to_roman_known_values (__main__.KnownValues)
to_roman should give known result with known input ... ok
test_too_large (__main__.ToRomanBadInput)
to_roman should fail with large input ... FAIL                          (1)

======================================================================
FAIL: to_roman should fail with large input
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest2.py", line 78, in test_too_large
    self.assertRaises(roman2.OutOfRangeError, roman2.to_roman, 4000)
AssertionError: OutOfRangeError not raised by to_roman                 (2)

----------------------------------------------------------------------
Ran 2 tests in 0.016s

FAILED (failures=1)
```

1. The new test is still not passing, but it’s not returning an error either. Instead, the test is failing. That’s progress! It means the call to the ``assertRaises()`` method succeeded this time, and the unit test framework actually tested the ``to_roman()`` function.
2. Of course, the ``to_roman()`` function isn’t raising the ``OutOfRangeError`` exception you just defined, because you haven’t told it to do that yet. That’s excellent news! It means this is a valid test case — it fails before you write the code to make it pass. 

Now you can modify the code of ``to_roman()`` to make this test pass.

This is straightforward: if the given input (n) is greater than 3999, raise an ``OutOfRangeError`` exception. The unit test does not check the human-readable string that accompanies the exception, although you could write another test that did check it (but watch out for internationalization issues for strings that vary by the user’s language or environment).

Does this make the test pass? Let’s find out by executing again the cell. You should get something like

```
test_to_roman_known_values (__main__.KnownValues)
to_roman should give known result with known input ... ok
test_too_large (__main__.ToRomanBadInput)
to_roman should fail with large input ... ok                        (1)    

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

1. Hooray! Both tests pass. Because you worked iteratively, bouncing back and forth between testing and coding, you can be sure that the two lines of code you just wrote were the cause of that one test going from “fail” to “pass.” That kind of confidence doesn’t come cheap, but it will pay for itself over the lifetime of your code. 

#### Bonus Exercise #8: More Halting, More Fire

Along with testing numbers that are too large, you need to test numbers that are too small. As we noted in our functional requirements, Roman numerals cannot express 0 or negative numbers.

```python
to_roman(0)  # Returns '' for now; bad
to_roman(-1) # Returns '' for now; bad
```

Well that’s not good. Let’s add tests for each of these conditions. 

In the following code cell, copy paste your code from the previous section and complete the class ``ToRomanBadInput`` with two new methods ``test_zero`` and ``test_negative``, both relying on ``assertRaises`` and the ``OutOfRangeError`` exception.


```python
# Copy paste your code from the previous section and complete the class ToRomanBadInput with two new methods test_zero and test_negative
```

1. The ``test_too_large()`` method has not changed since the previous step.
2. You should add a new test: the ``test_zero()`` method. Like the ``test_too_large()`` method, it tells the ``assertRaises()`` method defined in ``unittest.TestCase`` to call our ``to_roman()`` function with a parameter of 0, and check that it raises the appropriate exception, ``OutOfRangeError``. 
3. The ``test_negative()`` method is almost identical, except it passes -1 to the ``to_roman()`` function. If either of these new tests does not raise an ``OutOfRangeError`` (either because the function returns an actual value, or because it raises some other exception), the test is considered failed.

Now check that the tests fail: 

```
test_to_roman_known_values (__main__.KnownValues)
to_roman should give known result with known input ... ok
test_negative (__main__.ToRomanBadInput)
to_roman should fail with negative input ... FAIL
test_too_large (__main__.ToRomanBadInput)
to_roman should fail with large input ... ok
test_zero (__main__.ToRomanBadInput)
to_roman should fail with 0 input ... FAIL

======================================================================
FAIL: to_roman should fail with negative input
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest3.py", line 86, in test_negative
    self.assertRaises(roman3.OutOfRangeError, roman3.to_roman, -1)
AssertionError: OutOfRangeError not raised by to_roman

======================================================================
FAIL: to_roman should fail with 0 input
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest3.py", line 82, in test_zero
    self.assertRaises(roman3.OutOfRangeError, roman3.to_roman, 0)
AssertionError: OutOfRangeError not raised by to_roman

----------------------------------------------------------------------
Ran 4 tests in 0.000s

FAILED (failures=2)
```

If you get a similar result, it's excellent: both tests failed, as expected. Now let’s switch over to the code and see what we can do to make them pass. 

You can now complete the ``to_roman()`` function. Catch in one line of code inputs that are too large, negative, or zero. 

You can now run the tests. They should all pass:

```
test_to_roman_known_values (__main__.KnownValues)
to_roman should give known result with known input ... ok
test_negative (__main__.ToRomanBadInput)
to_roman should fail with negative input ... ok
test_too_large (__main__.ToRomanBadInput)
to_roman should fail with large input ... ok
test_zero (__main__.ToRomanBadInput)
to_roman should fail with 0 input ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.016s

OK
```

#### Bonus Exercise #9: And One More Thing...

There was one more functional requirement for converting numbers to Roman numerals: dealing with non-integers. 

```python
to_roman(0.5)  # Returns '' for now; bad
to_roman(1.0)  # Returns 'I' for now; bad
```

Both of these cases should raise an exception. Instead, they give bogus results. 

Testing for non-integers is not difficult. First, copy paste your code from the previous section in the cell below. 

* Define a ``NotIntegerError`` exception.
* Next, write a test case in ``ToRomanBadInput`` that checks for the NotIntegerError exception. 


```python
# Copy paste your code from the previous section and complete it
```

* Now check that the test fails properly. 

```
test_to_roman_known_values (__main__.KnownValues)
to_roman should give known result with known input ... ok
test_negative (__main__.ToRomanBadInput)
to_roman should fail with negative input ... ok
test_non_integer (__main__.ToRomanBadInput)
to_roman should fail with non-integer input ... FAIL
test_too_large (__main__.ToRomanBadInput)
to_roman should fail with large input ... ok
test_zero (__main__.ToRomanBadInput)
to_roman should fail with 0 input ... ok

======================================================================
FAIL: to_roman should fail with non-integer input
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest4.py", line 90, in test_non_integer
    self.assertRaises(roman4.NotIntegerError, roman4.to_roman, 0.5)
AssertionError: NotIntegerError not raised by to_roman

----------------------------------------------------------------------
Ran 5 tests in 0.000s

FAILED (failures=1)
```

* Write the code that makes the test pass (hint: use ``isinstance()`` that tests whether a variable is a particular type or, technically, any descendant type)
* Finally, check that the code does indeed make the test pass. 

```
test_to_roman_known_values (__main__.KnownValues)
to_roman should give known result with known input ... ok
test_negative (__main__.ToRomanBadInput)
to_roman should fail with negative input ... ok
test_non_integer (__main__.ToRomanBadInput)
to_roman should fail with non-integer input ... ok
test_too_large (__main__.ToRomanBadInput)
to_roman should fail with large input ... ok
test_zero (__main__.ToRomanBadInput)
to_roman should fail with 0 input ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

The ``to_roman()`` function passes all of its tests, and we can’t think of any more tests, so it’s time to move on to ``from_roman()``. 

#### Bonus Exercise #10: A Pleasing Symmetry

Converting a string from a Roman numeral to an integer sounds more difficult than converting an integer to a Roman numeral. 

Certainly there is the issue of validation. It’s easy to check if an integer is greater than 0, but a bit harder to check whether a string is a valid Roman numeral. We will give you later a regular expression to check for Roman numerals, so that part can be easily done. 

That leaves the problem of converting the string itself. As we’ll see in a minute, thanks to the rich data structure we defined to map individual Roman numerals to integer values, the nitty-gritty of the ``from_roman()`` function is as straightforward as the ``to_roman()`` function. 

But first, the tests. We’ll need a “known values” test to spot-check for accuracy. Our test suite already contains a mapping of known values (``known_values`` in the ``KnownValues`` class); let’s reuse that. 

Copy paste your code from the previous section and complete it following our instructions


```python
# Copy paste your code from the previous section and complete it
```

* Add a ``test_from_roman_known_values`` method in the ``KnownValues`` class, testing the ``from_roman()`` function using the ``known_values`` tuple. It is very similar to ``test_to_roman_known_values``

There’s a pleasing symmetry here. The ``to_roman()`` and ``from_roman()`` functions are inverses of each other. The first converts integers to specially-formatted strings, the second converts specially-formated strings to integers. In theory, we should be able to “round-trip” a number by passing to the ``to_roman()`` function to get a string, then passing that string to the ``from_roman()`` function to get an integer, and end up with the same number: 

```python
n = from_roman(to_roman(n)) for all values of n
```

In this case, “all values” means any number between 1..3999, since that is the valid range of inputs to the ``to_roman()`` function. We can express this symmetry in a test case that runs through all the values 1..3999, calls ``to_roman()``, calls ``from_roman()``, and checks that the output is the same as the original input. 

* Add a ``RoundtripCheck`` class with a ``test_roundtrip`` method implementing such a behavior.

These new tests won’t even fail yet. We haven’t defined a ``from_roman()`` function at all, so they’ll just raise errors. 

```
E.E....
======================================================================
ERROR: test_from_roman_known_values (__main__.KnownValues)
from_roman should give known result with known input
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest5.py", line 78, in test_from_roman_known_values
    result = roman5.from_roman(numeral)
AttributeError: 'module' object has no attribute 'from_roman'

======================================================================
ERROR: test_roundtrip (__main__.RoundtripCheck)
from_roman(to_roman(n))==n for all n
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest5.py", line 103, in test_roundtrip
    result = roman5.from_roman(numeral)
AttributeError: 'module' object has no attribute 'from_roman'

----------------------------------------------------------------------
Ran 7 tests in 0.019s

FAILED (errors=2)
```

* Implement a quick stub function to solve that problem (only docstring or with the ``pass`` instruction)

Now the test cases will actually fail. 

```
F.F....
======================================================================
FAIL: test_from_roman_known_values (__main__.KnownValues)
from_roman should give known result with known input
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest5.py", line 79, in test_from_roman_known_values
    self.assertEqual(integer, result)
AssertionError: 1 != None

======================================================================
FAIL: test_roundtrip (__main__.RoundtripCheck)
from_roman(to_roman(n))==n for all n
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest5.py", line 104, in test_roundtrip
    self.assertEqual(integer, result)
AssertionError: 1 != None

----------------------------------------------------------------------
Ran 7 tests in 0.002s

FAILED (failures=2)
```

* Now it’s time to complete the ``from_roman()`` function. 

The pattern here is the same as the ``to_roman()`` function. You iterate through your Roman numeral data structure (``roman_numeral_map``, a tuple of tuples), but instead of matching the highest integer values as often as possible, you match the “highest” Roman numeral character strings as often as possible. 

Time to re-run the tests. 

```
.......
----------------------------------------------------------------------
Ran 7 tests in 0.060s

OK
```

Two pieces of exciting news here. The first is that the ``from_roman()`` function works for good input, at least for all the known values. The second is that the “round trip” test also passed. Combined with the known values tests, you can be reasonably sure that both the ``to_roman()`` and ``from_roman()`` functions work properly for all possible good values. (This is not guaranteed; it is theoretically possible that ``to_roman()`` has a bug that produces the wrong Roman numeral for some particular set of inputs, and that ``from_roman()`` has a reciprocal bug that produces the same wrong integer values for exactly that set of Roman numerals that ``to_roman()`` generated incorrectly. Depending on your application and your requirements, this possibility may bother you; if so, write more comprehensive test cases until it doesn't bother you.) 

#### Bonus Exercise #11: More Bad Input

Now that the ``from_roman()`` function works properly with good input, it's time to fit in the last piece of the puzzle: making it work properly with bad input. That means finding a way to look at a string and determine if it's a valid Roman numeral. This is inherently more difficult than validating numeric input in the ``to_roman()`` function, but you have a powerful tool at your disposal: regular expressions. (If you’re not familiar with regular expressions, now would be a good time to learn about them.)

There are several simple rules for constructing a Roman numeral, using the letters M, D, C, L, X, V, and I. Let's review the rules:

* Sometimes characters are additive. I is 1, II is 2, and III is 3. VI is 6 (literally, “5 and 1”), VII is 7, and VIII is 8.
* The tens characters (I, X, C, and M) can be repeated up to three times. At 4, you need to subtract from the next highest fives character. You can't represent 4 as IIII; instead, it is represented as IV (“1 less than 5”). 40 is written as XL (“10 less than 50”), 41 as XLI, 42 as XLII, 43 as XLIII, and then 44 as XLIV (“10 less than 50, then 1 less than 5”).
* Sometimes characters are... the opposite of additive. By putting certain characters before others, you subtract from the final value. For example, at 9, you need to subtract from the next highest tens character: 8 is VIII, but 9 is IX (“1 less than 10”), not VIIII (since the I character can not be repeated four times). 90 is XC, 900 is CM.
* The fives characters can not be repeated. 10 is always represented as X, never as VV. 100 is always C, never LL.
* Roman numerals are read left to right, so the order of characters matters very much. DC is 600; CD is a completely different number (400, “100 less than 500”). CI is 101; IC is not even a valid Roman numeral (because you can't subtract 1 directly from 100; you would need to write it as XCIX, “10 less than 100, then 1 less than 10”). 

Thus, one useful test would be to ensure that the ``from_roman()`` function should fail when you pass it a string with too many repeated numerals. How many is “too many” depends on the numeral. 

In the following code cell, copy-paste your code and complete it following our instructions


```python
# Copy paste your code from the previous section and complete it
```

* Add a class ``FromRomanBadInput`` with a test method ``test_too_many_repeated_numerals``. This method tests the occurence of the ``InvalidRomanNumeralError`` exception when passing invalid roman numbers with repeated numerals, e.g., "MMMM".
* Another useful test to add ``test_repeated_pairs`` would be to check that certain patterns aren’t repeated. For example, IX is 9, but IXIX is never valid. 
* A third test (``test_malformed_antecedents``) could check that numerals appear in the correct order, from highest to lowest value. For example, CL is 150, but LC is never valid, because the numeral for 50 can never come before the numeral for 100. This test includes a randomly chosen set of invalid antecedents: I before M, V before X, and so on. 

Each of these tests relies the ``from_roman()`` function raising a new exception, ``InvalidRomanNumeralError``, which we haven’t defined yet. 

All three of these tests should fail, since the ``from_roman()`` function doesn’t currently have any validity checking. (If they don’t fail now, then what the heck are they testing?) 

```
FFF.......
======================================================================
FAIL: test_malformed_antecedents (__main__.FromRomanBadInput)
from_roman should fail with malformed antecedents
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest6.py", line 113, in test_malformed_antecedents
    self.assertRaises(roman6.InvalidRomanNumeralError, roman6.from_roman, s)
AssertionError: InvalidRomanNumeralError not raised by from_roman

======================================================================
FAIL: test_repeated_pairs (__main__.FromRomanBadInput)
from_roman should fail with repeated pairs of numerals
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest6.py", line 107, in test_repeated_pairs
    self.assertRaises(roman6.InvalidRomanNumeralError, roman6.from_roman, s)
AssertionError: InvalidRomanNumeralError not raised by from_roman

======================================================================
FAIL: test_too_many_repeated_numerals (__main__.FromRomanBadInput)
from_roman should fail with too many repeated numerals
----------------------------------------------------------------------
Traceback (most recent call last):
  File "romantest6.py", line 102, in test_too_many_repeated_numerals
    self.assertRaises(roman6.InvalidRomanNumeralError, roman6.from_roman, s)
AssertionError: InvalidRomanNumeralError not raised by from_roman

----------------------------------------------------------------------
Ran 10 tests in 0.058s

FAILED (failures=3)
```

Good deal. Now, all we need to do is properly add the regular expression to test for valid Roman numerals into the ``from_roman()`` function. 

```python
roman_numeral_pattern = re.compile('''
    ^                   # beginning of string
    M{0,3}              # thousands - 0 to 3 Ms
    (CM|CD|D?C{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 Cs),
                        #            or 500-800 (D, followed by 0 to 3 Cs)
    (XC|XL|L?X{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 Xs),
                        #        or 50-80 (L, followed by 0 to 3 Xs)
    (IX|IV|V?I{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 Is),
                        #        or 5-8 (V, followed by 0 to 3 Is)
    $                   # end of string
    ''', re.VERBOSE)
```

And re-run the tests...

```
..........
----------------------------------------------------------------------
Ran 10 tests in 0.066s

OK
```

And the anticlimax award of the year goes to... the word “OK”, which is printed by the ``unittest`` module when all the tests pass. 

## Part #3: Functional programming

One aspect of Python we've somewhat skimmed over thus far concerns functional programming. 

Much like object-oriented programming, FP is a programming paradigm, i.e., a programming "style" which requires you to structure your code in a certain way. If OOP can be roughly defined as "everything is just objects with attributes and method", FP can be thought of as "all the code is just functions of data". As such, FP style code tends to use specific functions such as `map` and`reduce`, tries to avoid `for`, `if`, and other syntactic words, and tries to describe the full process as a series of calls.

We'll be covering the basic blocks of FP-style code here.

### Review #3.1: `lambda` functions

In python, you can define a function using the `def` keyword:

```Python
def lower_first_char(arg_str):
    """A silly function that takes the first character, lowers it, and returns it."""
    return arg_str[0].lower()
    
lower_first_char("CHIMPS!") # returns "c"
```

On the other hand, writing a function can be undesirable at times, expecially when you're dealing with very trivial pieces of codes that don't really warrant giving potential users of your code access to them. Enter lambdas!

```Python
f = lambda s: s[0].lower()
f("CHIMPS!") # returns "c"
```

This example here is strictly equivalent to our earlier `lower_first_char` function.

A lambda (or lambda function) is a statement that produces a callable. They are identified by the syntactic word `lambda`. Anything appearing between that `lambda` and the colon `:` correspond to arguments. Anything after the colon corresponds to what a call to the lambda will return.

Lambdas have many use cases. For instance, consider the following:

```Python
>>> l = [
...     "    Space", "\tmonkey", " in  ", "the", "\t\tplace ", " to", "  be",
...     "\nLying", "\tin", "a", "\n\rrocket", "  to", "     a", " planet", "of", "sound",
... ]
>>> sorted(l)
['\t\tplace ', '\tin', '\tmonkey', '\n\rrocket', '\nLying', '     a', '    Space', '  be', '  to', ' in  ', ' planet', ' to', 'a', 'of', 'sound', 'the']
>>> sorted(l, key=lambda s: s.strip().lower())
['a', '     a', '  be', ' in  ', '\tin', '\nLying', '\tmonkey', 'of', '\t\tplace ', ' planet', '\n\rrocket', 'sound', '    Space', 'the', ' to', '  to']
```

The lambda here allows us to sort our elements "properly", instead of being misguided by the existence of whitespace around our items. On the other hand, assuming we only really need this pre-processing for sorting, it would be overkill to define a function for that.

Many python functions accept callable arguments just like `sorted`. Whenever this is the case, lambdas may prove useful!

### Review #3.2: `map`

Another use case for lambdas is the `map` function. Map takes as arguments a callable and a sequence, applies the callable to all elements of the sequence, and return the "mapped" sequence.

In general, `map` can replace `for` loops and comprehensions:
```Python
mapped = []
for item in seq:
    mapped.append(func(item))
```
is roughly equivalent to:
```Python
mapped = [func(item) for item in seq]
```
and roughly equivalent to: 
```Python
mapped = map(func, seq)
```
The main differences between map and the two others is that it produces a map object, over which you can only iterate once. If you need to iterate multiple times, consider casting the full result in a list:

```Python
mapped = list(map(func, seq))
```

The `map ` function also allows you to map multiple sequences into one. Consider for instance:
```Python
>>> monkeys = ["Koko", "Grodd", "Harambe"]
>>> peanuts = [42, 3, 5]
>>> list(map(lambda m, p: "Monkey '%s' has %i peanuts" % (m,p), monkeys, peanuts))
["Monkey 'Koko' has 42 peanuts", "Monkey 'Grodd' has 3 peanuts", "Monkey 'Harambe' has 5 peanuts"]
```

### Review #3.3: generators and the `itertools` library

This brings us to an important point: all the functional API in python is designed around **generators**. Generators are ordered sequences over which you can iterate only once. 


#### Creating generator

There are two main ways of constructing generators. The first one consists in function definitions containing the `yield` syntactic word:

```Python
def my_gen(...):
    ...
    yield something
    
g = my_gen(...) # creates the generator
```

Every time the `yield` keyword is used will correspond to another element in the generator. Therefore, to convert a list in a generator, one may write the following:

```Python
def list_to_gen(some_list):
    for elem in some_list:
        yield elem
```

The second way is to use a comprehension with parentheses (rounded brackets):
```Python
my_gen = (func(item) for item in seq if test(item))
```

#### Why generators?

The main interest of generators is that they are iterable sequences, but they have low memory footprint: once you've processed one element, that element is discared and not stored in memory. Assuming you have to deal with a very large sequence, using generators will help you avoid memory errors and the like.

Another crucial point with generators is that they're not evaluated unless explicitly required. This means that you potentially write more efficient programs, as computations that are not necessary will be ignored.

To explicitely evaluate a generator, you can either user the `next` function, or use a `for` loop:

```Python
g = some_generator(...)
elem = next(g) # will evaluate the first element in the generator 
for elem in g:
    # will evaluate all elements in the generator, one by one
```

#### `itertools`: a generator-based library for iterable sequences

The python standard library `itertools` contains many function for merging, duplicating and manipulating generators (or sequences in general). Have a look at it [here](https://docs.python.org/3/library/itertools.html): it contains many very useful functions that can save you a lot of time.

### Review #3.4: `filter`

The `filter` function allows you to drop items from a sequence based on a `test` callable.

In short, the following are roughly equivalent:
```Python
# 1. using a for-loop
filtered = []
for item in sequence:
    if test(item):
        filtered.append(item)
        
# 2. using a comprehension
filtered = [item for item in sequence if test(item)]

# 3. using filter
filtered = filter(test, sequence)
```

Much like `map`, `filter` has the added benefit that it returns a generator-based sequence. Chaining `map` and `filter` therefore does not perform any computation until their elements are evaluated.

Lastly, `filter` also accepts the `None` object instead of a `test` callable. In that case, it will drop all `falsy` items:
```Python
>>> list(filter(None, [None, "", "chimp", 0, False]))
['chimp']
```

### Review #3.5: the `functools` library and the `reduce` function.

#### `functools.reduce` 

The `reduce` function from the `functools` library allows you to transform a sequence into a single element. The example generally being given is the sum or the product:

```Python
>>> import functools
>>> nums = [1, 2, 3, 4, 5]
>>> functools.reduce(lambda acc, el: acc + el, nums)
15
>>> functools.reduce(lambda acc, el: acc * el, nums)
120
```

Note that the `reduce` function generalizes this behavior to any function that accepts an accumulator and an element, and returns an updated version of the accumulator. In the case of a summation, the intermediate result of the summation is the accumulator, and the addition suffices.

You can also supply an initial value as the accumulator:
```Python
>>> functools.reduce(lambda a,b: a + b, nums, 42)
57
```

In all, this means that `reduce` can serve in a great number of situations. Here are some examples:
```Python
>>> nums = [1, 2, 3, 4, 5]
>>> functools.reduce(lambda a,b: a + [b], nums, ['a', 'b', 'c']) # extends ['a', 'b', 'c'] with nums
['a', 'b', 'c', 1, 2, 3, 4, 5]
>>> list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
>>> functools.reduce(lambda a,b: a + b, list_of_lists) # flattens
[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> nums = [1, 2, 3, 4, 5]
>>> functools.reduce(lambda acc, el: 10*acc + el, nums, 0) # converts list of digits to integer
12345
```

While `reduce` used to be a default function available without import, it has been moved to the `functools` standard library. It remains one of the most important concepts in functionnal programming.

In functional programming languages, the analog of `reduce` is often called `fold`.


#### `functools` contents

The `functools ` library contains some other useful pieces of codes: 

- a [`singledispatch` decorator](https://docs.python.org/3/library/functools.html?highlight=functools#functools.singledispatch) for type-based polymorphism, 
- a [`cache` decorator](https://docs.python.org/3/library/functools.html?highlight=functools#functools.cache) to make functions memoizable, 
- utilities for sorting and comparisons, 
- a [`partial` function ](https://docs.python.org/3/library/functools.html?highlight=functools#functools.partial) to pre-fill some arguments (NB: you could the same with a lambda!)
 

### Review #3.6: Function composition for even more FP goodness!

One of the hallmarks of functionnal programming is to treatfunctions as if they were variables. In particular, we expect of a FP-style language that it is able to compose functions. 

Function composition works as follows: Assuming we have two functions $f$ and $g$, then the composed function $h = f \circ g$ is defined as $h(x) = f(g(x))$.

This is less easy to do in Python, but not quite impossible. In any event, there's no standard way of doing it. One possible way is to define a function ourselves:

```Python
def compose(f, g):
    def h(*args, **kwargs):
        return f(g(*args, **kwargs))
    return h
```    
Note that this assumes that the sole argument of `f` corresponds to the return value of `g`. In general, function compostion without type checking can lead to trouble. Also, be careful with the execution order of the composed functions!

Do note however that composition will give us even more flexibility when coupled with `filter`, `map` and `reduce`. Consider the following: 
```Python
>>> def compose(f, g):
...     def h(*args, **kwargs):
...             return f(g(*args, **kwargs))
...     return h
... 
>>> def lower_case(s):
...     return s.lower()
... 
>>> def double_str(s):
...     return s * 2
... 
>>> def every_other_chr(s):
...     return s[::2]
... 
>>> process = functools.reduce(compose, [lower_case, double_str, every_other_chr])
>>> process("CHIMPS FOREVER!")
'cip oee!cip oee!'
```


## Part #4: Standard and Third-party libraries

In this last part of the lab, we'll be discussing how to install third party libraries, and give you pointers to some librarires that will be useful .

### Review #4.1: `pip` and `venv`: keep track of your python environment

#### Package Installer for Python

The first thing you need to make sure is that you're able to download and install third party librarires. Python normally comes shipped in with [`pip`, the package installer for Python](https://pypi.org/project/pip/). Do note that `conda` (`anaconda`, `miniconda`) also provides a similar utility, which might be more convenient for you, depending on your install and your preferences.

You may already have had to install jupyter or the like using the following command:
```
pip install jupyter-lab
```
Here, `jupyter-lab` corresponds to the package name you're trying to install. The same command can work for any package, e.g., supposing you're trying to install numpy:
```
pip install numpy
```

After running these commands, you should be able to import the libraries you want.

You can find a summary of all third party libraries you have install using the command `pip freeze`

You can install multipe libraries at once as well. Either name all libraries in the call itself:
```
pip install numpy scipy sklearn scikit-learn
```
Or create a **requirements file**, where each line corresponds to a library (potentially with its version number). Assuming you have such a file, you can install all required libraries as listed in the file by running:
```
pip install -r requirements.txt
```
Note that the output of `pip freeze` corresponds exactly to the file format expected by `pip install -r`. It's therefore fairly customary on NIX systems to run something like:
```
pip freeze > requirements.txt
```
so that you can share your requirements file along with your code for anyone trying to reproduce your code (*like, I dunno, the tutors that will review your code for a KNN-based monkey classification system, for instance...*)


#### Virtual environment

One issue that comes up very often is that you have a script which requires version X of the library, whereas another of your script was written with version Y of that same library.

To avoid **version conflicts**, it is generally recommended to set up a virtual environment. Python comes shipped in with the `venv` module for doing just that: see [here](https://docs.python.org/3/library/venv.html).

1. Set up a virtual environment called `my-venv`: ```python3 -m venv my-venv```
2. Activate it, on NIX: ```source my-venv/bin/activate```, on windows: ```my-venv\Scripts\activate.bat```
3. Install whatever you need, do your work on your code
4. Once you're done working, close the environment using the `deactivate` command. 

Following these steps will minimize the number of version conflicts you encounter, by making sure that your installations are compartimented on a per-project basis. 
Also, you should try to come up with a better name than the example `my-env` given here.

### Review #4.2: `argparse`: handling command-line interfaces

The [`argparse` library](https://docs.python.org/3/library/argparse.html) is part of the standard libraries in python (so no need to install it!).

This library allows you to quickly create command-line interfaces, i.e., make sure that your python script can receive arguments from the terminal, has a custom help message for those trying to run it, etc. In short, it provides a simple entry point for end-users to interact with.

The main class you'll interact with is the [`ArgumentParser`](https://docs.python.org/3/library/argparse.html#argumentparser-objects) class. These objects have three methods that you should pay close attention to:

1. [`add_argument()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument), which allows you to describe what argument your script expects, and how they should be handled
1. [`add_subparser()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers), which allows you to define subcommands for your program
1. [`parse_args()`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args), which does the job of actually converting command-line arguments into a Python object


Read the documentation carefully (it's rather clear, for once), at least for these three functions. Keep in mind that you will need this library to handle Exercise #4.

### Review #4.3: `numpy`: python for scientific numeric computations

`numpy`is a third party library for numeric computation. Generally speaking, it is more efficient thanpython, which might have some impact if you perform intensive computations.

`numpy` is a very large library, containing quite a lot of material. The main class you should be aware of, to start with, is the [array](https://numpy.org/doc/stable/reference/generated/numpy.array.html) class, which is more or less the basic object manipulated by most of the `numpy` code you'll encounter. It overloads operators for a number of operations, for instance, vector addition or element-wise vector multiplication, as well as other useful basic methods such as the dot product.
```Python
>>> import numpy as np
>>> a = np.array([1, 2, 3, 4])
>>> b = np.array([1, 2, 3, 4])
>>> a + b # element-wise addition
array([2, 4, 6, 8])
>>> a * b # element-wise multiplication
array([ 1,  4,  9, 16])
>>> a @ b # dot product
30
```

Arrays also support slicing along the different **axes** ("dimensions"):

```Python
>>> c = np.array([[1, 2],[3, 4]])
>>> c
array([[1, 2],
       [3, 4]])
>>> c[0,:] # select the 0th row
array([1, 2])
>>> c[:,0] # select the 0th column
array([1, 3])
```

Numpy also contains a number of useful runctions to merge arrays or reshape them:
```Python
>>> d = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> d.reshape(3, 3)
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])
>>> a = a.reshape(1, -1)
>>> a
array([[1, 2, 3, 4]])
>>> b = b.reshape(2, -1)
>>> b
array([[1, 2],
       [3, 4]])
>>> np.concatenate([b, c], axis=1)
array([[1, 2, 1, 2],
       [3, 4, 3, 4]])
>>> e = np.concatenate([b, c], axis=1)
>>> e
array([[1, 2, 1, 2],
       [3, 4, 3, 4]])
>>> f = np.concatenate([a, e], axis=0)
>>> f
array([[1, 2, 3, 4],
       [1, 2, 1, 2],
       [3, 4, 3, 4]])
>>> f.T # matrix transpose
array([[1, 1, 3],
       [2, 2, 4],
       [3, 1, 3],
       [4, 2, 4]])
```

`numpy` is, in a word, vast. Exploring its capabilities requires time, but is very rewarding: it generally contains all the functions you need to handle about everything. `numpy` is also omnipresent in the Python community: virtually every major scientific 3rd party library uses it, directly or indirectly.

Often associated with numpy is `scipy`, which content is more "scientific-oriented". It contains a number of rather specific algorithms for classification, distance computing, etc. 

### Review #4.4: `matplotlib`: visualization


`matplotlib` is a visualization library (i.e., that produces graphics and figures from data), built upon `numpy` objects (we told you numpy was a big deal in Python). The documentation is rather thorough, and it contains a great many examples for you to learn from. In the interest of this monkey KNN project, have a look at [this link](https://matplotlib.org/gallery/lines_bars_and_markers/scatter_with_legend.html#sphx-glr-gallery-lines-bars-and-markers-scatter-with-legend-py), for instance.

### Review #4.5: `pandas`: data handling

`pandas` is a data handling library that is built upon numpy (again!), mostly in the spirit of functional programming. It is mostly intended for handling CSV-like data (CSV, Excell files, TSV...). 

The most common entry-point for usersis to call a function such as [`read_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html), which should yield a [`DataFrame` object](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html?highlight=dataframe#pandas.DataFrame). This `DataFrame`can be queried through its rows or through its columns, and is designed to be rather straightforward in its use.

Consider having a look at the tutorials [here](https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/index.html). 

## Submitting your lab

All done? Good job!

Submit your lab through Arche.

#### Credits

Credits to Pierre Monnin for Part #2 on TDD & unittest.

The rest from tmickus. Inspired from old exercises that have been passed on from tutors to tutors at Univ Paris.  
