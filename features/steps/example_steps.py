from behave import given, when, then
from referee import Referee, Action
from referee.rules import AlwaysValidRule


@given('I have a referee system')
def step_given_referee_system(context):
    """
    Initialize the referee system with a basic rule.
    Demonstrates the merged implementation combining:
    - Maintainability: Clean Rule abstraction
    - Performance: Efficient validation
    - Robustness: Error handling and validation
    """
    # Create a referee with an always-valid rule for this example
    rule = AlwaysValidRule()
    context.referee = Referee(rules=[rule])
    assert context.referee is not None
    assert context.referee.rule_count == 1


@when('I perform an action')
def step_when_perform_action(context):
    """
    Create and validate an action through the referee system.
    """
    # Create an action to validate
    context.action = Action(action_type='test_action', data={'test': True})
    assert context.action is not None

    # Validate the action through the referee
    context.result = context.referee.validate(context.action)
    assert context.result is not None


@then('the result should be valid')
def step_then_result_valid(context):
    """
    Verify that the validation result is valid.
    """
    assert context.result is not None
    assert context.result.is_valid is True
    assert len(context.result.messages) > 0
    assert context.result.metadata is not None
    assert context.result.metadata['rules_evaluated'] == 1
    assert context.result.metadata['rules_passed'] == 1
    assert context.result.metadata['rules_failed'] == 0
