from pdb import set_trace


def check_input():
    s = None
    while not isinstance(s, int):
        s = input("Please enter the index of the number you choose...")
        if s == 'a':
            print('Not a!')
        elif s == 'b':
            print('Not b!')
        else:
            try:
                s = int(s)
            except ValueError or TypeError:
                continue
    return s


def main():
    num = check_input()
    set_trace()
    print(num)


if __name__ == '__main__':
    main()
