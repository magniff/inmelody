import watch


ZeroOne = watch.Pred(lambda value: value in [0, 1])
String = watch.builtins.InstanceOf(str)
ZeroPositiveInteger = watch.Pred(
    lambda value: isinstance(value, int) and value >= 0
)
