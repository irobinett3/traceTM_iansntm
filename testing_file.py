import unittest
from main import read_tm_csv, trace_ntm 

class TestNTMs(unittest.TestCase):
    def test_aplus(self):
        # Test the NTM for the language "a*"
        machine_description, transitions = read_tm_csv('csv_tests/a_plus.csv')
        
        # Define various test cases to validate the NTM's behavior
        test_cases = [
            ("_", False),       # Empty string should be invalid
            ("a_", True),       # Single 'a' should be valid
            ("aaa_", True),     # Multiple 'a's should be valid
            ("b_", False),      # Invalid character 'b'
            ("aaab_", False),   # Invalid ending character
            ("ab_", False),     # Invalid sequence
            ("a_", True),       # Another valid case with a single 'a'
        ]
        
        # Loop through each test case and check if the result is as expected
        for input_string, expected in test_cases:
            tree, accepted, num_transitions = trace_ntm(machine_description, transitions, input_string)
            self.assertEqual(accepted, expected, f"Failed on input: {input_string}")


    def test_palindrome(self):
        # Test the NTM for palindrome strings
        machine_description, transitions = read_tm_csv('csv_tests/palindrome.csv')
        
        # Test cases for palindromes
        test_cases = [
            ("aba_", True),  # Palindrome
            ("abba_", True),  # Palindrome
            ("abc_", False),  # Not a palindrome
            ("_", True),  # Empty string is a palindrome
        ]
        
        # Check if the NTM accepts the correct palindrome strings
        for input_string, expected in test_cases:
            with self.subTest(input_string=input_string):
                _, accepted, _ = trace_ntm(machine_description, transitions, input_string)
                self.assertEqual(accepted, expected)
    
    def test_equal_01s(self):
        # Test the NTM for strings with equal numbers of 0's and 1's
        machine_description, transitions = read_tm_csv('csv_tests/equal_01s.csv')
        
        # Test cases to check if the NTM handles equal 0's and 1's correctly
        test_cases = [
            ("01_", True),  # Equal number of 0's and 1's
            ("0011_", True),  # Equal number of 0's and 1's
            ("0101_", True),  # Equal number of 0's and 1's
            ("000_", False),  # Unequal number of 0's and 1's
            ("_", True),  # Empty string (trivially equal)
        ]
        
        # Run tests to see if the NTM correctly accepts strings with equal 0's and 1's
        for input_string, expected in test_cases:
            with self.subTest(input_string=input_string):
                _, accepted, _ = trace_ntm(machine_description, transitions, input_string)
                self.assertEqual(accepted, expected)
    
    def test_abc_star(self):
        # Test the NTM for the language "a^n b^n c^m"
        machine_description, transitions = read_tm_csv('csv_tests/abc_star.csv')
        print(machine_description)
        print(transitions)

        # Test cases for the "a^n b^n c^m" language
        test_cases = [
            ("aabbcc_", True),  # Matches a^n b^n c^m
            ("aaabbccc_", True),  # Matches a^n b^n c^m
            ("ab_", True),  # Matches a^n b^n
            ("abcabc_", False),  # Interleaved characters should be rejected
            ("_", True),  # Empty string should be accepted
        ]
        
        # Check if the NTM accepts the correct strings for the language "a^n b^n c^m"
        for input_string, expected in test_cases:
            with self.subTest(input_string=input_string):
                _, accepted, _ = trace_ntm(machine_description, transitions, input_string)
                self.assertEqual(accepted, expected)

class TestDTMS(unittest.TestCase):
    def test_aplus(self):
        # Test the DTM for the language "a*"
        machine_description, transitions = read_tm_csv('csv_tests/a_plus_DTM.csv')
        
        # Define test cases for the DTM's behavior
        test_cases = [
            ("a_", True),       # Single 'a' should be valid
            ("aaa_", True),     # Multiple 'a's should be valid
            ("b_", False),      # Invalid character 'b'
            ("aaab_", False),   # Invalid ending character
            ("ab_", False),     # Invalid sequence
            ("a_", True),       # Another valid case with a single 'a'
        ]
        
        # Check if the DTM accepts the correct strings for the "a*" language
        for input_string, expected in test_cases:
            tree, accepted, num_transitions = trace_ntm(machine_description, transitions, input_string)
            self.assertEqual(accepted, expected, f"Failed on input: {input_string}")


    def test_palindrome(self):
        # Test the DTM for palindrome strings
        machine_description, transitions = read_tm_csv('csv_tests/palindrome_DTM.csv')
        
        # Test cases for palindromes
        test_cases = [
            ("aba_", True),  # Palindrome
            ("abba_", True),  # Palindrome
            ("abc_", False),  # Not a palindrome
            ("_", True),  # Empty string is a palindrome
        ]
        
        # Check if the DTM accepts the correct palindrome strings
        for input_string, expected in test_cases:
            with self.subTest(input_string=input_string):
                _, accepted, _ = trace_ntm(machine_description, transitions, input_string)
                self.assertEqual(accepted, expected)
    
    def test_equal_01s(self):
        # Test the DTM for strings with equal numbers of 0's and 1's
        machine_description, transitions = read_tm_csv('csv_tests/equal_01s_DTM.csv')
        
        # Test cases for equal 0's and 1's
        test_cases = [
            ("01_", True),  # Equal number of 0's and 1's
            ("0011_", True),  # Equal number of 0's and 1's
            ("0101_", True),  # Equal number of 0's and 1's
            ("000_", False),  # Unequal number of 0's and 1's
            ("_", True),  # Empty string (trivially equal)
        ]
        
        # Check if the DTM handles equal numbers of 0's and 1's correctly
        for input_string, expected in test_cases:
            with self.subTest(input_string=input_string):
                _, accepted, _ = trace_ntm(machine_description, transitions, input_string)
                self.assertEqual(accepted, expected)
    
    def test_abc_star(self):
        # Test the DTM for the language "a^n b^n c^m"
        machine_description, transitions = read_tm_csv('csv_tests/abc_star_DTM.csv')
        print(machine_description)
        print(transitions)

        # Test cases for the "a^n b^n c^m" language
        test_cases = [
            ("aabbcc_", True),  # Matches a^n b^n c^m
            ("aaabbccc_", True),  # Matches a^n b^n c^m
            ("ab_", True),  # Matches a^n b^n
            ("abcabc_", False),  # Interleaved characters should be rejected
            ("_", True),  # Empty string should be accepted
        ]
        
        # Check if the DTM accepts the correct strings for the language "a^n b^n c^m"
        for input_string, expected in test_cases:
            with self.subTest(input_string=input_string):
                _, accepted, _ = trace_ntm(machine_description, transitions, input_string)
                self.assertEqual(accepted, expected)

if __name__ == "__main__":
    unittest.main()  # Run all the test cases