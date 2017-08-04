import collectd

class MetricsUtil:

    _reserved_symbols = frozenset([' ', '='])

    @staticmethod
    def validate_nonempty(s, key):

        if not s:
            raise Exception('Value for key %s cannot be empty' % key)


    @staticmethod
    def validate_positive(v):

        if not v > 0:
            raise Exception('%s is not a positive float' % v)

    @staticmethod
    def validate_field(s):
        """
        Field must be string that does not contains '=' or ' '
        """

        if type(s) is not str:
            raise Exception('Field %s must be string type. Type is %s' % (s, type(s)))

        for reserved_symbol in MetricsUtil._reserved_symbols:
            if reserved_symbol in s:
                raise Exception('Field %s must not contain reserved symbol %s' %
                                (s, reserved_symbol))

    @staticmethod
    def validate_type(data, types):
        """
        Validate type are defined in types.db and matching data values
        """

        # Verify type is defined in types.db
        if data.type not in types:
            raise Exception('Do not know how to handle type %s. Do you have all your types.db files'
                            ' configured?' % data.type)

        # Verify values conform to the type defined
        if len(data.values) != len(types[data.type]):
            raise Exception('Number values %s differ from types defined for %s' %
                            (data.values, data.type))

    @staticmethod
    def fail_with_recoverable_exception(msg, batch, e):
        """
        Warn about exception and raise RecoverableException
        """

        collectd.warning(msg + ': %s. Retrying sending batch %s' % (batch, e.message))
        raise RecoverableException(e)

    @staticmethod
    def fail_with_unrecoverable_exception(msg, batch, e):
        """
        Error about exception and pass through exception
        """

        collectd.error(msg + ': %s. Dropping batch %s' % (batch, e.message))
        raise e


class RecoverableException(Exception):
    """
    Exception that are recoverable.
    """

    pass
