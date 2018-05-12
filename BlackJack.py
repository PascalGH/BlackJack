def closest_21(number1, number2):
    # Determines which of 2 numbers is the closest to 21, without being over that number
    if number1 > 21:
        if number2 > 21:
            # Both numbers are over 21, no one wins
            return(0)
        else:
            # Number 2 wins because number one is over 21, and number 2 not
            return(number2)
    else:
        if number2 > 21:
            # Number 1 wins because number 2 is over 21, and number 1 not
            return number1
        else:
            # Both numbers are eligible, the biggest wins as it is the closest to21
            return max(number1, number2)


def yes_no(question):
    # Gets a yes or no anser to a question
    answer = '*'
    while answer.lower() != 'y' and answer.lower() != 'n':
        answer = input(question + ' (y / n)')
        if answer.lower() != 'y' and answer.lower() != 'n':
            print('Please answer by y or n')
    return(answer.lower())