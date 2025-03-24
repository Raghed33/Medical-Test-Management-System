#Raghed Isleem 1211326 _ Mais Younis 1212326
class Patient:
    def __init__(self, patient_id):
        'Initialize a new Patient instance with a unique patient ID.'

        self.patient_id = patient_id
        self.tests = {}  # Use a dictionary to store tests with a tuple of (test name, test date) as the key

    def add_test(self, test):
        'Add a test to the patient record.'
        self.tests[(test.name, test.date)] = test

    def update_test(self, test_name, test_date, updated_test):
        'Update an existing test in the patient record.'
        key = (test_name, test_date)
        if key in self.tests:
            self.tests[key] = updated_test
            return True
        return False

    def delete_test(self, test_name, test_date):
        'Delete a test from the patient record.'
        key = (test_name, test_date)
        if key in self.tests:
            del self.tests[key]
            return True
        return False

    def get_tests(self, test_name=None):
        'Retrieve tests from the patient record.'
        if test_name:
            return [test for (name, date), test in self.tests.items() if name == test_name]
        return list(self.tests.values())