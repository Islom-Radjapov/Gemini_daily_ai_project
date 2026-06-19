import inspect
import sys
import traceback

class TestFailure(Exception):
    """
    Custom exception raised when an assertion fails within a test method.
    This helps differentiate assertion failures from unexpected errors.
    """
    pass

class TestCase:
    """
    Base class for creating test cases.
    Users should inherit from this class to define their test suites.
    It provides common assertion methods and hooks for setup/teardown.
    """
    def setup(self):
        """
        Method called before each test method is run.
        Override this method in your test class to perform setup actions
        (e.g., initializing variables, opening resources).
        """
        pass

    def teardown(self):
        """
        Method called after each test method is run.
        Override this method in your test class to perform teardown actions
        (e.g., cleaning up resources, resetting state).
        This method is guaranteed to run, even if the test method fails or errors.
        """
        pass

    # --- Assertion Methods ---

    def assert_equal(self, actual, expected, message=""):
        """
        Asserts that two values are equal.
        If they are not equal, a TestFailure is raised.
        """
        if actual != expected:
            msg = f"Assertion Failed: {actual!r} != {expected!r}"
            if message:
                msg = f"{message}\n{msg}"
            raise TestFailure(msg)

    def assert_true(self, condition, message=""):
        """
        Asserts that a given condition is true.
        If the condition is false, a TestFailure is raised.
        """
        if not condition:
            msg = f"Assertion Failed: {condition!r} is not True"
            if message:
                msg = f"{message}\n{msg}"
            raise TestFailure(msg)

    def assert_false(self, condition, message=""):
        """
        Asserts that a given condition is false.
        If the condition is true, a TestFailure is raised.
        """
        if condition:
            msg = f"Assertion Failed: {condition!r} is not False"
            if message:
                msg = f"{message}\n{msg}"
            raise TestFailure(msg)

    def assert_is_none(self, obj, message=""):
        """
        Asserts that an object is None.
        If the object is not None, a TestFailure is raised.
        """
        if obj is not None:
            msg = f"Assertion Failed: {obj!r} is not None"
            if message:
                msg = f"{message}\n{msg}"
            raise TestFailure(msg)

    def assert_is_not_none(self, obj, message=""):
        """
        Asserts that an object is not None.
        If the object is None, a TestFailure is raised.
        """
        if obj is None:
            msg = f"Assertion Failed: {obj!r} is None"
            if message:
                msg = f"{message}\n{msg}"
            raise TestFailure(msg)

    def assert_raises(self, expected_exception, callable_obj, *args, **kwargs):
        """
        Asserts that a specific exception is raised when `callable_obj` is called.
        `callable_obj` will be called with `*args` and `**kwargs`.
        If the expected exception is not raised, or a different exception is raised,
        a TestFailure is raised.
        """
        try:
            callable_obj(*args, **kwargs)
            raise TestFailure(f"Assertion Failed: Expected {expected_exception.__name__} was not raised.")
        except expected_exception as e:
            # The expected exception was raised, which is good.
            pass
        except Exception as e:
            # A different exception was raised.
            raise TestFailure(f"Assertion Failed: Expected {expected_exception.__name__} but got {type(e).__name__}.")

