#comment
class Person():
    def __init__(self, name, age):#constructor
        self.name = name
        self.age = age
    def display(self):#method
        print("Name:", self.name, "Age:", self.age)
    def greet(self):
        print("Hello", self.name)
#comment
p = Person("John", 36) 
""" This is a multi-line 
    comment """
p.display()
''' This is a multi-line 
    comment 2 '''
p.greet()#comment
print("this # is not a comment")

if __name__ == '__test__':
    print("Hello World")
print("'''this is not a comment'''")