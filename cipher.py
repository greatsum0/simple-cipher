import numpy as np
import re
import math


class Cipher:
    
    def __init__(self, key, conversion_table):
        self.key = self._preprocess_text(key)
        self.conversion_table = np.array(conversion_table)

    def encrypt(self, plain_text):
        return self._encrypt_second_phase(self._encrypt_first_phase(plain_text))[0]

    def decrypt(self, cipher_text):
        return self._decrypt_second_phase(self._decrypt_first_phase(cipher_text))[0]

    def _preprocess_text(self, plain_text):
        return ("".join(re.findall("[A-Za-z]+",plain_text))).upper()

    def _extend_key(self, plain_text):
            len_plaintext = len(plain_text)
            len_key = len(self.key)
            extension_mul = math.ceil(len_plaintext/len_key)
            extended_key = (self.key * extension_mul)[:len_plaintext]
            return extended_key   

    def _encrypt_first_phase(self, plain_text):
        plain_text = self._preprocess_text(plain_text)
        self.extended_key = self._extend_key(plain_text)
        cipher = []

        for i in range(len(plain_text)):
            idx_table= self.conversion_table[:,:1]
            key_idx, _ = np.where(idx_table == self.extended_key[i])
            plain_text_idx, _ = np.where(idx_table == plain_text[i])
            cipher.append(self.conversion_table[key_idx,plain_text_idx][0])

        return "".join(cipher)

    def _encrypt_second_phase(self, cipher_text):
        len_column = math.ceil(len(cipher_text)/2)
        cipher_text = cipher_text + "0"*abs(len(cipher_text) - len_column * 2)
        return "".join(np.array(list(cipher_text)).reshape((2,len_column)).T.reshape(1,-1).squeeze().tolist()), np.array(list(cipher_text)).reshape((2,len_column))
        

    def _decrypt_first_phase(self, cipher_text):
        len_column = math.ceil(len(cipher_text)/2)
        decipher = "".join(
            (np.array(list(cipher_text)).reshape(len_column,2).T).reshape(1,-1).squeeze())
        return self._preprocess_text(decipher), np.array(list(cipher_text)).reshape(len_column,2).T
        

    def _decrypt_second_phase(self, cipher_text):
        plain_text = []
        idx_table= self.conversion_table[:1,:][0]   
        self.extended_key = self._extend_key(cipher_text)
        for i in range(len(cipher_text)):
            key_idx= np.where(idx_table == self.extended_key[i])[0][0]
            decipher_row = self.conversion_table[key_idx,:]
            plain_text_idx = np.where(decipher_row == cipher_text[i])[0][0]
            plain_text.append(idx_table[plain_text_idx])
        return "".join(plain_text)