class TestRunner:
    """
    Discovers, runs, and reports on test methods found in TestCase subclasses.
    """
    def __init__(self):
        """Initializes the TestRunner with empty results."""
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "total": 0,
            "failures": [],       # Stores details for failed assertions
            "errors_detail": []   # Stores details for unexpected errors
        }

    def run(self, test_classes):
        """
        Runs all test methods found in the provided list of test classes.
        Prints progress and a summary report.
        """
        print("Running tests...\n")
        for test_class in test_classes:
            self._run_test_class(test_class)
        self._print_summary()
        return self.results

    def _run_test_class(self, test_class):
        """Runs all test methods within a single TestCase subclass."""
        test_methods = self._discover_test_methods(test_class)
        if not test_methods:
            print(f"  No test methods found in {test_class.__name__} (methods must start with 'test_')")
            return

        print(f"  Running tests from {test_class.__name__}")
        for method_name in test_methods:
            self.results["total"] += 1
            test_instance = test_class() # Create a new instance for each test method to ensure isolation

            try:
                # Run setup method before each test
                test_instance.setup()
                # Run the actual test method
                getattr(test_instance, method_name)()
                print(f"    [PASS] {method_name}")
                self.results["passed"] += 1
            except TestFailure as e:
                # An assertion failed in the test method
                print(f"    [FAIL] {method_name}")
                self.results["failed"] += 1
                self.results["failures"].append({
                    "test_class": test_class.__name__,
                    "test_method": method_name,
                    "message": str(e)
                })
            except Exception as e:
                # An unexpected error occurred during test execution
                print(f"    [ERROR] {method_name}")
                self.results["errors"] += 1
                self.results["errors_detail"].append({
                    "test_class": test_class.__name__,
                    "test_method": method_name,
                    "exception": type(e).__name__,
                    "message": str(e),
                    "traceback": traceback.format_exc() # Capture full traceback for debugging
                })
            finally:
                # Run teardown method after each test, regardless of outcome
                try:
                    test_instance.teardown()
                except Exception as e:
                    # If teardown itself fails, it's a critical error
                    print(f"      [CRITICAL ERROR] Teardown failed for {method_name}: {e}")
                    self.results["errors"] += 1
                    self.results["errors_detail"].append({
                        "test_class": test_class.__name__,
                        "test_method": method_name + " (teardown)",
                        "exception": type(e).__name__,
                        "message": str(e),
                        "traceback": traceback.format_exc()
                    })

    def _discover_test_methods(self, test_class):
        """
        Discovers methods within a TestCase subclass that start with 'test_'.
        These methods are considered test methods to be executed by the runner.
        """
        methods = []
        for name in dir(test_class):
            # Check if it starts with 'test_', is callable, and is defined directly on the class
            # or an instance, not just inherited from object or TestCase base methods.
            # Using inspect.isfunction on the class attribute ensures it's a method.
            if name.startswith('test_') and inspect.isfunction(getattr(test_class, name)):
                # Further ensure it's not a method defined in the base TestCase itself (if any were 'test_')
                # For this framework, TestCase has no 'test_' methods, so this check is sufficient.
                methods.append(name)
        return sorted(methods) # Sort for consistent test execution order

    def _print_summary(self):
        """Prints a comprehensive summary of the test results."""
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {self.results['total']}")
        print(f"Passed:      {self.results['passed']}")
        print(f"Failed:      {self.results['failed']}")
        print(f"Errors:      {self.results['errors']}")

        if self.results["failures"]:
            print("\n" + "-" * 50)
            print("FAILURES:")
            for failure in self.results["failures"]:
                print(f"  {failure['test_class']}.{failure['test_method']}:")
                print(f"    Message: {failure['message']}")
            print("-" * 50)

        if self.results["errors_detail"]:
            print("\n" + "-" * 50)
            print("ERRORS:")
            for error in self.results["errors_detail"]:
                print(f"  {error['test_class']}.{error['test_method']}:")
                print(f"    Exception: {error['exception']} - {error['message']}")
                print(f"    Traceback:\n{self._indent_traceback(error['traceback'])}")
            print("-" * 50)

        print("\n" + "=" * 50)
        if self.results["failed"] == 0 and self.results["errors"] == 0:
            print("ALL TESTS PASSED!")
        else:
            print("SOME TESTS FAILED OR ENCOUNTERED ERRORS!")
        print("=" * 50)

    def _indent_traceback(self, tb_string, indent="      "):
        """
        Helper method to indent a traceback string for better readability in output.
        """
        return "\n".join([indent + line for line in tb_string.splitlines()])