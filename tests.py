import unittest

from functions.get_file_content import get_file_content


class TestCalculator(unittest.TestCase):
    def test(self):
        # result = get_file_content("calculator", "lorem.txt")
        # print("Result for file larger than 10,000 characters")
        # print(result)
        # print(len(result))
        # print("\n")

        result = get_file_content("calculator", "main.py")
        print("Result for calculator/main.py")
        print(result)
        print("\n")

        result = get_file_content("calculator", "pkg/calculator.py")
        print("Result for calculator/pkg/calculator.py")
        print(result)
        print("\n")

        result = get_file_content("calculator", "/bin/cat")
        print("Result for /bin/cat")
        print(result)
        print("\n")


if __name__ == "__main__":
    unittest.main()
