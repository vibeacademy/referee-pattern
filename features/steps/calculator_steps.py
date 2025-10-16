from behave import given, when, then


@given('I have a calculator')
def step_given_calculator(context):
    pass


@when('I add {a:d} and {b:d}')
def step_when_add(context, a, b):
    pass


@when('I subtract {b:d} from {a:d}')
def step_when_subtract(context, a, b):
    pass


@when('I multiply {a:d} and {b:d}')
def step_when_multiply(context, a, b):
    pass


@when('I divide {a:d} by {b:d}')
def step_when_divide(context, a, b):
    pass


@then('the result should be {expected:f}')
def step_then_result_float(context, expected):
    pass


@then('the result should be {expected:d}')
def step_then_result_int(context, expected):
    pass


@then('it should raise a division by zero error')
def step_then_division_error(context):
    pass
