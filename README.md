# lgl_interpreter.py

This Python script demonstrates a simple functional programming ("little german languange") language. It includes various operations, such as creating arrays, working with classes, and performing mathematical calculations. The script reads a program from a JSON file and executes it. THe function names are in German, so the abbreviation lgl(little german language) makes sense. 

## Operations

- **do_kreieren_array**: Creates an array with empty lots, of a fixed size--> ["kreieren_array", 10] creates an array with 10 empty slots. The word array also exists in german, so the lgl abbreviation still holds. The size of the function is executed first through the do function, to make sure it's an integer (floats are also not allowed).
- **do_array_standort**: Retrieves the value at a specified location in an array. It doesn't change the value of the array location, it just returns it for user to see. exp: ["array_standort", ["abrufen", "array1"], 0] returns the first argument in the array. The counting starts at 0 like in python. The location parameter has to be in the range of 0 and the length of the array-1, to make sure it's in the array, otherwise it raises an error.
- **do_setzen_array_wert**: Sets the value at a specified location in an array. 
["set_array_value", ["create_array", 3], 0, 24] == [24, '', '']--> As in do_array-standort the location given is also int within the range of 0 and len(array)-1.
- **do_klasse**: Defines a class. The entire class is a dictionary, to facilitate the storing and retrieving of new methods. The methods and functions inside of the class are also dictionaries. They are the stored in an environment for later use.
- **do_abfolge**: Executes a sequence of operations. This function is absolutely necessary if we want to have a sequence of functions. Just calling it at the start is enough for the rest of the code to be executed properly. The only requirement for this code to work is that there is at least one operation. ["addieren", ["addieren" 1, 1], ["addieren", 1, 1]] counts as one function, so the do_abfolge isn't necessary but can still be utilized nonetheless. the different functions must be separated using commas.
- **do_drucken**: Prints a statement. For this function to work as intended we decided that it shouldn't return the argument itself but it should just print it. The function itself returns --> "", this was a conscious decision to make sure that the function doesn't return None or the statement again, as this would print the argument twice. Especially when we applied it in the while loops, it would not work as intended if the function actually returned the argument.
- **do_addieren**: Adds two numbers. The function raises an Assertionerror if there aren't exactly 2 arguments. This function was pretty much left intact from the book. The function rounds to 2 decimal places, with the intent of making sure that example_class.gsc would give us the exact same output as intended in the assignment.
- **do_absolutwert**: Computes the absolute value of a number. This function was pretty much left intact from the book.
- **do_subtrahieren**: Subtracts one number from another. The function raises an Assertionerror if there aren't exactly 2 arguments. This function was pretty much left intact from the book. The function rounds to 2 decimal places, with the intent of making sure that example_class.gsc would give us the exact same output as intended in the assignment.
- **do_multiplizieren**: Multiplies two numbers. This function was implemented with the same logic in mind as the other mathematic-functions before. The function rounds to 2 decimal places, with the intent of making sure that example_class.gsc would give us the exact same output as intended in the assignment.
- **do_potenzieren**: Raises one number to the power of another. This function was implemented with the same logic in mind as the other arithmetic functions before. The user can define to which power of it should operate the argument. ["potenzieren", 2, 1] returns 2 while ["potenzieren", 2, 2] return 4. The function raises an Assertionerror if there aren't exactly 2 arguments. The function rounds to 2 decimal places, with the intent of making sure that example_class.gsc would give us the exact same output as intended in the assignment.
- **do_dividieren**: Divides one number by another. The function raises an Assertionerror if there aren't exactly 2 arguments. The function rounds to 2 decimal places, with the intent of making sure that example_class.gsc would give us the exact same output as intended in the assignment.
- **do_funktion**: Defines a function.
- **do_waehrend**: Executes a block of code while a condition is met. ["<", ">", "<=", ">="] it utilizes these four operators. The user has to set the beginning value of the counter one of the four operators and the limit the counter should stop the execution at.
- **do_wortb**: Creates a dictionary. The dictionary has to have an even length. To get the value of the key we would just have to increase the index by 1. The purpose of this is to have an array where all the even positions are the keys and all the odd positions are the values. ["wortb", "a", 1] would return {a:1}.
- **do_wortb_wert**: Retrieves the value from a dictionary. The first argument passed on is the dictionary itself and the second is the key. If the key is not in the dictionary, it raises a KeyError. 
- **do_wortb_setzen**: Sets the value in a dictionary. The first argument is the dictionary, the second the key and the third the new value the key should take on. The former value of the key is then replaced.
- **do_wortb_zusammenfuehren**: Merges two dictionaries. The arguments consists of two arguments and the "|" operator in python. We didn't really know to what degree we had to implement this operator, so we made sure that it had to be included after the two dictionaries. Should the first and second dictionaries share keys with different values, then the function automatically takes the values of the second dictionary. Should one of the dictionaries be longer than its keys and values are also implemented in the new longer dictionary that would be returned as the output. To make this work as described we copied the first dictionary with the .copy function of python and updated the copy with right dictionary.
- **log_event**: Logs events during function calls (with tracing option).
- **with_logging**: Decorator for logging function calls.
- **do_aufrufen**: Calls a function or method.
- **run_method**: Runs a method within a class.
- **do_setzen**: Sets a variable in the environment. It then saves it in an environment, and stores it in envs with all the other environments. Should the variable already exist with another value then the former value is replaced with the latest. It also checks if the thing we want to save is a dictionary because it would make the storing process easier, as the envs_set function isn't required.
- **do_abrufen**: Retrieves the value of a variable, using the envs_get function. It can only retrieve one variable at a time.


