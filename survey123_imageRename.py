import os
import csv

#Specify the desired prefix for the file names
file_prefix = '2022_CommonGroundGolfCourse_FloristicInventory'

# Specify the path for the dir containing the image files
directory_path = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory'

# Specify the path for the csv containing the image records
imageDataCSV = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory/specimenImage_table_1.csv'

# Specify the path for the csv containing the survey123 record data
surveyRecordsCSV = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory/_2022_CommonGrounds_FloristicInventory_0.csv'

# Specify the path for the new csv with combined data
output_file = 'Q:/Research/Images(new)/FieldWork/SpecimenCollecting/2022_CommonGroundGolfCourse_FloristicInventory/_2022_CommonGrounds_FloristicInventory_output.csv'


# Function to get all the jpgs from a directory, sort them as they are in the directory, and add them to a list
def get_jpg_file_names(directory):
    jpg_file_names = sorted(
        [filename for filename in os.listdir(directory) if filename.endswith('.jpg')],
        key=lambda x: os.path.getmtime(os.path.join(directory, x))
    )
    return jpg_file_names

#Function to add the jpg file names to an existing csv in a new row.
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


# Get the JPG file names from the directory
jpg_files = get_jpg_file_names(directory_path)

# Add file names to the CSV file
add_file_names_to_csv(imageDataCSV, jpg_files)


# Function to populate data in csv containing image metadata (csv1) with data from csv containing csv records (csv2). Records are matched using ParentGlobalID in csv1 = GlobalID in csv2.
def populate_csv(imageDataCSV, surveyRecordsCSV, output_file):
    # Read data from CSV2 and create a dictionary of GlobalID and records
    with open(surveyRecordsCSV, 'r') as csv2:
        csv2_reader = csv.DictReader(csv2)
        csv2_data = {row['GlobalID']: row for row in csv2_reader}

    # Read data from CSV1 and populate with records from CSV2
    with open(imageDataCSV, 'r') as csv1:
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

# Populate imageDataCSV based on information from surveyRecordsCSV
populate_csv(imageDataCSV, surveyRecordsCSV, output_file)

#Rename the files using data from the output csv
def rename_files_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            # Combine values from multiple rows to generate new file name
            new_file_name = f"{directory_path}/{file_prefix}_{row['Primary Collector'].replace('_','').replace(' ','')}_{row['Collector Number']}_{i}.jpg"

            # Rename the file
            old_file_path = directory_path+'/'+row['ImageFile']
            new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)
            os.rename(old_file_path, new_file_path)

            # Update the CSV with the new file name
            row['ImageFile'] = new_file_path

    # Rewrite the updated CSV file
    # with open(csv_file, 'w', newline='') as file:
    #     writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
    #     writer.writeheader()
    #     writer.writerows(reader)

# Specify the CSV file path
csv_file_path = output_file

# Call the function to rename files
rename_files_from_csv(csv_file_path)