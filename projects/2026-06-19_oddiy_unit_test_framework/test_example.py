from micro_test import TestCase

# A simple example function that we might want to test
def add_numbers(a, b):
    return a + b

def divide_numbers(a, b):
    return a / b

class ExampleMathTests(TestCase):
    """
    A collection of unit tests for basic mathematical operations
    using the PyMiniTest framework.
    """
    def setup(self):
        """
        This method runs before each test_ method in this class.
        It's useful for initializing common resources or variables.
        """
        self.num1 = 10
        self.num2 = 5
        # print(f"  [DEBUG] Setup for a test in {self.__class__.__name__}")

    def teardown(self):
        """
        This method runs after each test_ method in this class,
        even if the test failed or caused an error.
        It's useful for cleaning up resources.
        """
        self.num1 = None
        self.num2 = None
        # print(f"  [DEBUG] Teardown for a test in {self.__class__.__name__}")

    def test_addition_of_positive_numbers(self):
        """Tests the addition of two positive numbers."""
        self.assert_equal(add_numbers(self.num1, self.num2), 15, "10 + 5 should be 15")
        self.assert_equal(add_numbers(1, 1), 2)

    def test_subtraction_of_numbers(self):
        """Tests the subtraction operation."""
        self.assert_equal(self.num1 - self.num2, 5)

    def test_multiplication_of_numbers(self):
        """Tests the multiplication operation."""
        self.assert_equal(self.num1 * self.num2, 50)

    def test_division_of_numbers(self):
        """Tests the division operation."""
        self.assert_equal(divide_numbers(self.num1, self.num2), 2.0)
        self.assert_raises(ZeroDivisionError, divide_numbers, 10, 0, "Dividing by zero should raise ZeroDivisionError")

    def test_assert_true_condition(self):
        """Tests the assert_true method."""
        self.assert_true(self.num1 > self.num2, "10 should be greater than 5")
        self.assert_true(True)

    def test_assert_false_condition(self):
        """Tests the assert_false method."""
        self.assert_false(self.num1 < self.num2, "10 should not be less than 5")
        self.assert_false(False)

    def test_assert_is_none_and_not_none(self):
        """Tests assert_is_none and assert_is_not_none methods."""
        x = None
        y = "some string"
        self.assert_is_none(x, "x should be None")
        self.assert_is_not_none(y, "y should not be None")

    # --- Examples of tests that will fail or error ---

    def test_deliberately_failing_assertion(self):
        """
        This test is designed to fail to demonstrate failure reporting.
        """
        self.assert_equal(add_numbers(self.num1, self.num2), 20, "This assertion should fail (10+5 is not 20)")

    def test_causing_an_unexpected_runtime_error(self):
        """
        This test is designed to cause an unexpected Python error
        to demonstrate error reporting.
        """
        my_list = [1, 2, 3]
        # Trying to access an out-of-bounds index will raise an IndexError
        _ = my_list[3] # This will cause an IndexError

class AnotherExampleTests(TestCase):
    """
    Another set of tests to demonstrate that PyMiniTest can discover
    and run tests from multiple TestCase classes.
    """
    def test_string_equality(self):
        """Tests basic string equality."""
        self.assert_equal("hello " + "world", "hello world")

    def test_list_length_check(self):
        """Tests the length of a list."""
        self.assert_equal(len([10, 20, 30, 40]), 4)

    def test_failing_string_comparison(self):
        """Another failing test from a different class."""
        self.assert_equal("python", "Python", "String comparison should be case-sensitive")