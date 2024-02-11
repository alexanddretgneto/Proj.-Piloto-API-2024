from django.test import TestCase

# Crie seus testes aqui.
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Executa uma vez para configurar dados não modificados para todos os métodos da classe.")
        pass

    def setUp(self):
        print("setUp: Executa uma vez para cada método de teste para configurar dados limpos.")
        pass

    def test_false_is_false(self):
        print("Método: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Método: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Método: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
