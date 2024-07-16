import pytest
def myFunction(parameter): #replace with function imported from file
    pass

print('_')
print('Starting tests...')

@pytest.mark.parametrize('data, expected', [
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None),
    (None,None)
    ]) #replace with test data

def test_myFunction(data, expected):
    assert myFunction(data) == expected #replace with function imported from file