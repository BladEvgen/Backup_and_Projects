# task 1
validname = "user"

validpassword = "qwerty"

username = input("Enter your username: ")
userpassword = input("Enter your password: ")

if username != validname or userpassword != validpassword:
    print("Invalid username or password")
else:
    print("Authentication completed welcome " + username)

# task 2

print("\n\n================================\n\n")

currUSD = 420.0

currEUR = 510.0

currRUB = 5.8

currKZT = float(input("Please enter KZT value: "))

change = int(input("Please enter which currency do you need:\n1. USD\n2. EUR\n3. RUB\n"))

match change:
    case 1:
        print(currKZT/currUSD)
    case 2:
        print(currKZT/currEUR)
    case 3:
        print(currKZT/currRUB)
    case _:
        print("Invalid choice")


#task 3 

number = [i for i in range(1001)]
squares = [num**2 for num in number]

print(f'Array: {number}')
print(f'Array of squares: {squares}')