#Raghed Isleem 1211326 _ Mais Younis 1212326
# Provides functionality for reading from and writing to CSV (Comma Separated Values) files
import csv
# The 're' module allows for working with regular expressions, which are used for searching, matching, and manipulating strings based on patterns.
import re
# Supplies classes for manipulating dates and times
from datetime import datetime
from  MedicalTest import MedicalTest # Importing the MedicalTest class
from Patient import Patient  # Importing the Patient class


class MedicalRecordSystem:
    def __init__(self):
        self.patients = {} # Dictionary to store patient records, with patient_id as the key

    def get_patient(self, patient_id):
        # Retrieve a patient by their ID from the dictionary
        return self.patients.get(patient_id)

    def validate_patient_id(self, patient_id):
        # Check if the patient ID is a 7-digit integer
        if patient_id.isdigit() and len(patient_id) == 7:
            return True
        print("Error: Patient ID must be a 7-digit integer.")
        return False

    def validate_test_name(self, test_name):
        # Validate the test name against a set of allowed values
        valid_tests = {"Hgb", "BGT", "LDL", "systole", "diastole"}
        if test_name.lower() in {v.lower() for v in valid_tests}:
            return True
        print("Error: The test name must be one of the following: Hgb, BGT, LDL, systole, diastole")
        return False

    def validate_test_date(self, test_date):
        # Check if the test date is in the correct format
        try:
            datetime.strptime(test_date, "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            print("Error: Test date must be in the format YYYY-MM-DD HH:MM.")
            return False

    def validate_date(self, date_str):
        """Validate the date format as YYYY-MM-DD."""
        try:
            # Try to parse the date string into a datetime object
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            # If parsing fails, the format is incorrect
            return False

    def validate_unit(self, unit):
        # Validate the unit of measurement for the test result
        valid_units = {"mg/dL", "g/dL", "mm Hg"}
        if unit in valid_units:
            return True
        print("Error: The unit must be one of the following: mg/dL, g/dL, mm Hg")
        return False

    def validate_status(self, status):
        # Validate the status of the test result
        valid_statuses = {"Pending", "Completed", "Reviewed"}
        if status.lower() in {v.lower() for v in valid_statuses}:
            return True
        print("Error: Status must be one of the following: Pending, Completed, Reviewed")
        return False

    def add_patient(self, patient_id):
        # Add a new patient to the dictionary if they do not already exist
        if patient_id not in self.patients:
            self.patients[patient_id] = Patient(patient_id)

    def add_test_record(self):
        # Collect and validate test information, then add the test record to the patient
        while True:
            patient_id = input("Enter Patient ID (7 digits): ")
            if self.validate_patient_id(patient_id):
                break

        self.add_patient(patient_id)

        while True:
            test_name = input(
                "Enter Test Name (Hgb, BGT, LDL, systole, diastole): ")
            if self.validate_test_name(test_name):
                break

        while True:
            test_date = input("Enter Test Date (YYYY-MM-DD HH:MM): ")
            if self.validate_test_date(test_date):
                break

        result = input("Enter Result: ")

        while True:
            unit = input("Enter the Unit (mg/dL, g/dL, mm Hg): ")
            if self.validate_unit(unit):
                break

        while True:
            status = input("Enter Status (Pending, Completed, Reviewed): ")
            if self.validate_status(status):
                break

        result_time = None
        # Check if the status is "completed"
        if status.lower() == "completed":
            # If so, prompt the user to enter the result date and time
            while True:
                result_time = input(
                    "Enter Results Date and Time (YYYY-MM-DD HH:MM): ")
                if self.validate_test_date(result_time):
                    break
        #creating a new instance of MedicalTest class
        new_test = MedicalTest(test_name,test_date,result,unit,status,result_time)
        self.patients[patient_id].add_test(new_test)

        # Save the changes immediately after adding a record
        self.save_to_file("midecalRecord.txt")
        print("Record added successfully!")

    def add_new_medical_test(self):
        print("Add New Medical Test Type")

        # Collecting test information from the user
        while True:
            test_name = input("Enter Test Name: ")
            if test_name:
                break
            print("Error: Test name cannot be empty.")

        #Check that the lower bound is less than the upper bound
        while True:
            try:
                range_low = float(input("Enter the lower bound of the test range: "))
                range_high = float(input("Enter the upper bound of the test range: "))
                if range_low < range_high:
                    break
                else:
                    print("Error: The lower bound must be less than the upper bound.")
            except ValueError:
                print("Error: Please enter valid numeric values for the range.")

        while True:
            unit = input("Enter the Unit: ")
            if unit:
                break
            print("Error: Unit cannot be empty.")

        while True:
            # The strip() method is used to remove any whitespace characters (such as spaces, tabs, or newlines) from the input string.
            result_time = input("Enter new result time: ").strip()
            # Validate the input time format
            try:
                datetime.strptime(result_time, "%H:%M:%S")
                print("Valid time format.")
                break  # Exit the loop if the time format is valid
            except ValueError:
                print("Invalid time format. Please enter time in hh:mm:ss format.")

        # Define the test file where the new test type will be saved
        test_file = "medicalTest.txt"

        # Writing the new test type to the file
        with open(test_file, "a") as file:
            file.write(f"{test_name};>{range_low},<{range_high};{unit};{result_time}\n")

        print("New medical test type added successfully!")

    def update_test_result(self):
        # Prompt user to enter a valid patient ID
        while True:
            patient_id = input("Enter Patient ID (7 digits): ")
            if not self.validate_patient_id(patient_id):
                print("Invalid Patient ID format. Please try again.")
                continue
            if patient_id not in self.patients:
                print("Error: Patient ID not found. Please enter a valid ID.")
            else:
                # Print all records for this patient
                print("Patient records:")
                for test in self.patients[patient_id].get_tests():
                    print(test)
                break

        # Prompt user to enter a valid test name
        while True:
            test_name = input("Enter Test Name (Hgb, BGT, LDL, systole, diastole):").strip().lower()
            if not self.validate_test_name(test_name):
                print("Invalid test name. Please enter a valid test name.")
                continue

            matching_tests = [
                test for test in self.patients[patient_id].get_tests()
                if test.name.lower() == test_name
            ]

            if not matching_tests:
                print("Error: Test name not found for the patient. Please enter a valid test name.")
            else:
                # Print all records for this patient with the specified test name
                print("Matching records:")
                for test in matching_tests:
                    print(test)
                break

        # Prompt user to enter a valid test date
        while True:
            test_date = input("Enter Test Date (YYYY-MM-DD HH:MM): ")
            if not self.validate_test_date(test_date):
                print("Invalid date format. Please enter the date in YYYY-MM-DD HH:MM format.")
                continue

            test_to_update = None
            for test in matching_tests:
                if test.date == test_date:
                    test_to_update = test
                    break

            if not test_to_update:
                print("Error: The test date not found for the patient. Please enter again.")
            else:
                break

        # Print current values
        print(f"Current Test Value: {test_to_update.result}")
        new_value = input("Enter new Test Value: ")

        print(f"Current Test Status: {test_to_update.status}")
        while True:
            new_status = input("Enter new Test Status (Pending/Completed/Reviewed): ").capitalize()
            if new_status in {"Pending", "Completed", "Reviewed"}:
                break
            else:
                print("Invalid status. Please enter one of the following: Pending, Completed, Reviewed.")

        # Handle status change
        if test_to_update.status.lower() == "completed" and new_status.lower() in {"pending","reviewed"}:
            test_to_update.result_time = None  # Remove the result time if status changes from completed to pending or reviewed
        elif test_to_update.status.lower() != "completed" and new_status.lower() == "completed":
            while True:
                result_time = input("Enter Results Date and Time (YYYY-MM-DD HH:MM): ")
                if self.validate_test_date(result_time):
                    test_to_update.result_time = result_time
                    break

        # Update the test with new values
        test_to_update.result = new_value
        test_to_update.status = new_status

        # Print the updated record
        print("Updated Test Record:")
        print(test_to_update)

        # Save the updated records back to the file
        self.save_to_file("midecalRecord.txt")
        print("Test record updated successfully!")

    def update_medical_tests(self):
        # Read the existing tests from the file
        with open("medicalTest.txt", 'r') as file:
            lines = file.readlines()

        # Create a dictionary to hold test data for easy lookup
        tests = {}
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(';')
                if len(parts) >= 3:
                    test_name = parts[0]
                    test_range = parts[1]
                    unit = parts[2]
                    result_time = parts[3] if len(parts) > 3 else ""
                    tests[test_name.lower()] = f"{test_name};{test_range};{unit};{result_time}"

        # Get a valid test name from the user
        while True:
            test_name = input("Enter Test Name to update: ").strip().lower()
            if test_name in tests:
                print(f"Current details: {tests[test_name]}")
                break
            else:
                print("Error: Test name not found. Please enter a valid test name.")

        # Get new details for the test
        while True:
            try:
                # Check that the lower bound is less than the upper bound
                range_low = float(input("Enter the new lower bound of the test range: "))
                range_high = float(input("Enter the new upper bound of the test range: "))
                if range_low < range_high:
                    break
                else:
                    print("Error: The lower bound must be less than the upper bound.")
            except ValueError:
                print("Error: Please enter valid numeric values for the range.")

        while True:
            unit = input("Enter new unit: ").strip()
            if unit:  # Ensure the unit is not empty
                break
            else:
                print("Error: Unit cannot be empty. Please enter a valid unit.")

        while True:
            # Prompt for new result time and validate format
            result_time = input("Enter new result time (HH:MM:SS): ").strip()
            try:
                # Validate the input time format
                datetime.strptime(result_time, "%H:%M:%S")
                break  # Exit the loop if the format is valid
            except ValueError:
                print("Error: Invalid time format. Please enter time in HH:MM:SS format.")

        # Update the test entry
        tests[test_name] = f"{test_name};{range_low};{range_high};{unit};{result_time}"
        print(f"Test '{test_name}' updated.")

        # Write the updated tests back to the file
        with open("medicalTest.txt", 'w') as file:
            for test in tests.values():
                file.write(f"{test}\n")

        print("Medical tests updated successfully!")

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            for patient_id, patient in self.patients.items():
                for test in patient.get_tests():
                    file.write(f"{patient_id}:{test}\n")

    def load_from_file(self, filename):
        try:
            # Attempt to open the file for reading
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        if ":" in line:
                            try:
                                patient_id, test_data = line.split(":", 1)
                                test_fields = test_data.split(",")
                                if len(test_fields) >= 5:
                                    test_name = test_fields[0]
                                    test_date = test_fields[1]
                                    result = test_fields[2]
                                    unit = test_fields[3]
                                    status = test_fields[4]
                                    result_time = test_fields[5] if len(test_fields) > 5 else None

                                    self.add_patient(patient_id)
                                    test = MedicalTest(test_name, test_date, result, unit, status, result_time)
                                    self.patients[patient_id].add_test(test)
                                else:
                                    print(f"Error: Incomplete test data in line: {line}")
                            except ValueError as e:
                                print(f"Error processing line: {line}. Details: {e}")
                        else:
                            print(f"Skipping improperly formatted line: {line}")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except IOError as e:
            print(f"Error: Unable to open or read the file '{filename}'. Details: {e}")

    def print_records(self):
        for patient_id, patient in self.patients.items():
            print(f"Patient ID:{patient_id}")
            for test in patient.get_tests():
                print(f"{test}")

    def filter_tests(self):
        # Initialize the filter criteria
        criteria = {
            "patient_id": None,
            "test_name": None,
            "abnormal_test": None,
            "specific_period": None,
            "test_status": None,
            "turnaround_time": None,
        }

        # Get the user's choice for each criterion
        print("Enter (0) for things you don't want to filter and (1) for things you want")

        # Validate and get Patient ID
        while True:
            if int(input("1-Patient ID (0 or 1) ? ")) == 1:
                patient_id = input("Enter Patient ID: ").strip()
                if self.validate_patient_id(patient_id):
                    if patient_id in self.patients:
                        criteria["patient_id"] = patient_id
                        break
                    else:
                        print("Error: Patient ID not found. Please enter a valid ID.")
                else:
                    print("Invalid Patient ID format. Please try again.")
            else:
                break

        # Validate and get Test Name
        while True:
            if int(input("2-Test Name (0 or 1)? ")) == 1:
                test_name = input("Enter Test name (Hgb, BGT, LDL, systole, diastole): ").strip().lower()
                if self.validate_test_name(test_name):
                    criteria["test_name"] = test_name
                    break
                else:
                    print("Invalid test name. Please enter a valid test name.")
            else:
                break

        # Set Abnormal Test criterion
        if int(input("3-Abnormal Test (0 or 1)? ")) == 1:
            criteria["abnormal_test"] = True

        # Validate and get Specific Period
        while True:
            if int(input("4-Specific Period (0 or 1)? ")) == 1:
                start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
                end_date = input("Enter End Date (YYYY-MM-DD): ").strip()
                if self.validate_date(start_date) and self.validate_date(end_date):
                    criteria["specific_period"] = (start_date, end_date)
                    break
                else:
                    print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
            else:
                break

        # Validate and get Test Status
        while True:
            if int(input("5-Test Status (0 or 1)? ")) == 1:
                test_status = input("Enter Test Status (Pending/Completed/Reviewed): ").strip().lower()
                if test_status in ["pending", "completed", "reviewed"]:
                    criteria["test_status"] = test_status
                    break
                else:
                    print("Invalid test status. Please enter one of the following: Pending, Completed, Reviewed.")
            else:
                break

        # Validate and get Turnaround Time
        while True:
            if int(input("6-Test turnaround time within a period (0 or 1)? ")) == 1:
                try:
                    min_time = int(input("Enter Minimum Turnaround Time (minutes): "))
                    max_time = int(input("Enter Maximum Turnaround Time (minutes): "))
                    if min_time >= 0 and max_time >= min_time:
                        criteria["turnaround_time"] = (min_time, max_time)
                        break
                    else:
                        print("Invalid turnaround time range. Minimum time should be less than or equal to maximum time.")
                except ValueError:
                    print("Invalid input. Please enter valid integers for turnaround times.")
            else:
                break

        # Filter and display the tests based on criteria
        matching_tests = []  # Initializes a list to store tests that match the filter criteria
        if criteria["abnormal_test"]:
            matching_tests = self.search_abnormal_tests(criteria)  # Adjusted to collect results

        for patient_id, patient in self.patients.items():
            if criteria["patient_id"] and patient_id != criteria["patient_id"]:
                continue
            for test in patient.get_tests():
                if criteria["test_name"] and test.name.lower() != criteria["test_name"]:
                    continue

                if criteria["abnormal_test"]:
                    # Extract the test name from matching_tests for comparison
                    test_name_in_matching = any(
                        test.name.lower() == t.split(";")[0].strip().lower()
                        for t in matching_tests
                    )
                    if not test_name_in_matching:
                        continue

                if criteria["specific_period"]:
                    start_date, end_date = criteria["specific_period"]
                    if not (start_date <= test.date <= end_date):
                        continue

                if criteria["test_status"] and test.status.lower() != criteria["test_status"]:
                    continue

                if criteria["turnaround_time"]:
                    min_time, max_time = criteria["turnaround_time"]
                    if not test.result_time:
                        continue
                    turnaround_minutes = self.calculate_turnaround_time(test)
                    if not (min_time <= turnaround_minutes <= max_time):
                        continue

                # If all criteria match, add the test to the matching list
                matching_tests.append(f"{patient_id}:{test}")

        # Print the matching tests
        if matching_tests:
            for test in matching_tests:
                print(test)
        else:
            print("No matching tests found.")

    def is_abnormal_test(self, test):
        # Check if the test result is abnormal based on the test's range
        return float(test.result) > float(test.get_range_high()) or float(test.result) < float(test.get_range_low())

    def get_test_range(self, test_name):
        #Retrieve the range for a given test from medicalTest.txt.
        try:
            with open("medicalTest.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(";", 1)
                    if len(parts) < 2:
                        continue  # Skip lines that don't have enough parts
                    name, range_info = parts
                    if name.lower() == test_name:
                        greater_than = None
                        less_than = None

                        # Parse greater_than value if present
                        if ">" in range_info:
                            try:
                                greater_than = float(range_info.split(">")[1].split(",")[0].strip())
                            except ValueError:
                                print(f"Error: Invalid greater than value in range_info: {range_info}")

                        # Parse less_than value if present
                        if "<" in range_info:
                            try:
                                less_than = float(range_info.split("<")[1].strip())
                            except ValueError:
                                print(f"Error: Invalid less than value in range_info: {range_info}")

                        return greater_than, less_than
        except Exception as e:
            print(f"Error reading medicalTest.txt: {e}")
        return None, None  # Ensure that we return a tuple even if there is an error

    def calculate_turnaround_time(self, test):
        # Extract date and result_time from the test object
        if test.result_time:
            result_time = datetime.strptime(test.result_time, "%Y-%m-%d %H:%M")
            test_date = datetime.strptime(test.date, "%Y-%m-%d %H:%M")
            turnaround_time = (result_time - test_date).total_seconds() / 60  # in minutes
            return turnaround_time
        return 0

    def generate_summary_report(self, tests):
        #Generate a summary report of test values and turnaround times
        test_values = [float(test.value) for test in tests]
        turnaround_times = [
            self.calculate_turnaround_time(test) for test in tests
            if self.calculate_turnaround_time(test) > 0
        ]

        print("\nSummary Report:")
        print(f"Number of Tests: {len(tests)}")
        print(f"Minimum Test Value: {min(test_values):.2f}")
        print(f"Maximum Test Value: {max(test_values):.2f}")
        print(f"Average Test Value: {sum(test_values) / len(test_values):.2f}")

        if turnaround_times:
            print(f"Minimum Turnaround Time: {min(turnaround_times):.2f} minutes")
            print( f"Maximum Turnaround Time: {max(turnaround_times):.2f} minutes")
            print(f"Average Turnaround Time: {sum(turnaround_times) / len(turnaround_times):.2f} minutes")
        else:
            print("No turnaround times available.")

    def search_tests_by_patient_id(self):
        patient_id = input("Enter Patient ID to search: ")
        if self.validate_patient_id(patient_id):
            patient = self.patients.get(patient_id)
            if patient:
                print(f"Patient ID: {patient_id}")
                for test in patient.get_tests():
                    print(f"  {test}")
            else:
                print("No records found for this Patient ID.")
        else:
            print("Invalid Patient ID.")

    def search_abnormal_tests(self, criteria):
        matching_abnormal_tests = []

        for patient_id, patient in self.patients.items():
            # If filtering by patient ID and it doesn't match, skip this patient
            if criteria["patient_id"] and patient_id != criteria["patient_id"]:
                continue

            for test in patient.get_tests():
                test_name = test.name.lower()
                test_result = float(test.result)  # Convert test result to float for comparison

                # Retrieve the test range from medicalTest.txt
                test_range = self.get_test_range(test_name)
                if not test_range:
                    continue  # Skip if the range is not found

                # Extract the lower and upper bounds
                greater_than, less_than = test_range

                # Ensure the test result falls outside the expected range (abnormal)
                if (greater_than is not None and test_result <= greater_than) or (
                        less_than is not None and test_result >= less_than):
                    # This is an abnormal test
                    matching_abnormal_tests.append(
                        f"Abnormal | Patient ID: {patient_id} | Test Name: {test.name} | Test Result: {test.result} | Expected Range: >{greater_than}, <{less_than}"
                    )

        # Print matching abnormal tests
        if matching_abnormal_tests:
            for abnormal_test in matching_abnormal_tests:
                print(abnormal_test)
        else:
            print("No abnormal tests found.")

    def export_all_records_to_csv(self, source_filename, destination_filename):
        # Open the source file for reading and the destination file for writing
        try:
            with open(source_filename,'r') as infile, open(destination_filename,'w',newline='') as outfile:
                reader = infile.readlines() # Read all lines from the source file
                writer = csv.writer(outfile)  # Create a CSV writer object for the destination file

                # Write CSV headers to the output file
                writer.writerow(["Patient ID","Test Name","Test Date","Test Value","Unit","Status","Result Date"])

                # Write each line from the source file to the CSV
                for line in reader:
                    if ":" in line:
                        patient_id, test_data = line.strip().split(":", 1)
                        test_fields = test_data.split(",")
                        if len(test_fields) >= 5:
                            writer.writerow([patient_id] + test_fields)

            print(f"Records successfully exported to {destination_filename}.")
        except Exception as e:
            print(f"Error exporting records: {e}")

    def import_records_from_csv(self, filename):
        try:
            with open(filename,'r') as file:
                reader = csv.reader(file)
                headers = next(reader)  # Skip the header row

                # Open midecalRecord.txt in write mode to overwrite existing content
                with open('midecalRecord.txt','a') as medical_record_file:
                    for row in reader:
                        if len(row) >= 6:
                            patient_id = row[0]
                            test_name = row[1]
                            test_date = row[2]
                            test_value = row[3]
                            unit = row[4]
                            status = row[5]
                            result_time = row[6] if len(row) > 6 else None

                            # Ensure the patient exists
                            if patient_id not in self.patients:
                                self.patients[patient_id] = Patient(patient_id)

                            # Create the MedicalTest object and add it to the patient
                            test = MedicalTest(test_name,test_date,test_value,unit,status,result_time)
                            self.patients[patient_id].add_test(test)

                            # Save the record in the midecalRecord.txt file
                            medical_record_file.write(f"{patient_id}:{test_name},{test_date},{test_value},{unit},{status},{result_time}\n")

            print(f"Records successfully imported from {filename}.")
        except Exception as e:
            print(f"Error importing records: {e}")

    def delete_test_result(self):
        while True:
            patient_id = input("Enter Patient ID (7 digits): ")

            # Validate the patient ID format
            if not self.validate_patient_id(patient_id):
                continue

            # Check if the patient ID exists
            patient = self.get_patient(patient_id)
            if patient:
                print("Patient ID found.")
                # Print all tests for the patient
                if patient.get_tests():
                    print("Test Records for Patient:")
                    for test in patient.get_tests():
                        status = test.status.lower()
                        if status == 'completed' and test.result_time:
                            print(
                                f"Test Name: {test.name}, Date: {test.date}, Status: {status} , Result Date: {test.result_time}")
                        else:
                            print(f"Test Name: {test.name}, Date: {test.date}, Status: {status}")
                else:
                    print("No test records found for this patient.")
                break
            else:
                print("Error: Patient ID not found. Please enter a valid ID.")

        while True:
            test_name = input("Enter Test Name (Hgb, BGT, LDL, systole, diastole): ")

            # Validate the test name format
            if not self.validate_test_name(test_name):
                continue

            # Check if the test name exists for this patient
            tests = patient.get_tests(test_name)
            if tests:
                print("Test Name found.")
                # Print all tests with the given test name
                for test in tests:
                    print(
                        f"Date: {test.date}, Status: {'Completed' if hasattr(test, 'result_time') and test.result_time else status }")
                break
            else:
                print("Error: Test name not found for the patient. Please enter a valid test name.")

        while True:
            test_date = input("Enter Test Date (YYYY-MM-DD HH:MM): ")

            # Validate the test date format
            if not self.validate_test_date(test_date):
                print("Error: Test date must be in the format YYYY-MM-DD HH:MM.")
                continue

            # Check if the test date exists for this patient
            matching_tests = [test for test in tests if test.date.startswith(test_date)]
            if matching_tests:
                print("Test Date found.")
                break
            else:
                print("Error: Test date not found for the patient. Please enter a valid date.")

        # Check if the test is completed (i.e., it has a result time)
        completed_test = None
        for test in matching_tests:
            if hasattr(test, 'result_time') and test.result_time:
                completed_test = test
                break

        if matching_tests:
            # Delete the first matching test (or handle multiple matches as needed)
            patient.delete_test(test_name,test_date)
            print("Test result deleted successfully.")
        else:
            print("Error: Test date not found for the patient. Please enter a valid date.")
        self.save_to_file("midecalRecord.txt")

    def display_menu(self):
        while True:
            print("Medical Test Management System")
            print("1. Add new medical test type")
            print("2. Add a new medical test record")
            print("3. Update a patient record")
            print("4. Update medical tests in the medicalTest file")
            print("5. Filter medical tests")
            print("6. Generate textual summary reports")
            print("7. search_tests_by_patient_id ")
            print("8. Delete a medical test record")
            print("9. Export medical records to a comma separated file")
            print("10. Import medical records from a comma separated file")
            print("11. Exit")

            choice = input("Enter your choice (1-7): ")

            if choice == "1":
                self.add_new_medical_test()
            elif choice == "2":
                self.add_test_record()
            elif choice == "3":
                 self.update_test_result()
            elif choice == "4":
                 self.update_medical_tests()
            elif choice == "5":
                self.filter_tests()
            elif choice == "6":
                self.generate_summary_report()
            elif choice == "7":
                self.search_tests_by_patient_id()
            elif choice == "8":
                self.delete_test_result()
            elif choice == "9":
                filename = input(
                        "Enter the filename to save the records (default is 'medical_records.csv'): "
                ).strip()
                filename = filename if filename else "medical_records.csv"
                self.export_all_records_to_csv("midecalRecord.txt", filename)
            elif choice == "10":
                filename = input(
                    "Enter the filename to import records from: ").strip()
                self.import_records_from_csv(filename)
            elif choice == "11":
                print("Goodbye")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")

# Create an instance of the MedicalRecordSystem class
system = MedicalRecordSystem()
# Load patient records from midecalRecord.txt file into the system
system.load_from_file("midecalRecord.txt")
# Display the menu options to the user
system.display_menu()
system.save_to_file("midecalRecord.txt")