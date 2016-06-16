class BaseTest(object):
    def _raise_not_implemented(self, method_name):
        raise NotImplementedError(
            '%s must be implemented in %s' % (
                method_name, self.__class__.__name__
            )
        )

    def test_to_iso8601(self):
        self._raise_not_implemented('test_to_iso8601')

    def test_to_seconds(self):
        self._raise_not_implemented('test_to_seconds')

    def test_to_timedelta(self):
        self._raise_not_implemented('test_to_timedelta')

    def test_to_tuple(self):
        self._raise_not_implemented('test_to_tuple')
