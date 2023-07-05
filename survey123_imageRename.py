import os
import csv

def get_jpg_file_names(directory):
    jpg_file_names = sorted(
        [filename for filename in os.listdir(directory) if filename.endswith('.jpg')],
        key=lambda x: os.path.getmtime(os.path.join(directory, x))
    )
    return jpg_file_names

def add_file_names_to_csv(csv_file, file_names):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        header = rows[0]
        header.append('ImageFile')  # Add a new column header

        for i, row in enumerate(rows[1:], start=1):
            if i <= len(file_names):
                row.append(file_names[i-1])
            else:
                row.append('')  # Add an empty cell if no file name available

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# Specify the directory path
directory_path = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory'

# Specify the CSV file path
csv_file_path = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory/specimenImage_table_1.csv'

# Get the JPG file names from the directory
jpg_files = get_jpg_file_names(directory_path)

# Add file names to the CSV file
add_file_names_to_csv(csv_file_path, jpg_files)


# # Function to get file names from directory
# def get_file_names(directory):
#     file_names = sorted(os.listdir(directory), key=lambda x: os.path.getmtime(os.path.join(directory, x)))
#     return file_names

# # Specify the directory path
# directory_path = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory'

# # Get the file names from the directory
# files = get_file_names(directory_path)

# # Specify the existing CSV file path
# csv_file = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory/specimenImage_table_1.csv'

# # Specify the new CSV file path
# new_csv_file = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory/specimenImage_table__WithFileNames.csv'

# # Open the existing CSV file and create a new CSV file
# with open(csv_file, 'r') as input_file, open(new_csv_file, 'w', newline='') as output_file:
#     reader = csv.reader(input_file)
#     writer = csv.writer(output_file)

#     # Read the existing rows and add a new column for file names
#     for i, row in enumerate(reader):
#         if i == 0:  # Header row
#             row.append('File Name')  # Add new column header
#         else:
#             row.append(files[i - 1])  # Add file name from the directory

#         writer.writerow(row)

# print(f"File names added successfully to {new_csv_file}.")

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
        csv2FieldNames = csv2_reader.fieldnames
        fieldnames.extend(csv2FieldNames)

        with open(output_file, 'w', newline='') as output:
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()

            for row in csv1_reader:
                parent_global_id = row['ParentGlobalID']
                if parent_global_id in csv2_data:
                    csv2_row = csv2_data[parent_global_id]
                    row.update(csv2_row)  # Update the row with CSV2 data

                writer.writerow(row)

    print(f"Data populated successfully in {output_file}.")

 


# Specify the file paths for CSV1, CSV2, and the output file
csv1_file = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory/specimenImage_table_1.csv'
csv2_file = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory/_2022_CommonGrounds_FloristicInventory_0.csv'
output_file = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory/_2022_CommonGrounds_FloristicInventory_output.csv'

# Populate CSV1 based on information from CSV2
populate_csv(csv1_file, csv2_file, output_file)
