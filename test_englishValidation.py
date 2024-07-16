import pytest
import textValidator

print('_')
print('Starting tests...')

@pytest.mark.parametrize('data, expected', [
    ('savage','SAVAGE'),
    ('HAPPY','HAPPY'),
    ('HAPPY BIRTHDAY MR SAVAGE','HAPPY BIRTHDAY MR SAVAGE'),
    ('Happy Birthday, Mr Savage!','HAPPY BIRTHDAY, MR SAVAGE!'),
    ('Happy Birthday, Mr Savage 🎉!','HAPPY BIRTHDAY, MR SAVAGE !'),
    ('',False),
    ('عيد ميلاد سعيد',False),
    ('Nous avons fêté l\'anniversaire de M. Savage.','NOUS AVONS FTÉ L\'ANNIVERSAIRE DE M. SAVAGE.'),
    ('Nous avons célébré l\'anniversaire de M. Savage.','NOUS AVONS CÉLÉBRÉ L\'ANNIVERSAIRE DE M. SAVAGE.'),
    (' jsavage@saintolaves.net','JSAVAGE@SAINTOLAVES.NET'),
    ('\#1 Mr Savage','1 MR SAVAGE'),
    ('.... .- .--. .--. -.--','.... .- .--. .--. -.--'),
    ('\"Happy Birthday, Mr Savage\"','\"HAPPY BIRTHDAY, MR SAVAGE\"'),
    ('\'Happy Birthday, Mr Savage\'','\'HAPPY BIRTHDAY, MR SAVAGE\''),
    ('+447596283679','+447596283679'),
    ('   ',False),
    ('Happy\nBirthday\nMr\nSavage','HAPPY BIRTHDAY MR SAVAGE'),
    ('\n',False),
    ('\#J\nSA\#V\n\#','J SAV'),
    ('عيد ميلاد\n سعيد',False)
    ]) 

def test_validateEnglish(data, expected):
    assert textValidator.validateEnglish(data) == expected