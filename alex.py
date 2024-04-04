import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys


def question1(fileName):

    occupations = ['Total, all occupations', 'Management occupations [0]',
                   'Business, finance and administration occupations [1]',
                   'Natural and applied sciences and related occupations [2]',
                   'Health occupations [3]', 'Occupations in education, law and social, community and government services [4]',
                   'Occupations in art, culture, recreation and sport [5]', 'Sales and service occupations [6]',
                   'Trades, transport and equipment operators and related occupations [7]',
                   'Natural resources, agriculture and related production occupations [8]',
                   'Occupations in manufacturing and utilities [9]',
                   'Unclassified occupations',
                   ]

    print("")

    try:
        lowerYear = int(input("Enter lower year: "))
        upperYear = int(input("Enter upper year: "))

        print("Options: ")
        for i, job in enumerate(occupations):
            print(f"{i+1}: {job}")

        occupationSelection = int(input("Enter an integer 1-12: "))
    except ValueError:
        print("One or more input values are invalid. Proper input: python3 graphingstuff.py year1(int) year2(int) occupation(int)", file=sys.stderr)
        sys.exit(1)

    if occupationSelection < 1 or occupationSelection > 12:
        print(f"{occupationSelection} is an invalid selection for 'occupation.' Value must be from 1-6", file=sys.stderr)
        sys.exit(1)

    occupation = occupations[occupationSelection-1]

    try:
        totalFile = open(fileName, "r", encoding="utf-8-sig")
    except IOError:
        print("Unable to open file", file=sys.stderr)
        sys.exit(1)

    totalCSVReader = csv.reader(totalFile)

    vacanciesData = []
    workExperienceData = []

    experienceOrder = ["Minimum experience level sought, all levels", "Less than 1 year", "1 year to less than 3 years",
                       "3 years to less than 5 years", "5 years to less than 8 years", "8 years or more"]

    for line in totalCSVReader:
        if line[4] in experienceOrder:
            if line[1] == "Canada" and line[5] == "Job vacancies" and int(line[0][0:4]) >= lowerYear and int(line[0][0:4]) <= upperYear and line[3] == occupation:
                vacanciesData.append(line)
            elif line[1] == "Canada" and line[5] == "Average offered hourly wage" and int(line[0][0:4]) >= lowerYear and int(line[0][0:4]) <= upperYear and line[3] == occupation:
                workExperienceData.append(line)

    with open("wageBifFile.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(workExperienceData)

    # Create new names for headers
    newDataHeaders = ["Date", "Occupation Type",
                      "Vacancy Status", "Vacancies", "Wage"]

    # Initialize array for new data
    newData = []

    # Iterate through both csv files and look for given fields
    for vacancyLine, experienceLine in zip(vacanciesData, workExperienceData):
        if vacancyLine[3] == f"{occupation}" and experienceLine[3] == f"{occupation}":
            if int(vacancyLine[0][0:4]) >= lowerYear and int(vacancyLine[0][0:4]) <= upperYear and int(experienceLine[0][0:4]) >= lowerYear and int(experienceLine[0][0:4]) <= upperYear:
                newData.append([vacancyLine[0]] + vacancyLine[3:5] +
                               [vacancyLine[12]] + [experienceLine[12]])

    # Print comma separated lines
    outputFile = open("output.csv", "w")

    csvWriter = csv.writer(outputFile)
    csvWriter.writerows(newData)

    # Condense group names for x-axis scaling
    condensedExperiences = ["All", "<1", "1-3", "3-5", "5-8", "8<"]

    df = pd.DataFrame(newData, columns=newDataHeaders)

    df['Wage'] = pd.to_numeric(df['Wage'], errors='coerce')
    df['Vacancies'] = pd.to_numeric(df['Vacancies'], errors='coerce')

    df['Vacancy Status'] = pd.Categorical(
        df['Vacancy Status'], categories=experienceOrder, ordered=True)

    # Create dataframe that takes the averages of the given years
    averageWages = df.groupby('Vacancy Status', observed=True)['Wage'].mean()
    averageVacancies = df.groupby('Vacancy Status', observed=True)[
        'Vacancies'].mean()

    fix, axs = plt.subplots(2, 1, figsize=(10, 10))

    # Plot wage data
    axs[0].bar(averageWages.index, averageWages.values, color='blue')
    axs[0].set_xticks(range(len(averageWages)), condensedExperiences)
    axs[0].set_title(
        f'Average Wages for {occupation} from {lowerYear} - {upperYear}')
    axs[0].set_xlabel('Experience Level (years)')
    axs[0].set_ylabel('Average Wage')

    # Plot vacancy data
    axs[1].bar(averageVacancies.index, averageVacancies.values, color='red')
    axs[1].set_xticks(range(len(averageVacancies)), condensedExperiences)
    axs[1].set_title(
        f'Average Vacancies for {occupation} from {lowerYear} - {upperYear}')
    axs[1].set_xlabel('Experience Level (years)')
    axs[1].set_ylabel('Average Vacancies')

    plt.tight_layout()

    plt.savefig('laborData.pdf', format='pdf')

    # Close files
    outputFile.close()

    totalFile.close()
