from typing import List, Callable


def is_valid_password(password: int) -> bool:
    password_string = str(password)

    is_six_digits = len(password_string) == 6
    has_two_in_a_row = any(l == r for l, r in zip(password_string[:-1], password_string[1:]))
    always_incrementing = all(r >= l for l, r in zip(password_string[:-1], password_string[1:]))

    return is_six_digits and has_two_in_a_row and always_incrementing


def is_valid_password_updated(password: int) -> bool:
    password_string = str(password)

    is_six_digits = len(password_string) == 6
    # Since this will only pass if always_incrementing is True, if we have 2 or more of the same char, they 
    # HAVE to be consecutive.
    digits = set(password_string)
    has_two_of_the_same = any(password_string.count(digit) == 2 for digit in digits)
    always_incrementing = all(r >= l for l, r in zip(password_string[:-1], password_string[1:]))

    return is_six_digits and has_two_of_the_same and always_incrementing


def find_valid_passwords_in_range(
    lowest_password: int, highest_password: int, validation_function: Callable[[int], bool]
) -> List[int]:

    return [
        password for password in range(lowest_password, highest_password + 1) 
        if validation_function(password)
    ]


if __name__ == '__main__':
    assert is_valid_password(111111)
    assert not is_valid_password(223450)
    assert not is_valid_password(123789)

    min_password = 145852
    max_password = 616942
    valid_passwords = find_valid_passwords_in_range(min_password, max_password, is_valid_password)
    print(f"There are {len(valid_passwords)} in the range {min_password} to {max_password} by the first set of rules.")

    assert is_valid_password_updated(112233)
    assert not is_valid_password_updated(123444)
    assert is_valid_password_updated(111122)

    valid_passwords = find_valid_passwords_in_range(min_password, max_password, is_valid_password_updated)
    print(f"There are {len(valid_passwords)} in the range {min_password} to {max_password} by the second set of rules.")
