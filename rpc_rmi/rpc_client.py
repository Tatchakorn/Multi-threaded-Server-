import random
import logging
import sys

import rpyc


LOG_FORMAT = '%(asctime)s %(threadName)-17s %(message)s'
logging.basicConfig(level=logging.INFO, 
                    format=LOG_FORMAT, 
                    handlers=[ 
                        logging.FileHandler(r'client.log'),
                        logging.StreamHandler(sys.stdout),
                        ])
logger = logging.getLogger(__name__)

AV_BIN_OPS = ('add', 'sub', 'mul', 'div', 'pow', 'log')
AV_UNA_OPS = ('sqrt', 'sin', 'cos')


def test_calc():
    client = rpyc.connect("localhost", 18861)

    def test_bin():
        rand_op = random.choice(AV_BIN_OPS)
        rand_operands = [random.randint(0, 1_000), random.randint(0, 100)]
        res = client.root.SciCalculator(rand_op, rand_operands)
        logger.info(f'{rand_op} {rand_operands}: {res}')

    def test_un():
        rand_op = random.choice(AV_UNA_OPS)
        rand_operand = [random.randint(0, 100)]
        res = client.root.SciCalculator(rand_op, rand_operand)
        logger.info(f'{rand_op} {rand_operand}: {res}')
    
    for _ in range(100):
        try:
            random.choice((test_un, test_bin,))()
        except Exception as e:
            logger.error(f'Err: {e}')

if __name__ == '__main__':
    test_calc()
    input('[ENTER]')