## Helper functions

 **find_method**

This function searches for a method in a given class and its parent classes. It takes three parameters. It will look for the parent iterates through the parent of the classes until it finds the desired method. Should none of the parents contain the method in their class it raises a NotImplementederror. It takes three parameters:

    envs: A list of environments.
    cls: The class or class name to search for the method.
    method_name: The name of the method to find.
To make sure we get the actual class as a dictionary we utilize the env_get() function, to make sure we don't just only get a string back.

**call_method**

This function calls a method on an object. It internally uses find_method to locate the method and then executes it. It takes four parameters:

    envs: A list of environments.
    obj: The object on which the method is called.
    method_name: The name of the method to call.
    args: A list of arguments to pass to the method.

**create_object**

This function creates an object based on a class definition. It initializes the object by calling its _init method if defined. It takes three parameters:

    envs: A list of environments.
    cls: The class or class name for the object.
    args: A list of arguments to pass to the object's _init method.

**envs_get**

This function retrieves the value of a variable by name from the list of environments. It takes two parameters:

    envs: A list of environments.
    name: The name of the variable to retrieve.

**envs_set**

This function sets the value of a variable in the current environment. It takes three parameters:

    envs: A list of environments.
    name: The name of the variable to set.
    value: The value to assign to the variable.

**OPERATIONS**
It is not a function but a dictionary, that contains all globals().items() that start with "do_". So in our case all the Operators. the key is the function name without the "do_" at the beginning and the value is the function itself.

**do**

This function is the main interpreter for the scripting language. It evaluates expressions and performs the corresponding operations. It takes two parameters:

    envs: A list of environments.
    expr: The expression to evaluate.
It searches for the desired function is in the OPERATIONS dictionary and after finding it, it executes it. Should the function name not be in the OPERATIONS dictionary, an error will be raised.
**main**

This is the main entry point of the script. It reads a program from a file, interprets it using the do function, and prints the result. If tracing is enabled, it outputs a trace log.

## Usage

```bash
python lgl_interpreter.py filename.gsc [--trace trace-output.log]
```

- `filename.gsc`: The JSON file containing the program to execute.
- `--trace trace-output.log`: (Optional) Enables tracing and specifies the output file for the trace log.

## Trace Log

If the `--trace` option is used, the script generates a trace log containing information about function calls. The log includes columns for call ID, function name, event (start/stop), and timestamp.













## reporting.py


**Create Function**


The create function within the Reporting Tool script processes a trace log file and generates a statistical report on function calls. Below is an overview of how the create function works:
Function Overview

The create function performs the following tasks:

    Open Trace Log File: Reads the specified CSV-formatted trace log file (file_path) to extract information about function calls.

    Aggregate Function Statistics:
        Iterates through each row in the trace log.
        Retrieves the function name and timestamp from each log entry.
        Maintains a dictionary (function_stats) to aggregate statistics for each unique function.
        Tracks the number of calls (Num. of calls), start times, and total time spent in each function.

    Calculate Total and Average Time:
        Calculate the elapsed time for each function by subtracting the start time from the stop time.
        Aggregates the total time spent in each function.

    Generate Result Table:
        Constructs a result table containing columns for "Function Name," "Num. of calls," "Total Time (ms)," and "Average Time (ms)."
        Populates the table with data based on the aggregated function statistics. For this step, we imported the tabulate library which made the construction of the table more manageable.
        To install the tabulate library, one can use the following command in your terminal or command prompt:
