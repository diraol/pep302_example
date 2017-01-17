from example.v2.myclass import MyClass as MyClass2
print("\n\n -- LOADED MYCLASS2 -- \n\n")
from example.v3.myclass import MyClass as MyClass3
print("\n\n -- LOADED MYCLASS3 -- \n\n")
from example.v1.myclass import MyClass as MyClass1
print("\n\n -- LOADED MYCLASS1 -- \n\n")

MyClass1()
MyClass2()
MyClass3()
