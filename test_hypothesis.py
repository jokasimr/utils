from hypothesis import given, example, strategies as st

from utils import flatten

any_atom = st.floats() | st.booleans() | \
    st.integers() | st.none() | st.characters() | \
    st.text()

extend_into_iterable = lambda x: st.lists(x) | st.tuples(x) | x

any_atoms_in_nested_tuple_or_list = st.recursive(any_atom, extend_into_iterable)

def is_any_atom(e):
    te=type(e)
    return te==bool or te==float or te==str or te==int or e==None

@given(any_atoms_in_nested_tuple_or_list)
def test_flatten_any_atoms_nested(iterable):
    for e in flatten(iterable):
        assert is_any_atom(e)

