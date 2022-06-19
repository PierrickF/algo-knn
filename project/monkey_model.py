from utils import check_hexacolor


class Monkey:
    """A class describing monkeys."""

    def __init__(self, fur_color, size, weight, species=""):                # Initiate a monkey

        self.fur_color = fur_color                                          # Give the monkey four attributes
        self.size = size
        self.weight = weight
        self.species = species

        if not check_hexacolor(fur_color):                                  # Check the validity of fur_color
            raise ValueError("Fur color isn't a valid hexadecimal code.")

    def __str__(self):                                                      # Default method
        my_string = "{0}, {1:.2f}, {2:.2f}, {3}". format(self.fur_color, self.size, self.weight, self.species)
        return my_string

    def __repr__(self):                                                     # Default method
        my_string = "{0}, {1:.2f}, {2:.2f}, {3}".format(self.fur_color, self.size, self.weight, self.species)
        return my_string

    def compute_bmi(self):
        """Compute the BMI of a monkey,
        which is silly as they only eat healthy bananas."""
        return round(self.weight / (self.size ** 2), 2)
