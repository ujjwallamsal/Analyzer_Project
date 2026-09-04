"""A small, well-written example file used to demonstrate the analyzer
on code that follows good practices (should report very few issues)."""


def calculate_average(numbers):
    """Return the average of a list of numbers."""
    total = 0
    for number in numbers:
        total = total + number
    return total / len(numbers)


class ShoppingCart:
    """A very small shopping cart example."""

    def __init__(self):
        self.items = []

    def add_item(self, item_name):
        self.items.append(item_name)
