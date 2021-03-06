from validr import Compiler, T

from ..helper import expect_position
from . import case


class User:

    def __init__(self, userid):
        self.userid = userid


@case({
    T.dict(userid=T.int): [
        ({'userid': 1}, {'userid': 1}),
        (User(1), {'userid': 1}),
        ({'userid': 1, 'extra': 'xxx'}, {'userid': 1}),
    ],
    T.dict(userid=T.int).optional: {
        'valid': [
            None,
        ],
        'invalid': [
            {},
            {'extra': 1}
        ]
    },
    T.dict: {
        'valid': [
            {},
            {'key': 'value'},
        ],
        'invalid': [
            None,
            123,
        ]
    }
})
def test_dict():
    pass


compiler = Compiler()


@expect_position('key[0].key')
def test_dict_error_position():
    validate = compiler.compile(T.dict(key=T.list(T.dict(key=T.int))))
    validate({
        'key': [
            {'key': 'x'}
        ]
    })
