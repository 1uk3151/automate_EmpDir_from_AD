class HTMLTemplate:

    def __init__(self, html_file):
        self.html_file = html_file

    def heading(self):
        with open(self.html_file, mode="w") as employee_html:
            employee_html.write("""
            <h1>Employee Directory</h1>
            <hr/>
            <br/>
            """)

    def list_employee(self, lastname, firstname, title, department, office, phone, email):
        with open(self.html_file, mode="a") as employee_html:
            employee_html.write(f"""
            <h3>{lastname}, {firstname}</h3> 
                <h4>{title}</h4>
                    <p>Department: {department}</p>
                    <p>Office: {office}</p>
                    <p>Contact: {phone}, {email}</p>
            <br/>
            """)








