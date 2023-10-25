def password_validator(value: str) -> str:
    MIN_LENGTH = 8
    MIN_LOWER = 1
    MIN_UPPER = 1
    MIN_NUMERIC = 1
    MIN_SPECIAL = 1

    if len(value) < MIN_LENGTH:
        raise ValueError(
            f"Password must be at least {MIN_LENGTH} characters long"
        )

    if len(list(filter(lambda x: x.islower(), value))) < MIN_LOWER:
        raise ValueError(
            f"Password should contain at least {MIN_LOWER} lowercase character"
        )
    if len(list(filter(lambda x: x.isupper(), value))) < MIN_UPPER:
        raise ValueError(
            f"Password should contain at least {MIN_UPPER} uppercase character"
        )
    if len(list(filter(lambda x: x.isnumeric(), value))) < MIN_NUMERIC:
        raise ValueError(
            f"Password should contain at least {MIN_NUMERIC} numeric character"
        )
    if (
        len(
            list(filter(lambda x: not x.isnumeric() and not x.isalpha(), value))
        )
        < MIN_SPECIAL
    ):
        raise ValueError(
            f"Password should contain at least {MIN_SPECIAL} special character"
        )
    return value
