#!/usr/bin/env python3
import sys
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict


def question2(fileName):
    print(
        "You will have to select an occupation to proceed the question with\n")
    print(
        "\t1)Total, all occupations\n\t2)Management occupations\n\t3)Business, finance and administration occupations\n\t4)Natural and applied sciences and related occupations\n\t5)Health occupations\n\t6)Occupations in education, law and social, community and government services\n\t7)Occupations in art, culture, recreation and sport\n\t8)Sales and service occupations\n\t9)Trades, transport and equipment operators and related occupations\n\t10)Natural resources, agriculture and related production occupations\n\t11)Occupations in manufacturing and utilities\n\t12)Unclassified occupations"
    )
    occupation_dict = {
        1: "Total, all occupations",
        2: "Management occupations",
        3: "Business, finance and administration occupations",
        4: "Natural and applied sciences and related occupations",
        5: "Health occupations",
        6:
        "Occupations in education, law and social, community and government services",
        7: "Occupations in art, culture, recreation and sport",
        8: "Sales and service occupations",
        9: "Trades, transport and equipment operators and related occupations",
        10:
        "Natural resources, agriculture and related production occupations",
        11: "Occupations in manufacturing and utilities",
        12: "Unclassified occupations"
    }
    while True:
        try:
            occupation_number = int(
                input(
                    "\nPlease enter the number corresponding to the occupation: "
                ))
            if occupation_number in occupation_dict:
                occupation = occupation_dict[occupation_number]
                break  # Exit loop if a valid occupation number is entered
            else:
                print("Invalid input. Please enter a number between 1 and 12.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    # files we will be using
    graphicsfile = "plot.pdf"  # Graphics file name
    outputFile = "filtered_data.csv"  # Output file name

    # Open file

    try:
        openFile = open(fileName, "r", encoding="utf=8-sig")
    except IOError:
        print(f"Unable to open file: {fileName}", file=sys.stderr)
        sys.exit(1)

        # Print headers
    fileReader = csv.reader(openFile)
    firstLine = next(fileReader)

    headers = ["Reference Date",
               "Job Vacancy Characteristics", "Vacancies"]

    filteredCsv = []

    years = ["2020", "2021", "2022", "2023"]

    # Iterate through CSV
    for line in fileReader:
        # Check if the line has enough elements
        if line[5] == "Job vacancies" and line[0][:4] in years:
            if len(line) >= 6:

                feild = line[3].split(' [')[
                    0]  # spliting the string as it sees a [ to get the occupation
                if feild == occupation:
                    if line[4] in [
                            "Company website", "Online job boards", "Social media"
                    ]:
                        line = line[0:1] + [line[4]] + [line[-5]]
                        # Check to see if line has a value
                        if not line[-1]:
                            line[-1] = "0"
                        filteredCsv.append(line)

        # Close the file
    openFile.close()

    # Write filtered data to new CSV file
    with open(outputFile, "w", newline="", encoding="utf-8") as openFile:
        writer = csv.writer(openFile)
        writer.writerow(headers)
        writer.writerows(filteredCsv)

    # Create plot using new CSV file
    plot_data = pd.read_csv(outputFile)
    fig = plt.figure()

    sns.lineplot(x="Reference Date",
                 y="Vacancies",
                 hue="Job Vacancy Characteristics",
                 data=plot_data)
    # Now we can save the matplotlib figure that seaborn has drawn
    # for us to a file
    # writing the title of the graphic on top and saving it
    title = "Distribution of Online Recruiting Strategies for Job Vacancies in " + occupation + "."
    plt.title(title, pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    fig.savefig(graphicsfile, bbox_inches="tight")
