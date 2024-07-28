# open(<FILE_NAME> <FILE_LOCATION>, <MODE>)
# Mode defines the action required

# 'r' -> Open & read (text format)
# 'rb' -> Open & read (binary format)
# 'r+' -> Open for reading & writing
# 'w' -> Open for writing (overwrite existing file)
# 'a' -> Open for editing or appending data
# add b for binary to any mode

# close() -> for closing the open file
# with open('file.txt', 'r') as file :  -> closes file automatically


with open('names.txt', mode ='r') as file :
    data = file.readline()
    print(data)


# Creating files
# overwrites to existing files for 'w'
# use 'a' to append 
#with open('newfile.txt','w') as file :
#try:
#    with open('newfile.txt','a') as file :
#        file.writelines(["\nThis is a new file created-2!","\nThis is another line to be added."])
#except FileExistsError as e:
#    print("ERROR", e)

# Read file
# read - prints as a string all characters
print("\nRead ")
try:
    with open('names.txt','r') as file :
        print(file.read())
except FileExistsError as e:
    print("ERROR", e)


# read(n) - prints till n number of characters
print("\nRead n characters. ")
try:
    with open('names.txt','r') as file :
        print(file.read(30))
except FileExistsError as e:
    print("ERROR", e)

# readline - prints only first line of text, can also take n as arguments for characters
print("\nReadLine")
try:
    with open('names.txt','r') as file :
        print(file.readline())
except FileExistsError as e:
    print("ERROR", e)

# readlines - reads entire contents of file and retuns as ordered list
print("\nReadLines")
try:
    with open('names.txt','r') as file :
        print(file.readlines())
except FileExistsError as e:
    print("ERROR", e)

print("\nTest")
with open('names.txt','r') as file :
    for x in file :
        print(x)

# Excercise

print("\nRead with the redundant print() calls deleted.")
f = open("petnames.txt", "r")
f_content = f.read()
f_content_list = f_content.split("\n")
print(f_content_list)
f.close()