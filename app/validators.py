RAISE_422 = "All parameter provided must be a positive integer."


def validate_all_inputs_as_integers(*args):
    """
  Validates if all input arguments can be converted to integers.
  Returns:
    True if all arguments can be converted to integers, False otherwise.
  """
    for arg in args:
        try:
            int(arg)
        except ValueError:
            return False
    return True
