#!/usr/bin/env python3
import sys
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict


def question4(fileName):
    # print to user they selected question 4
    print("You have selected question 4")

    # Prompt user for the CSV file path
    filePath = fileName

    # Full list of industries
    industries = [
        'Accommodation and food services [72]',
        'Administrative and support, waste management and remediation services [56]',
        'Arts, entertainment and recreation [71]', 'Construction [23]',
        'Educational services [61,611]', 'Finance and insurance [52]',
        'Forestry, logging and support [11N]',
        'Goods producing industries [11-33N]',
        'Health care and social assistance [62]',
        'Industrial aggregate excluding unclassified businesses [11-91N]',
        'Information and cultural industries [51]', 'Manufacturing [31-33]',
        'Mining, quarrying, and oil and gas extraction [21]',
        'Other services (except public administration) [81]',
        'Professional, scientific and technical services [54,541]',
        'Public administration [91]',
        'Real estate and rental and leasing [53]',
        'Service producing industries [41-91N]', 'Trade [41-45N]',
        'Transportation and warehousing [48-49]', 'Utilities [22,221]'
    ]

    # Display industry options to the user
    print("Please select an industry by its corresponding number:")
    for index, industry in enumerate(industries):
        print(f"{index + 1}. {industry}")

    # Get user's industry choice
    industry_choice = int(input("Enter your choice: ")) - 1
    industry_target = industries[industry_choice].split(' [')[
        0]  # Extract the industry name without the code

    # Get user's start and end year choices
    start_year = int(input("Enter the start year: "))
    end_year = int(input("Enter the end year: "))

    # Use defaultdict to handle cumulative totals and counts for each year efficiently
    workweek_data = defaultdict(lambda: {'total': 0, 'count': 0})
    with open(filePath, 'r', encoding='utf-8-sig') as csvfile:
        # Utilize the DictReader to map the information read into a dictionary
        # where each row is read as a dictionary
        reader = csv.DictReader(csvfile)

        # Process each row in the CSV file
        for row in reader:
            # Extract the industry category from the current row
            industry = row[
                'North American Industry Classification System (NAICS)']
            # If the industry from the row starts with the target industry name,
            # it means it matches or is a subcategory of the desired industry
            if industry.startswith(industry_target):
                # Extract the year from the 'REF_DATE' field and convert to an integer.
                year = int(row['REF_DATE'][:4])
                # If the year is within the specified range, process the data
                if start_year <= year <= end_year:
                    # Ensure that the 'VALUE' field, representing workweek length - is not empty
                    value = row['VALUE']
                    if value:
                        # Convert the value to a float
                        # for the respective year, also incrementing the count
                        workweek_length = float(value)
                        workweek_data[year]['total'] += workweek_length
                        workweek_data[year]['count'] += 1

    # Prepare a list of years within the specified range
    years = list(range(start_year, end_year + 1))
    # Initialize a list to keep track of the average workweek lengths
    average_lengths = []

    # Print the header for the output data
    print("Industry,Year(Start-End),Average workweek length")
    # Calculate and print the average workweek length for each year
    for year in years:
        if workweek_data[year]['count'] > 0:
            # Calculate the average by dividing the total by the count of entries
            average = workweek_data[year]['total'] / workweek_data[year][
                'count']
            average_lengths.append(average)
            # Output the average workweek length for the year
            print(f"{industry_target},{year},{average:.1f}")
        else:
            # If there's no data for the year, we append 0 and print '0' for the average
            average_lengths.append(0)
            print(f"{industry_target},{year},0")

    # Set up a plot with a specific size
    plt.figure(figsize=(50, 25))
    # Plot the average workweek lengths as a line plot with markers
    plt.plot(years, average_lengths, marker='o')
    # Set the title of the plot including the target industry
    plt.title(f'Average Workweek Length for {industry_target} Industry')
    # Label the x-axis as 'Year'
    plt.xlabel('Year')
    # Label the y-axis as 'Average Workweek Length (Hours)'
    plt.ylabel('Average Workweek Length (Hours)')
    # Set the x-ticks to correspond to the years
    plt.xticks(years)
    # Enable grid for better readability of the plot
    plt.grid(True)
    plt.savefig('average_workweek_length.pdf', format='pdf')
    plt.show()
