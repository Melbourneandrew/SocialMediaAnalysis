# 1. Prompt user for a 32 bit unsigned binary number
# 2. Convert the binary to decimal
# 3. Print the decimal number
# 4. Repeat steps 1-3 until user enters 0

# Initialize variables
binary = 1

# Prompt user for 32 bit unsigned binary number
while binary != 0:
    binary = int(input("Enter a 32 bit unsigned binary number: "))
    decimal = 0
    i = 0

    # Convert the binary to decimal
    while binary != 0:
        remainder = binary % 10
        binary = binary // 10
        decimal = decimal + remainder * pow(2, i)
        i += 1

    # Print the decimal number
    print("The decimal number is", decimal)