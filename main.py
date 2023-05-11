import os
import random

def encrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = f"{filename}.crypt"
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = ''.join(chr(random.randint(0, 0xFF)) for _ in range(16))
    with open(filename, 'rb') as input_file:
        with open(output_file, 'wb') as output_file:
            output_file.write(filesize.encode())
            output_file.write(IV.encode())

            while True:
                chunk = input_file.read(chunk_size)

                if len(chunk) == 0:
                    break

                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                xor_chunk = ''.join(chr(ord(chunk[i]) ^ ord(key[i])) for i in range(16))
                output_file.write(xor_chunk.encode())

def decrypt(key, filename):
    chunk_size = 64 * 1024
    output_file = filename[:-6]
    filesize = int(filename[-22:-6])
    IV = filename[-6:]

    with open(filename, 'rb') as input_file:
        with open(output_file, 'wb') as output_file:
            while True:
                chunk = input_file.read(chunk_size)

                if len(chunk) == 0:
                    break

                xor_chunk = ''.join(chr(ord(chunk[i]) ^ ord(key[i])) for i in range(16))
                output_file.write(xor_chunk.encode())

            output_file.truncate(filesize)

def main():
    choice = input("Encrypt (E) or Decrypt (D)? ")

    if choice == 'E':
        filename = input("File to encrypt: ")
        key = input("Encryption key: ")
        encrypt(key, filename)
        print("File encrypted.")

    elif choice == 'D':
        filename = input("File to decrypt: ")
        key = input("Decryption key: ")
        decrypt(key, filename)
        print("File decrypted.")

    else:
        print("Invalid choice.")

if __name__ == '__main__':
    main()
