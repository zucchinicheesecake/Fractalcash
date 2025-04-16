from src.utils.config import load_config
from src.fractalhash.fractalhash import FractalHash

if __name__ == '__main__':
    config = load_config()
    fh = FractalHash()
    print('FractalHash ready:', fh)
