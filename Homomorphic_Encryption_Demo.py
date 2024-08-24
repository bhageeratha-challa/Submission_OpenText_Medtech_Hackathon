import tenseal as ts
import base64

def initialize_encryption_context(scaling_factor=2**30):  # Start with a reasonably large scaling factor
    context = ts.context(
        ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = scaling_factor
    context.generate_galois_keys()
    return context

def string_to_numeric(data):
    # Convert string to a numeric vector using ASCII values
    return [ord(char) for char in data]

def numeric_to_string(numeric_data):
    # Convert numeric vector back to a string
    result = []
    for num in numeric_data:
        try:
            char = chr(int(round(num)))
            if 0 <= ord(char) <= 1114111:  # Valid Unicode range
                result.append(char)
            else:
                result.append('?')  # Placeholder for invalid characters
        except ValueError:
            result.append('?')  # Placeholder for conversion errors
    return ''.join(result)

def encrypt_data(context, data):
    numeric_data = string_to_numeric(data)
    encrypted_vector = ts.ckks_vector(context, numeric_data)
    encrypted_data = encrypted_vector.serialize()
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_data(context, encrypted_data_base64):
    encrypted_data = base64.b64decode(encrypted_data_base64.encode('utf-8'))
    encrypted_vector = ts.ckks_vector_from(context, encrypted_data)
    decrypted_numeric_data = encrypted_vector.decrypt()
    return numeric_to_string(decrypted_numeric_data)

# Example usage
context = initialize_encryption_context(scaling_factor=2**30)
original_data = "Cold Cough Ascoryl NA NA"
encrypted_data = encrypt_data(context, original_data)
decrypted_data = decrypt_data(context, encrypted_data)

print("Original Data:", original_data)
print("Encrypted Data:", encrypted_data)
print("Decrypted Data:", decrypted_data)
