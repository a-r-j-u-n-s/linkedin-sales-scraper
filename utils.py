class NonEmployeeException(Exception):
    """
    Raised if it is likely that the given profile is somehow not actually a valid employee with a job title
    Ex: User's 'job title' is 'Student'
    """


class EmailError(Exception):
    """
    Raised if email data cannot be accessed
    """


class Employee:
    """
    Represents a single employee
    """
    def __init__(self, first_name: str, last_name: str, job_title: str, company: str, location: str):
        self.first_name = first_name
        self.last_name = last_name
        self.job_title = job_title
        self.location = location
        self.company = company

        # Based on Rocketreach email formatting (subject to change if Rocketreach goes down)
        self.email_formatting = {'first_initial': self.first_name[0].lower(), 'first': self.first_name.lower(),
                                 'last': self.last_name.lower(), 'last_initial': self.last_name[0].lower()}

