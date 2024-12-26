import pytest
#import model

@pytest.fixture()
def some_data():
    """Return answer to ultimate question."""
    return 42

def test_some_data(some_data):
    """Use fixture return value in a test."""
    assert some_data == 42

@pytest.fixture(scope='module')
async def opensearch_client() -> AsyncGenerator[Opensearch, None]:
    client = get_es().client()
    yield client
    await client.close()

@pytest.mark.parametrize("a, b, expected", [
    (4, 2, 2),
    (9, 3, 3),
    (15, 3, 3)
])
def test_add(a, b, expected):
    result = add(a, b)
    assert result == expected


def test_zero():
    try:
        add(a:4, b:5)
    except ValueError as e:
        #print(e)
        assert str(e) == 'div by zero'

if __name__ == '__main__':
    pytest.main()

# file_path = 'users.json'
# data = model.Open(file_path).read()
# book = model.TelephoneBook(data)
# test_contact = model.Contact(book["01ff6bf4-5445-45f7-82ba-657a1fc78468"])
# print(test_contact.full_name)
# print(book.show_contacts())