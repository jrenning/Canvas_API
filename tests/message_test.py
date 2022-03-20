import email
from pyexpat.errors import messages
from src.text_message import split_messages, email_message
import pytest 

@pytest.fixture
def messages():
    return split_messages(email_message)



def test_split_message_length(messages):

    
    for message in messages:
        assert len(message) < 140
        
def test_split_message_integrity(messages):
    
    length = 0
    
    for message in messages:
        length += len(message)
    
    print(f'Length of the original message is {len(email_message)} the length of the new ones is {length}')
    assert length == len(email_message)
    
def test_good_splits(messages):
    splits = round(len(email_message) / 140)
    
    print(f'Good split number is {splits}, number of messages is {len(messages)}')
    assert splits  == len(messages)
    
        
