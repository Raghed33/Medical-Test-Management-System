#Raghed Isleem 1211326 _ Mais Younis 1212326
class MedicalTest:

    def __init__(self, name, date, result, unit, status, result_time=None):
        'Initialize a new MedicalTest instance with the provided attributes.'
        self.name = name
        self.date = date
        self.result = result
        self.unit = unit
        self.status = status
        self.result_time = result_time

    def __str__(self):
        'Return a string representation of the MedicalTest instance.'
        result_time_str = f",{self.result_time}" if self.result_time else ""
        return f"{self.name},{self.date},{self.result},{self.unit},{self.status}{result_time_str}"