"""
Step definitions for calculator feature.

TODO: Implement these step definitions to make the calculator.feature scenarios pass.

Expected implementation:
1. Create a Calculator class (in a calculator module or inline)
2. Implement basic operations: add, subtract, multiply, divide
3. Handle division by zero with a custom exception
4. Wire up the step definitions below to your implementation

Run tests with: uv run behave
"""

from behave import given, when, then


@given('I have a calculator')
def step_given_calculator(context):
    """Initialize a calculator instance."""
    raise NotImplementedError("TODO: Create calculator instance")


@when('I add {a:d} and {b:d}')
def step_when_add(context, a, b):
    """Perform addition operation."""
    raise NotImplementedError("TODO: Implement addition")


@when('I subtract {b:d} from {a:d}')
def step_when_subtract(context, a, b):
    """Perform subtraction operation."""
    raise NotImplementedError("TODO: Implement subtraction")


@when('I multiply {a:d} and {b:d}')
def step_when_multiply(context, a, b):
    """Perform multiplication operation."""
    raise NotImplementedError("TODO: Implement multiplication")


@when('I divide {a:d} by {b:d}')
def step_when_divide(context, a, b):
    """Perform division operation, catching errors if needed."""
    raise NotImplementedError("TODO: Implement division with error handling")


@then('the result should be {expected:f}')
def step_then_result_float(context, expected):
    """Verify result matches expected float value."""
    raise NotImplementedError("TODO: Verify float result")


@then('the result should be {expected:d}')
def step_then_result_int(context, expected):
    """Verify result matches expected integer value."""
    raise NotImplementedError("TODO: Verify integer result")


@then('it should raise a division by zero error')
def step_then_division_error(context):
    """Verify that a division by zero error was raised."""
    raise NotImplementedError("TODO: Verify division by zero error")