```bash
pip install tabulate
```
For this to work Python and pip must be(Python package installer) installed on the system. Once the installation is complete, one can use the tabulate library in the Python scripts. 

    Print Result Table:
        Utilizes the tabulate library to format the result table in GitHub-flavored markdown.
        Returns the formatted table as a string.

Usage

To use the create function, run the Reporting Tool script with the following command:

```bash
python reporting.py trace_file.log
```
    Replace trace_file.log with the path to your CSV-formatted trace log file.















## example_class.gsc

**description of the gsc file**
This file shows the capacity of our compiler. By using the formerly mentioned do_functions it is able to instantiate classes with its own methods. The classes can inherit from other classes by using the find_method function.

**CLASSES AND METHODS**
**Shape Class**

    Constructor: shape_new(name, weight): Creates a new instance of the Shape class with a specified name and weight.
    Properties:
        name: Name of the shape.
        side: Weight of the shape.
    Method:
        density(thing, weight): Calculates the density of the shape based on a thing and weight.

**Square Class (Inherits from Shape)**

    Constructor: square_new(name, side): Creates a new instance of the Square class with a specified name and side length.
    Method:
        area(thing): Calculates the area of the square based on a thing.

**Circle Class (Inherits from Shape)**

    Constructor: circle_new(name, radius): Creates a new instance of the Circle class with a specified name and radius.
    Method:
        area(thing): Calculates the area of the circle based on a thing.

The provided example program creates instances of Square and Circle, sets their properties, and calculates the density of each shape. Finally, it adds the density values of the square and circle and as expected in the assignment description it returns 0.96.



















**example_operations.gsc**

This script demonstrates the usage of a simple programming language that supports various operations, including arithmetic, array manipulation, and dictionary operations. The script includes examples of setting variables, performing mathematical operations, working with arrays and dictionaries, and printing the results. All the functions of the first part of the assignment are demonstrated here.

**Makes this sequence of operations possible**
[
    "abfolge",
]

**OPERATIONS AND EXPRESSIONS**
**ARITHMETIC OPERATIONS**

**Addition:**

["addieren", 5, 5]

**Subtraction:**

["subtrahieren", ["abrufen", "alpha"], 1]

**Multiplication:**

["multiplizieren", ["abrufen", "alpha"], ["abrufen", "beta"]]

**Division:**

["dividieren", ["abrufen", "result1"], 5]

**Exponentiation:**

["potenzieren", ["abrufen", "divisionresult"], 2]

**ARRAY OPERATIONS**

**Array Creation:**

["kreieren_array", 10]

**Setting Array Values:**

["setzen_array_wert", ["abrufen", "array1"], 0, "alpha"]

**Accessing Array Values:**

["array_standort", ["abrufen", "array1"], 0]

**LOOPING**

**While Loop:**

this function prints all the elements of the array1 one by one, utilizing the while loop.

["waehrend", 0, "<", 10, ["drucken", ["array_standort", ["abrufen", "array1"], ["setzen", "counter", ["addieren", ["abrufen", "counter"], 1]]]]]

**DICTIONARY OPERATIONS**

**Creating a Dictionary:**

["wortb", "a", 1, "b", 2, "c", 3]

**Accessing Dictionary Values:**

["wortb_wert", ["abrufen", "dict1"], "a"]

**Setting Dictionary Values:**

["wortb_wert_setzen", ["abrufen", "dict1"], "a", 10]

**Merging Dictionaries:**

["wortb_zusammenfuehren", ["abrufen", "dict1"], ["abrufen", "dict2"], "|"]

**Program Execution**

The provided example program sets variables (alpha, beta, result1, divisionresult, potenzresult, array1, counter, dict1, dict2) and performs various operations on them. The script also includes a while loop and demonstrates array and dictionary manipulations.







**example_trace.gsc**
This file was left intact, with the exception of the names of the function. They would be translated into the names of the functions that we defined, so the code could work properly.
