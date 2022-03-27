from cv2 import phase
from cipher import Cipher
import numpy as np
import re

def read_matrix(fname="table.txt"):
    f = open(fname, "r")
    txt = f.read()
    matrix = np.array(re.findall("[A-Z]+",txt))
    return matrix.reshape((26,26))

def prompt():
    print("Simple Cipher:\n\
        [1] Encrypt\n\
        [2] Decrypt\n\
        [3] Exit")
    return input("Selection:")

def main():
    selection = prompt()
    cipher = None
    matrix = read_matrix("table.txt")
    while(True):

        if selection == "1":
            plain_text = input("Enter text:")
            key = input("Enter key:")
            cipher = Cipher(key,matrix)
            print("**********************Encryption**********************\n")
            print("Encryption Phase-1")
            processed_plaintext = cipher._preprocess_text(plain_text=plain_text)
            print(f"Plaintext: {processed_plaintext}")
            print(f"Key: {cipher._extend_key(processed_plaintext)}")
            phase_1 = cipher._encrypt_first_phase(processed_plaintext)
            print(f"Output (phase-1): {phase_1}")

            print("Encryption Phase-2")
            print(f"Inputtext: {phase_1}")

            cipher_text, groups = cipher._encrypt_second_phase(phase_1)
            group_1 = "".join(groups[0])
            group_2 = "".join(groups[1])
            print(f"group-1: {group_1}")
            print(f"group-2: {group_2}")
            print(f"Ciphertext: {cipher_text}")
            print("******************************************************")

        elif selection == "2":
            print("**********************Decryption**********************\n")
            print("Decryption Phase-1")

            cipher_text = input("Inputtext: ")
            phase_1, groups = cipher._decrypt_first_phase(cipher_text)
            group_1 = "".join(groups[0])
            group_2 = "".join(groups[1])
            print(f"group-1: {group_1}")
            print(f"group-2: {group_2}")
            print(f"Output (phase-1): {phase_1}")

            print("Decryption Phase-2")
            print(f"Inputtext: {phase_1}")
            print(f"Key: {cipher._extend_key(processed_plaintext)}")
            print(f"Plaintext: {cipher._decrypt_second_phase(phase_1)}")
            print("******************************************************")

        elif selection == "3":
            break

        else:
            print("Enter valid selection!!")

        selection = prompt()


if __name__ == "__main__":
    main()