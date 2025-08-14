# result
# 127.0.0.1:6379> get radiator-user-d52f1f5ac88cb108
# "l=:n9n=ik@@kj98@"


def zeep_encode(input_str, key):
    """
    Convert Perl zeep_encode function to Python
    Original Perl: sub zeep_encode { my ($self, $input, $key) = @_; my $encoded = ''; foreach my $char (split //, $input) { $encoded .= chr(ord($char) + $key); } return substr($encoded, 1, length($encoded) - 2); }
    
    Args:
        input_str (str): The input string to encode
        key (int): The key value to shift characters by
        
    Returns:
        str: Encoded string with first and last characters removed
    """
    if not input_str:
        return ""
    
    if len(input_str) <= 2:
        return ""  # Would result in empty string after removing first and last chars
    
    encoded = ""
    
    for char in input_str:
        encoded += chr(ord(char) + key)
    
    return encoded[1:-1]  # equivalent to substr(..., 1, length - 2)


def zeep_decode(encoded_str, key):
    """
    Reverse function to decode a zeep_encoded string
    
    Args:
        encoded_str (str): The encoded string to decode
        key (int): The key value used for encoding
        
    Returns:
        str: Decoded original string
    """
    if not encoded_str:
        return ""
    
    # First, we need to reverse the substr operation by adding back chars
    # We need to guess what the first and last chars were
    # For now, let's assume they were the same as the current first/last + key
    first_char = chr(ord(encoded_str[0]) - key)
    last_char = chr(ord(encoded_str[-1]) - key)
    
    # Reconstruct the full encoded string
    full_encoded = first_char + encoded_str + last_char
    
    # Now decode each character
    decoded = ""
    for char in full_encoded:
        decoded += chr(ord(char) - key)
    
    return decoded


# Test the functions
if __name__ == "__main__":
    # Test with your example
    original = "d52f1f5ac88cb108"
    key = 8
    
    password = ''.join(chr(ord(c) + 8) for c in f"'{original}'")[1:-1]
    print(">>>>> ", password)
    zeep_encoded = zeep_encode(original, key)
    print(f"Original: {original}")
    print(f"Encoded:  {zeep_encoded}")  # Should output: n9n=ik@@kj98
    
    # Test edge cases
    print(f"\nEdge cases:")
    print(f"Empty string: '{zeep_encode('', key)}'")
    print(f"Short string: '{zeep_encode('ab', key)}'")
    print(f"Single char: '{zeep_encode('a', key)}'")
    
    # Show character mapping for debugging
    print(f"\nCharacter mapping with key={key}:")
    for char in original[:5]:  # Show first 5 characters
        encoded_char = chr(ord(char) + key)
        print(f"'{char}' (ASCII {ord(char)}) -> '{encoded_char}' (ASCII {ord(encoded_char)})")
