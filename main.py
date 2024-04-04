#!/usr/bin/env python3
import sys
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from alex import question1
from josephine import question3
from mobeen import question4
from nayyab import question2


def main(argv):
    fileName = argv[1]

    choice = 1

    while choice != -1:

        print("\nMENU:")
        print(
            "\t1:  How does job experience affect the average wage and vacancies for various professions in Canada?\n"
        )
        print(
            "\t2:  How have online recruiting strategies such as company websites, online job boards, and social media influenced job vacancies in different industries since 2020?\n"
        )

        print(
            "\t3:  How do different the Job types  affect the number of job vacancies available?\n"
        )
        print(
            "\t4:  How has the average workweek length varied across different industries in Canada from 2015 to 2022?\n"
        )
        print("\t-1; ``Exit the program\n")

        choice = input("Enter the question number you would like to search: ")

        if choice == "1":
            print("You have selected question 1")
            question1(fileName)

        elif choice == "2":
            print("You have selected question 2")
            question2(fileName)

        elif choice == "3":
            print("You have selected question 3")
            question3(fileName)
        elif choice == "4":
            print("You have selected question 4")
            question4("mobeenData.csv")

        elif choice == "-1":
            print("You have selected to exit the program")
        else:
            print("Invalid input! Please enter either 1, 2, 3, 4 or -1 ")


main(sys.argv)
