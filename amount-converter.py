import csv 
import argparse
from os import path
from dataclasses import dataclass

@dataclass
class Transaction:
    Date: str
    Description: str
    Original_Description: str
    Amount: float
    Transaction_Type: str
    Category: str
    Account_Name: str
    Labels: str
    Notes: str
    def __str__(self):
        selected_keys = ['Date', 'Description','Amount']
        # Use a generator expression to create a string with key-value pairs
        values_str = ', '.join(f"{getattr(self, key)}" for key in selected_keys)
        return f"{values_str}"



def main(args):
    result_file = {}

    with open(args.file) as fs:
        file = csv.reader(fs,delimiter=',')
        for row in file:
            transaction = Transaction(*row)
            transaction.Account_Name = transaction.Account_Name.lower()
            if transaction.Transaction_Type == 'debit':
                transaction.Amount = '-' + transaction.Amount
            if transaction.Account_Name not in result_file.keys():
                result_file[transaction.Account_Name] = [str(transaction)]
            else:
                result_file[transaction.Account_Name].append(str(transaction))


    for file in result_file.keys():
        filepath = "converted_"+file+".csv"
        with open(filepath, 'w', newline='') as f:
            print(f"Processing {file}")
            writer = csv.writer(f)
            header_row = ['Date', 'Description','Amount']
            writer.writerow(header_row)

            # Write each transaction as a row in the CSV file
            for transaction in result_file[file][1:]:
                writer.writerow(transaction.split(','))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, help='Transaction File')
    args = parser.parse_args()

    # Check for missing required arguments
    if not all([args.file]):
        parser.error("--file arg missing")

    # Call the main function with the parsed arguments
    main(args)