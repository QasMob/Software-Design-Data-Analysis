#!/usr/bin/env python3
import sys
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict


def question3(file):
    print("You have selected question 3")

    # Prompt the user for the required information
    print("JOB TYPE OPTIONS:\n1.Permanent\n2.Temporary (seasonal and non-seasonal)\n3.Seasonal")
    fileName = "allData.csv"
    jobType1 = int(input("Enter the first type of job to be compared: "))
    jobType2 = int(input("Enter the second type of job to be compared: "))
    year = input("Enter the year to be considered: ")
    outputFile = "job_type_data.csv"  # Output file name
    graphicsfile = "plot.pdf"  # Graphics file name

    # See if filename is valid and open file
    try:
        openFile = open(fileName, "r", encoding="utf-8-sig")
    except IOError:
        print(f"Unable to open file: {fileName}", file=sys.stderr)
        sys.exit(1)

    fileReader = csv.reader(openFile)

    jobTypes = ["Permanent",
                "Temporary (seasonal and non-seasonal)", "Seasonal"]

    jobType1 = jobTypes[jobType1-1]
    jobType2 = jobTypes[jobType2-1]

    # Create a list to store filtered data
    filtered_data = []

    # Iterate through csv for jobType1
    for line in fileReader:
        # Check criteria
        if line[5] == "Job vacancies":
            if line[4] == jobType1 and line[0][:4] == year:
                # Reduce line to the desired fields
                newLine = [line[4], line[0][:4], line[12]]
            # Check to see if line has a value
                if line[-5]:
                    filtered_data.append(newLine)
            elif line[4] == jobType2 and line[0][:4] == year:
                # Reduce line to the desired fields
                newLine = [line[4], line[0][:4], line[12]]
        # Check to see if line has a value
                if line[-5]:
                    filtered_data.append(newLine)

    # Reset file pointer to beginning of file

        # Close the file
    openFile.close()

    # Write filtered data to a new CSV file
    with open(outputFile, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        # Write headers
        writer.writerow(["Job Type", "Year", "Value"])
        # Write filtered data
        writer.writerows(filtered_data)

    print(f"Filtered data has been written to '{outputFile}'")

    # Now, let's use the previously provided code to generate a bar chart
    df = pd.DataFrame(filtered_data, columns=["Job Type", "Year", "Value"])

    # Group by 'Job Type' and calculate the mean of 'Value' for each job type
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    average_values = df.groupby('Job Type')['Value'].mean()

    # Plotting the bar chart
    plt.bar(average_values.index, average_values.values, color='green')
    plt.title(f'Average Value for Job Types in {year}')
    plt.xlabel('Job Type')
    plt.ylabel('Average Value')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.savefig('job_type_data_plot.pdf', format='pdf')
    plt.show()
