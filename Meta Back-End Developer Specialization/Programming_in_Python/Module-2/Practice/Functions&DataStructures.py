# functions

def calculate_tax(bill, tax_rate) :
    return round((bill * tax_rate) /100.00, 2)

print('Total tax', calculate_tax(175.00,15))
print('Total tax', calculate_tax(164.33,22))


# List

list1 = [1,2,3,4]
list2 = ['A', 'B','C']
list3 = ['hello', 1, True, 40.22]
list4 = [1,2,[4,5,6],7,8]

print(*list1)
print(list1, sep=" ")

list1.insert(len(list1),5)
print("After insert ",list1, sep=" ")

list1.append(6)
print("After Append ",list1, sep=" ")

list1.extend([7,8,9])
print("After extend ",list1, sep=" ")

# it pops of the index 4
list1.pop(4)
print("After pop ",list1, sep=" ")

# it deletes index 3
del list1[3]
print("After delete ",list1, sep=" ")

# iterate
for x in list1 :
    print("Value :", x)


# Tuples

my_tuple = (1, 'strings', 4.5,True,'strings')
print("Tuple : ", my_tuple[1])
print("Tuple type : ", type(my_tuple))

print("Occurence Count of 'strings': ", my_tuple.count('strings'))
print("Index of '4.5': ", my_tuple.index(4.5))

# iterate tuple
for idx,x in enumerate(my_tuple) :
    print("Value in tuple:", idx,x)


# Sets
# unordered, removes duplicates

set_a = {1,2,3,4,5,5}

print("Set : ",set_a)

set_a.add(6)
print("After add to Set : ",set_a)

# remove number 5 not index
set_a.remove(5)
print("After remove to Set : ",set_a)

# discard is same as remove
set_a.discard(4)
print("After discard to Set : ",set_a)

set_b = {1,2,3,4,5}
set_c = {4,5,6,7,8}

print("After Union : ",set_b.union(set_c))
print("After Union using | : ",set_b|set_c)

print("After Intersection : ",set_b.intersection(set_c))
print("After Intersection using & : ",set_b & set_c)


print("After symmetric_difference : ",set_b.symmetric_difference(set_c))
print("After symmetric_difference using ^ : ",set_b ^ set_c)

# Dictionary
# no duplicate key

sample_dict = {1:'Coffee', 2:'Tea', 'A':'Juice'}

print("Dictionary : ",sample_dict['A'])

sample_dict[2] = 'Mint Tea'
print("Dictionary after change: ",sample_dict)

del sample_dict[1]
print("Dictionary after delete: ",sample_dict)

# dictionary iterate
my_d = {1:'Test', 'Name': 'Jim'}

# prints only keys
for x in my_d:
    print(x)

# prints both
for key,value in my_d.items():
    print(str(key) + ":" + value)


#Args & kwargs (ley word arguments)


def sum_of(*args) :
    sum=0
    for x in args :
         sum += x
    return sum

print("Def using args : " +str(sum_of(4,5,6)))


def sum_of_k(**kwargs) :
    sum=0
    for k,v in kwargs.items() :
         sum += v
    return round(sum)

print("Def using kwargs : " +str(sum_of_k(coffee=2.99, cake=4.55, juice=2.99)))
