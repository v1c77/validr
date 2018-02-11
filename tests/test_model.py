import pytest
from validr import T, modelclass, fields, asdict, Compiler, Invalid


@modelclass
class MyModel:

    id = T.int.min(0)


@modelclass(compiler=Compiler())
class MyModelX:

    id = T.int.min(0)

    def __eq__(self, other):
        return id(self) == id(other)


class User(MyModel):

    id = T.int.min(100).default(100)
    name = T.str


def test_model():
    with pytest.raises(Invalid):
        User(name='test', xxx=123)
    user = User(name='test')
    assert user.id == 100
    assert user.name == 'test'
    with pytest.raises(Invalid):
        user.id = -1
    assert repr(user) == "User(id=100, name='test')"


def test_custom_method():
    m1 = MyModel(id=1)
    m2 = MyModel(id=1)
    assert m1 == m2
    x1 = MyModelX(id=1)
    x2 = MyModelX(id=1)
    assert x1 != x2


def test_repr():
    assert repr(MyModel) == 'MyModel<id>'
    assert repr(MyModelX) == 'MyModelX<id>'
    assert repr(User) == 'User<id, name>'


def test_schema():
    assert T(MyModel) == T.dict(
        id=T.int.min(0),
    )
    assert T(User) == T.dict(
        id=T.int.min(100).default(100),
        name=T.str,
    )


def test_fields():
    assert fields(User) == {'id', 'name'}
    user = User(id=123, name='test')
    assert fields(user) == {'id', 'name'}


def test_asdict():
    user = User(id=123, name='test')
    assert asdict(user) == {'id': 123, 'name': 'test'}
    assert asdict(user, keys=['name']) == {'name': 'test'}


def test_slice():
    assert User['id'] == T.dict(id=T.int.min(100).default(100))
    assert User['id', 'name'] == T.dict(
        id=T.int.min(100).default(100),
        name=T.str
    )
