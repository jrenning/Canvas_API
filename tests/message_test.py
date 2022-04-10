
from src import text_message 
import pytest 

@pytest.fixture
def messages():
    return text_message.split_messages(text_message.email_message)



def test_split_message_length(messages):

    
    for message in messages:
        assert len(message) < 140
        
def test_split_message_integrity(messages):
    
    length = 0
    
    for message in messages:
        length += len(message)
    
    print(f'Length of the original message is {len(text_message.email_message)} the length of the new ones is {length}')
    # account fpr removal of last newline
    assert length == len(text_message.email_message) - 1
    
def test_good_splits(messages):
    splits = round(len(text_message.email_message) / 140)
    # not always possible so add 1 for testing
    good_splits = splits + 1
    
    print(f'Best splits = {splits}, good split number is {good_splits}, number of messages is {len(messages)}')
    assert good_splits  == len(messages)
    
        
