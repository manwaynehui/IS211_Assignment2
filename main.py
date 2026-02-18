import argparse
import urllib.request
import logging
import datetime
import csv
import sys

"""PART II: downloadData"""


def downloadData(url):
    """Downloads the data from the URL and returns the content as a string."""
    try:
        response = urllib.request.urlopen(url)
        """Returns the raw data decoded into a string for processing."""
        return response.read().decode('utf-8')
    except Exception as e:
        """Requirement: Catch download exceptions and exit the program."""
        print(f"Error downloading data: {e}")
        sys.exit()


"""PART III: processData"""


def processData(file_content):
    """Processes CSV data and returns a dictionary mapping ID to (name, birthday)."""
    personData = {}
    """Access the logger named 'assignment2' as required."""
    logger = logging.getLogger('assignment2')

    """Split the downloaded content into lines for the CSV reader."""
    lines = file_content.splitlines()
    reader = csv.reader(lines)

    for linenum, row in enumerate(reader):
        """Skip the header row if the first column is 'id'."""
        if linenum == 0 and row[0].lower() == 'id':
            continue

        try:
            user_id = int(row[0])
            name = row[1]
            """Requirement: Convert dd/mm/yyyy string into a Date object."""
            birthday = datetime.datetime.strptime(row[2], '%d/%m/%Y').date()
            personData[user_id] = (name, birthday)
        except (ValueError, IndexError):
            """Requirement: Log errors to errors.log using the specified format."""
            logger.error(f"Error processing line #{linenum + 1} for ID #{row[0]}")

    return personData


"""PART IV: displayPerson"""


def displayPerson(id, personData):
    """Prints the person's info or an error if the ID is missing."""
    if id in personData:
        name, birthday = personData[id]
        """Requirement: Format date object as YYYY-MM-DD for printing."""
        date_str = birthday.strftime('%Y-%m-%d')
        print(f"Person #{id} is {name} with a birthday of {date_str}")
    else:
        print("No user found with that id")


"""PART V: main"""


def main(url):
    """Setup the logging configuration to write to errors.log."""
    logging.basicConfig(
        filename='errors.log',
        level=logging.ERROR,
        format='%(message)s'
    )

    """Step 1: Download the CSV data from the provided URL."""
    csvData = downloadData(url)

    """Step 2: Process the CSV data into the personData dictionary."""
    personData = processData(csvData)

    """Step 3: Begin the user input loop for ID lookups."""
    while True:
        try:
            user_input = int(input("Enter an ID to lookup (0 or negative to exit): "))
            if user_input <= 0:
                """Exit the loop if user enters 0 or a negative number."""
                break
            displayPerson(user_input, personData)
        except ValueError:
            print("Please enter a valid numeric ID.")


if __name__ == "__main__":
    """Main entry point: Parse the --url argument and call main."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)