"""Example module with functions to say hello and goodbye."""

from __future__ import annotations


def hello(name: str = "") -> str:
    """Say hello.

    Parameters
    ----------
    name
        Who to say hello to.

    Returns
    -------
    str
        Greeting.

    Notes
    -----
    See also: [`goodbye`][TRIPs.hello.goodbye]

    Examples
    --------
    >>> from example_project.hello import hello
    >>> hello("world")
    'Hello, world!'
    """
    greeting = "Hello"
    if len(name) > 0:
        greeting += ", " + name
    return greeting + "!"


def goodbye(name: str = "") -> str:
    """Say goodbye.

    Parameters
    ----------
    name
        Who to say goodbye to.

    Returns
    -------
    str
        Farewell.

    Notes
    -----
    See also: [`hello`][TRIPs.hello.hello]

    Examples
    --------
    >>> from example_project.hello import goodbye
    >>> goodbye("world")
    'Goodbye, world!'
    """
    farewell = "Goodbye"
    if len(name) > 0:
        farewell += ", " + name
    return farewell + "!"


def some_math(a: float, b: float) -> float:
    """Computes $\\frac{a}{b}$

    Parameters
    ----------
    a
        Numerator
    b
        Denominator

    Returns
    -------
    int
        Quotient
    """
    return a / b


if __name__ == "__main__":  # pragma: no cover
    print(hello("world"))
    print(goodbye("world"))
