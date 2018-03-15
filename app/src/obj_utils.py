
def call_if_obj_has_method_or_default(obj, name, default):
    op = getattr(obj, name, None)
    if callable(op):
        return op()
    else:
        return default