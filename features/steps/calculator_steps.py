from behave import given, when, then
from calculator import Calculator, DivisionByZeroError


@given('I have a calculator')
def step_given_calculator(context):
    """Initialize the merged calculator implementation."""
    context.calculator = Calculator()
    assert context.calculator is not None


@when('I add {a:d} and {b:d}')
def step_when_add(context, a, b):
    """Perform addition operation."""
    context.result = context.calculator.add(a, b)


@when('I subtract {b:d} from {a:d}')
def step_when_subtract(context, a, b):
    """Perform subtraction operation."""
    context.result = context.calculator.subtract(a, b)


@when('I multiply {a:d} and {b:d}')
def step_when_multiply(context, a, b):
    """Perform multiplication operation."""
    context.result = context.calculator.multiply(a, b)


@when('I divide {a:d} by {b:d}')
def step_when_divide(context, a, b):
    """Perform division operation, catching errors if needed."""
    try:
        context.result = context.calculator.divide(a, b)
        context.error = None
    except DivisionByZeroError as e:
        context.error = e
        context.result = None


@then('the result should be {expected:f}')
def step_then_result_float(context, expected):
    """Verify result matches expected float value."""
    assert context.result is not None, "Expected a result but got None"
    assert abs(context.result - expected) < 0.0001, \
        f"Expected {expected}, got {context.result}"


@then('the result should be {expected:d}')
def step_then_result_int(context, expected):
    """Verify result matches expected integer value."""
    assert context.result is not None, "Expected a result but got None"
    assert context.result == expected, \
        f"Expected {expected}, got {context.result}"


@then('it should raise a division by zero error')
def step_then_division_error(context):
    """Verify that a division by zero error was raised."""
    assert context.error is not None, "Expected an error but none was raised"
    assert isinstance(context.error, DivisionByZeroError), \
        f"Expected DivisionByZeroError, got {type(context.error).__name__}"
