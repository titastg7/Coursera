# ZeroDivisionError

def divide_by(a,b):
    return a/b

try:
    ans = print(divide_by(40,0))
except ZeroDivisionError as e:
    print(e, "We cannot divide by zero!")
except Exception as e :
    print(e, "Something went wrong!")

# IndexError

try:
    items = ['e', 'f', 'g']
    print(items[4])
except IndexError as e:
    print("Item does not exist in the list!")
    print(e.__class__)

# FileNotFoundError
try:
    with open('file_does_not_exist.txt', 'r') as file:
        print(file.read())
except:
    print("Unable to locate file")  
