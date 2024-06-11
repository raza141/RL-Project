
class RewaredFunction:

    def __init__():
        pass

    def traditional_opportunity_cost(current_balance, initial_balance, max_steps, current_step):
    """
    Calculates opportunity cost based on traditional definition.

    Args:
        current_balance (float): The current account balance.
        initial_balance (float): The initial account balance.
        max_steps (int): The maximum number of steps (e.g., investment period).
        current_step (int): The current step in the investment period.

    Returns:
        float: The opportunity cost.
    """

    # Check for zero initial balance to avoid division by zero
    if initial_balance == 0:
        return 0

    # Calculate the potential return if invested elsewhere
    potential_return = (max_steps - current_step) * (current_balance - initial_balance) / initial_balance

    return potential_return



    def custom_opportunity_cost(current_balance, max_steps, current_step):
    """
    Calculates opportunity cost based on the custom definition.

    Args:
        current_balance (float): The current account balance.
        max_steps (int): The maximum number of steps (e.g., investment period).
        current_step (int): The current step in the investment period.

    Returns:
        float: The opportunity cost.
    """

    # Avoid division by zero
    if current_step == 0:
        return 0

    return current_balance * current_step / max_steps