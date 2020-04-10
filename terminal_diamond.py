def wait_for_input():
    try:
        steps = int(input('Insert digit from 1 to 9: '))
    except ValueError:
        print('Incorrect character')
        wait_for_input()
    else:
        return steps


def make_diamond(steps):
    """
    Creates diamond brick in console
    """
    arr = list(range(1, steps + 1)) + list(range(steps - 1, 0, -1))
    for i in arr:
        rows = []
        dig = i - steps
        for j in arr:
            res = j + dig
            if res < 1:
                res = " "
            rows.append(res)
        print(*rows)


if __name__ == '__main__':
    make_diamond(wait_for_input())

