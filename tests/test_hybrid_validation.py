import pytest
from validator.consensus import HybridValidator

class BlockFactory:
    @staticmethod
    def create_valid_block():
        return type('Block', (), {"data": "valid"})
    
    @staticmethod
    def create_malicious_block():
        return type('Block', (), {"data": "malicious"})

def test_hybrid_validation():
    validator = HybridValidator()
    assert validator.validate_block(BlockFactory.create_valid_block())
    with pytest.raises(ValueError):
        validator.validate_block(BlockFactory.create_malicious_block())
