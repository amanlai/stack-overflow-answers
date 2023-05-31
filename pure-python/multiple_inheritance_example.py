# How to create instance of multiple inherited class?

# Must check method resolution order
# use `super()` method to pass arguments to parent methods

class Person:
    def __init__(self, name, last_name, age):
        self.name = name
        self.last_name = last_name
        self.age = age 

class Student(Person):
    def __init__(self, name, last_name, age, indexNr, notes, salary, position):
        # since Employee comes after Student in the mro, pass its arguments using super
        super().__init__(name, last_name, age, salary, position)
        self.indexNr = indexNr
        self.notes = notes

class Employee(Person):
    def __init__(self, name, last_name, age, salary, position):
        super().__init__(name, last_name, age)
        self.salary = salary
        self.position = position

class WorkingStudent(Student, Employee):
    def __init__(self, name, last_name, age, indexNr, notes, salary, position):
        # pass all arguments along the mro
        super().__init__(name, last_name, age, indexNr, notes, salary, position)

# uses positional arguments            
ws = WorkingStudent("john", "brown", 18, 1, [1,2,3], 1000, 'Programmer')
# then you can print stuff like
print(f"My name is {ws.name} {ws.last_name}. I'm a {ws.position} and I'm {ws.age} years old.")
# My name is john brown. I'm a Programmer and I'm 18 years old.




# Using kwargs is more readable and less error-prone

class Person:
    def __init__(self, name, last_name, age):
        self.name = name
        self.last_name = last_name
        self.age = age 

class Student(Person):
    def __init__(self, indexNr, notes, **kwargs):
        # since Employee comes after Student in the mro, pass its arguments using super
        super().__init__(**kwargs)
        self.indexNr = indexNr
        self.notes = notes

class Employee(Person):
    def __init__(self, salary, position, **kwargs):
        super().__init__(**kwargs)
        self.salary = salary
        self.position = position

class WorkingStudent(Student, Employee):
    def __init__(self, **kwargs):
        # pass all arguments along the mro
        super().__init__(**kwargs)

# keyword arguments (not positional arguments like the case above)
ws = WorkingStudent(name="john", last_name="brown", age=18, indexNr=1, notes=[1,2,3], salary=1000, position='Programmer')