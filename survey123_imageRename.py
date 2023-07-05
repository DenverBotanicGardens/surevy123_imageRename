import csv

# Function to populate data in CSV1 based on information from CSV2
def populate_csv(csv1_file, csv2_file, output_file):
    # Read data from CSV2 and create a dictionary of GlobalID and records
    with open(csv2_file, 'r') as csv2:
        csv2_reader = csv.DictReader(csv2)
        csv2_data = {row['GlobalID']: row for row in csv2_reader}

    # Read data from CSV1 and populate with records from CSV2
    with open(csv1_file, 'r') as csv1:
        csv1_reader = csv.DictReader(csv1)
        fieldnames = csv1_reader.fieldnames  # Preserve the fieldnames

        with open(output_file, 'w', newline='') as output:
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()

            for row in csv1_reader:
                parent_global_id = row['parentGlobalID']
                if parent_global_id in csv2_data:
                    csv2_row = csv2_data[parent_global_id]
                    row.update(csv2_row)  # Update the row with CSV2 data

                writer.writerow(row)

    print(f"Data populated successfully in {output_file}.")


# Specify the file paths for CSV1, CSV2, and the output file
csv1_file = 'csv1.csv'
csv2_file = 'csv2.csv'
output_file = 'output.csv'

# Populate CSV1 based on information from CSV2
populate_csv(csv1_file, csv2_file, output_file)
