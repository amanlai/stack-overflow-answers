It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/72299178/19123103

## How to create instance of multiple inherited class?

> I have this code:
> 
>     class Person:
>         def __init__(self, name, last_name, age):
>             self.name = name
>             self.last_name = last_name
>             self.age = age 
>     
>     class Student(Person):
>         def __init__(self, name, last_name, age, indexNr, notes):
>             super().__init__(name, last_name, age)
>             self.indexNr = indexNr
>             self.notes = notes
>     
>     class Employee(Person):
>         def __init__(self, name, last_name, age, salary, position):
>             super().__init__(name, last_name, age)
>             self.salary = salary
>             self.position = position
>     
>     class WorkingStudent(Student, Employee):
>         def __init__(self, name, last_name, age, indexNr, notes, salary, position):
>             Student.__init__(name, last_name, age, indexNr, notes)
>             Employee.__init__(name, last_name, age, salary, position)
> 
> I want to create a WorkingStudent instance like this:
> 
>     ws = WorkingStudent("john", "brown", 18, 1, [1,2,3], 1000, 'Programmer')
> 
> but it's not working, I get this error:
> 
>     TypeError: __init__() missing 1 required positional argument: 'notes'
> 
> Or what I am doing wrong here? Also, I have already tried `super()` in WorkingStudent class but it calls only the constructor of the first passed class. i.e in this case `Student`.

Instead of explicit classes, use `super()` to pass arguments along the mro:

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

Check mro:

    WorkingStudent.__mro__
    (__main__.WorkingStudent,
     __main__.Student,
     __main__.Employee,
     __main__.Person,
     object)

---

When you create an instance of WorkingStudent, it's better if you pass keyword arguments so that you don't have to worry about messing up the order of arguments.

Since WorkingStudent defers the definition of attributes to parent classes, immediately pass all arguments up the hierarchy using `super().__init__(**kwargs)` since a child class doesn't need to know about the parameters it doesn't handle. The first parent class is Student, so self.IndexNr etc are defined there. The next parent class in the mro is Employee, so from Student, pass the remaining keyword arguments to it, using `super().__init__(**kwargs)` yet again. From Employee, define the attributes defined there and pass the rest along the mro (to Person) via `super().__init__(**kwargs)` yet again.

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