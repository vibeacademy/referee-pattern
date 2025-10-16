from behave import given, when, then


@given('I have a referee system')
def step_given_referee_system(context):
    context.referee_system = True
    assert context.referee_system is True


@when('I perform an action')
def step_when_perform_action(context):
    context.action_performed = True
    assert context.action_performed is True


@then('the result should be valid')
def step_then_result_valid(context):
    assert context.referee_system is True
    assert context.action_performed is True
