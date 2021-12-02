#!/usr/bin/python

"""
General Functions for Advent of Code
====================================

Use the functions here by importing this script

import advent_of_code as aoc

"""

INPUT_PATH = "./input/"
INPUT_TEMPLATE = "day{num}.txt"

def input_readlines(num):
    ''' Function to
        num is an int or string of an int
        Examples: num = 3, num = '3'
    '''

    file_name = f'{INPUT_PATH}/{INPUT_TEMPLATE.format(num=num)}'
    with open(file_name,'r') as f:
        lines = f.readlines()

    return lines
    
