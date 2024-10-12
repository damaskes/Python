def wait_for_input():
    """
    Waits for a valid user input (an integer between 1 and 9).

    Returns:
        int: A valid input from the user.
    """
    while True:
        try:
            steps = int(input('Insert a digit from 1 to 9: '))
            if not (1 <= steps <= 9):
                print('Number must be between 1 and 9')
                continue
            return steps
        except ValueError:
            print('Incorrect character. Please enter an integer.')


def make_diamond():
    """
    Creates and displays a diamond shape in the console based on user input.

    The diamond is constructed using numbers where the maximum number is
    determined by the user's input. The diamond will expand up to that
    number and then contract back to 1.
    """
    steps = wait_for_input()  # Get user input for the number of steps
    diamond_pattern = list(range(1, steps + 1)) + list(range(steps - 1, 0, -1))  # Create the diamond pattern

    for i in diamond_pattern:
        rows = []
        # Calculate the offset for the current row
        offset = i - steps
        for j in diamond_pattern:
            # Adjust value based on the offset, fill empty spaces with a space character
            value = j + offset
            if value < 1:
                value = " "  # Fill with space for empty positions
            rows.append(value)
        # Print the row with space separation
        print(*rows)


if __name__ == '__main__':
    make_diamond()  # Run the diamond creation process


