"""
Given a list of patient demographics for several patients, 
this code groups the data by patients with the same name. 
The demographics provided are (in order): 
Patient ID, Patient Name, Patient Sex, Patient Date Of Birth.

Input example:
PID1,POND^AMY,F,19890224
PID2,WILLIAMS^RORY,M,19881102
PID3,POND^AMY,F,19890224
PID4,POND^AMY,F,20010911

Output:
0:
PID1,POND^AMY,F,19890224
PID3,POND^AMY,F,19890224
PID4,POND^AMY,F,20010911
1:
PID2,WILLIAMS^RORY,M,19881102

This tool accepts comma separated value files (.csv) only.
and requires python's csv library.

This file can also be imported as a module and contains the following
functions:

    * readInputFile - returns the data of the file as an array where each element is a row
    * main - the main function of the script

"""

import csv
import argparse


def readInputFile(inputFilename):
    """Reads a CSV file into a list

    Args:
        inputFilename (object): The csv file location

    Returns:
        list: Each csv row is now a list element
    """
    with open(inputFilename, 'r') as inputFile:
        dataReader = csv.reader(inputFile)
        data = list(dataReader)
    return data


def createKey(completeName):
    """
    Based on the string with structure LAST NAME^FIRST NAME^MIDDLE NAME,
    create a lowercase string with structure last name^first name,
    without the middle name

    Args:
        completeName (string): A string with structure LAST NAME^FIRST NAME^MIDDLE NAME

    Raises:
        Exception: If the string does not have the structure described

    Returns:
        string: Lowercase last name^first name
    """
    completeName = completeName.lower()
    name = completeName.split("^")
    nameLength = len(name)
    if nameLength == 2:
        return completeName
    elif nameLength == 3:
        return name[0] + "^" + name[1]
    else:
        raise Exception("Name is not in a proper structure")


def createDictionary(data):
    """
    Creates and returns a dictionary whose keys are 'last name^first name'
    obtained from the csv name entries and whose values are the (whole) entries that match
    the last name and first name of that key. 
    This is, it is a dictionary that groups entries that have the same last and first name.

    Args:
        data (list): The list structure of the data extracted from the csv file

    Returns:
        object: The dictionary 
    """
    namesDictionary = {}
    for item in data:
        currentKey = createKey(item[1])
        namesDictionary.setdefault(currentKey, [])
        namesDictionary[currentKey].append(item)
    return namesDictionary


def printOutput(namesDictionary):
    """
    Print to standard output in the following structure:
    Output:
    0:
    PID1,POND^AMY,F,19890224
    PID3,POND^AMY,F,19890224
    PID4,POND^AMY,F,20010911
    1:
    PID2,WILLIAMS^RORY,M,19881102

    Args:
        namesDictionary (object): The dictionary with keys that group the names with the 
        same last and first name
    """
    counter = 0
    for key, value in namesDictionary.items():  # pylint: disable=unused-variable
        print('{0}:'.format(counter))
        counter += 1
        for item in value:
            print(','.join(map(str, item)))


def extractNumber(str):
    """Extract the number from the string of the form PID###

    Args:
        str (string): A string of the form PID###

    Returns:
        integer: The number substring converted to integer
    """
    return int(str[3:])


def sortDictbyPidDesc(dict):
    """Sort the dictionary by the PID, descending

    Args:
        dict (object): The dictionary

    Returns:
        object: The sorted dictionary
    """
    for v in dict.values():
        v.sort(key=lambda arr: extractNumber(arr[0]), reverse=True)
    return dict


def main():
    # function calling
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'input_file',
        type=str,
        help="The csv file to read"
    )
    args = parser.parse_args()
    data = readInputFile(args.input_file)
    namesDictionary = createDictionary(data)
    printOutput(namesDictionary)
    print("Different version, sorted by PID number")
    sortedDictionary = sortDictbyPidDesc(namesDictionary)
    printOutput(sortedDictionary)


# main function calling
if __name__ == "__main__":
    main()
