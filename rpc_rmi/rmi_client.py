import random
import logging
import sys
import Pyro5.api

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

class SciCalculatorClient:
    def __init__(self) -> None:
        # use name server object lookup uri shortcut
        self.SciCalculator = Pyro5.api.Proxy("PYRONAME:SciCalculator")

    
    def test_calc(self):
        def test_bin():
            rand_op = random.choice(AV_BIN_OPS)
            rand_operands = [random.randint(0, 100), random.randint(0, 100)]
            res = self.SciCalculator.calc(rand_op, rand_operands)
            logger.info(f'{rand_op} {rand_operands}: {res}')

        def test_un():
            rand_op = random.choice(AV_UNA_OPS)
            rand_operand = [random.randint(0, 100)]
            res = self.SciCalculator.calc(rand_op, rand_operand)
            logger.info(f'{rand_op} {rand_operand}: {res}')
        
        for _ in range(100):
            try:
                random.choice((test_un, test_bin,))()
            except Exception as e:
                logger.error(f'Err: {e}')


if __name__ == '__main__':
    calc = SciCalculatorClient()
    calc.test_calc()
    input('[PRESS ENTER]')