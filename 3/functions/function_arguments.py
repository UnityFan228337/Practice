#parameter is the variable in the fucntion with fucntion can work
#argument is the data that calling and putting in the parameter
def my_function(fname):#<- parameter
  print(fname + " Refsnes")

my_function("Emil") #<- argument
my_function("Tobias")
my_function("Linus")


#several parametrs, you have to put arguments in the all paramters
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes")


#you have to know the correct order
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function("dog", "Buddy")



#also you can make like this
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(animal = "dog", name = "Buddy")



#default parameter
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function() #<-return friend because its default value
my_function("Linus")

#only positional argument

def my_function(name, /):
  print("Hello", name)

my_function("Emil")


#only keyword arguments
def my_function(*, name):
  print("Hello", name)

my_function(name = "Emil")



#combining before / = positional only, after * keyword only
def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)