def check_and_make_palindrome():
    # Take input from the user
    s = input("Enter a string: ")

    # Function to check if a string is a palindrome
    def is_palindrome(string):
        return string == string[::-1]

    # Check if the string is already a palindrome
    if is_palindrome(s):
        print(f"The input string '{s}' is already a palindrome!")
    else:
        # Function to make the string a palindrome
        def make_palindrome(s):
            # Create a temporary string combining s, a separator, and the reverse of s
            temp = s + "#" + s[::-1]
            n = len(temp)

            # Compute the Longest Prefix Suffix (LPS) array
            lps = [0] * n
            j = 0  # Length of previous longest prefix suffix

            for i in range(1, n):
                while j > 0 and temp[i] != temp[j]:
                    j = lps[j - 1]
                if temp[i] == temp[j]:
                    j += 1
                lps[i] = j

            # LPS value of the last character gives the length of the palindromic suffix
            longest_palindromic_suffix = lps[-1]

            # Append the non-palindromic prefix (reversed) to the original string
            return s + s[:len(s) - longest_palindromic_suffix][::-1]

        # Make the string a palindrome
        palindrome = make_palindrome(s)
        print(f"The input string '{s}' is not a palindrome.")
        print(f"The minimal palindrome by adding characters: '{palindrome}'")

# Call the function
check_and_make_palindrome()
