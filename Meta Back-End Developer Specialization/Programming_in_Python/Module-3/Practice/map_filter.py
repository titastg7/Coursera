menu = ['espresso', 'latte', 'mocha', 'cappucino','cortado','americano']

def find_coffee(coffee) :
    if coffee[0]=='c' :
        return coffee

# Map
map_coffee = map(find_coffee, menu)
print("Using Map function")
print(map_coffee)
for x in map_coffee:
    print(x)

# Filter
filter_coffee = filter(find_coffee, menu)
print("Using Filter function")
print(filter_coffee)
for x in filter_coffee:
    print(x)