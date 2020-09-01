import unittest
import genPrime


def is_prime_naive(n):
    if n == 2:
        return True
    if n & 1:
        end = n // 2
        for i in range(3, end, 2):
            if n % i == 0:
                return False
        return True
    return False


class TestGenPrime(unittest.TestCase):
    @unittest.skip("skipping")
    def test_exp(self):
        bases = 100
        exponents = 100
        modulos = 100
        print('\nTesting \'exp\'')
        for b in range(bases):
            for e in range(exponents):
                for m in range(1, modulos):
                    print(f'\r{b} {e} {m}', end='')
                    self.assertEqual(genPrime.exp(b, e, m), pow(b, e, m))
        print()


    def test_is_prime(self):
        num_tests = 5000
        print('\nTesting \'is_prime\'')
        for n in range(2, num_tests):
            print(f'\r{n + 1}/{num_tests}', end='')
            self.assertEqual(is_prime_naive(n), genPrime.is_prime(n))
        print()


    def test_generate_prime(self):
        self.assertRaises(TypeError, genPrime.generate_prime, 0)
        self.assertRaises(TypeError, genPrime.generate_prime, 1)
        num_tests = 2000
        max_k = 13
        errors = 0
        print('\nTesting \'generate_prime\'')
        for k in range(2, max_k):
            for n in range(num_tests):
                test_prime = genPrime.generate_prime(k)
                print(f'\rk = {k} {n + 1}/{num_tests} {test_prime}', end='')
                try:
                    self.assertTrue(is_prime_naive(test_prime))
                except TypeError:
                    errors += 1
                self.assertEqual(test_prime.bit_length(), k)
        print('\nNum errors:', errors)
        print()


if __name__ == '__main__':
    unittest.main(failfast=True)
