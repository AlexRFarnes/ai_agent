import unittest

from functions.get_files_info import get_files_info


class TestCalculator(unittest.TestCase):
    def test_cwd(self):
        result = get_files_info("calculator", ".")
        # self.assertIn("pkg", result)
        print(result)

    def test_nested_directory(self):
        result = get_files_info("calculator", "pkg")
        # self.assertIn("calculator.py", result)
        print(result)

    def test_of_cwd_1(self):
        result = get_files_info("calculator", "/bin")
        # self.assertEqual(
        #     result,
        #     'Error: Cannot list "/bin" as it is outside the permitted working directory',
        # )
        print(result)

    def test_of_cwd_2(self):
        result = get_files_info("calculator", "../")
        # self.assertEqual(
        #     result,
        #     'Error: Cannot list "../" as it is outside the permitted working directory',
        # )
        print(result)


if __name__ == "__main__":
    unittest.main()
