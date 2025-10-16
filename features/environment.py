def before_all(context):
    """
    Runs once before all features.
    Use this to set up any global configuration or resources.
    """
    pass


def before_feature(context, feature):
    """
    Runs before each feature.
    """
    pass


def before_scenario(context, scenario):
    """
    Runs before each scenario.
    Use this to set up test data or reset state.
    """
    pass


def after_scenario(context, scenario):
    """
    Runs after each scenario.
    Use this to clean up test data.
    """
    pass


def after_feature(context, feature):
    """
    Runs after each feature.
    """
    pass


def after_all(context):
    """
    Runs once after all features.
    Use this to tear down global resources.
    """
    pass
