class Person: #parent class
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#make child independed
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)