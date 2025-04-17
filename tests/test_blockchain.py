import pytest
from blockchain import Blockchain

@pytest.fixture
def sample_blockchain():
    bc = Blockchain()
    if hasattr(bc, 'create_genesis_block'):
        bc.create_genesis_block()
    return bc

def test_blockchain_initialization(sample_blockchain):
    assert isinstance(sample_blockchain.chain, list)
    assert len(sample_blockchain.chain) >= 1

def test_add_block(sample_blockchain):
    initial_length = len(sample_blockchain.chain)
    sample_blockchain.add_block('Test Data')
    assert len(sample_blockchain.chain) == initial_length + 1
    assert sample_blockchain.chain[-1].data == 'Test Data'
