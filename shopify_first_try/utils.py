def IsId(object_to_check):
    return isinstance(object_to_check, int) or isinstance(object_to_check, str)


def getObject(object_type, the_object):
    if the_object is None:
        return None
    elif IsId(the_object):
        return object_type.selectById(the_object)
    else:
        return the_object
