"""Various utility functions."""

import inspect


def get_args(func):
    """Get a list of argument names for a function.

    This is a wrapper around inspect.getargspec/inspect.signature because
    getargspec got deprecated in Python 3.5 and signature isn't available on
    Python 2.

    :param func: The function to inspect.

    :return: A list of argument names.
    :rtype: list
    """
    if hasattr(inspect, 'signature'):
        params = inspect.signature(func).parameters.values()
        return [param.name for param in params
                if param.kind == param.POSITIONAL_OR_KEYWORD]
    else:
        return inspect.getargspec(func).args


def get_fixture_value(request, name):
    """Get the given fixture from the pytest request object.

    getfuncargvalue() is deprecated in pytest 3.0, so we need to use
    getfixturevalue() there.
    """
    try:
        getfixturevalue = request.getfixturevalue
    except AttributeError:
        getfixturevalue = request.getfuncargvalue
    return getfixturevalue(name)


def get_fixture_value_raw(request, name):
    """Set the given raw fixture value from the pytest request object.

    :note: Compatibility with pytest < 3.3.2
    """
    try:
        return request._fixture_values.get(name)
    except AttributeError:
        try:
            return request._funcargs.get(name)
        except AttributeError:
            pass


def set_fixture_value(request, name, value):
    """Set the given fixture value on the pytest request object.

    :note: Compatibility with pytest < 3.3.2
    """
    try:
        request._fixture_values[name] = value
    except AttributeError:
        try:
            request._funcargs[name] = value
        except AttributeError:
            pass


def get_request_fixture_defs(request):
    """Get the internal list of FixtureDefs cached into the given request object.

    Compatibility with pytest 3.0.
    """
    try:
        return request._fixture_defs
    except AttributeError:
        return getattr(request, "_fixturedefs", {})


def get_request_fixture_names(request):
    """Get list of fixture names for the given FixtureRequest.

    Get the internal and mutable list of fixture names in the enclosing scope of
    the given request object.

    Compatibility with pytest 3.0.
    """
    return request._pyfuncitem._fixtureinfo.names_closure


def get_closest_marker_args(node, mark_name):
    """In pytest 3.6 new API to access markers has been introduced and it deprecated
    MarkInfo objects.

    This function uses that API if it is available otherwise it uses MarkInfo objects.
    """
    try:
        return get_closest_marker_args_using_get_closest_marker(node, mark_name)
    except AttributeError:
        return get_closest_marker_args_using_mark_objects(node, mark_name)


def get_closest_marker_args_using_get_closest_marker(node, mark_name):
    """Recommended on pytest>=3.6"""
    marker = node.get_closest_marker(mark_name)
    return marker.args if marker else None


def get_closest_marker_args_using_mark_objects(node, mark_name):
    """Deprecated on pytest>=3.6"""
    marker = node.keywords._markers.get(mark_name)
    return (marker.args[0], marker.args[1]) if marker else None
