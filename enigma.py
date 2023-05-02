import string


'''
This code creates the `Enigma` class, which contains a list of rotors and a reflector, 
as well as the `encrypt' method, which encrypts the message. Each rotor is represented by the `Rotor` class, 
which contains the rotor wiring and its current position. The reflector is represented by the `Reflector` class, 
which contains the reflector wiring. The `encrypt` method of the `Enigma` class encrypts each character of the message 
using the `encrypt_char' method, which encrypts the character through each rotor and reflector in reverse order. 
The `rotate_rotors` method of the `Enigma' class rotates the rotor by one position each time a character is encrypted.
'''


class Enigma:
    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector

    def encrypt(self, message):
        encrypted_message = ""
        for char in message:
            if char in string.ascii_uppercase:
                encrypted_char = self.encrypt_char(char)
                encrypted_message += encrypted_char
                self.rotate_rotors()
            else:
                encrypted_message += char
        return encrypted_message

    def encrypt_char(self, char):
        encrypted_char = char
        for rotor in self.rotors:
            encrypted_char = rotor.encrypt(encrypted_char)
        encrypted_char = self.reflector.reflect(encrypted_char)
        for rotor in reversed(self.rotors):
            encrypted_char = rotor.encrypt_inverse(encrypted_char)
        return encrypted_char

    def rotate_rotors(self):
        for i in range(len(self.rotors)):
            if i == 0:
                self.rotors[i].rotate()
            elif self.rotors[i-1].notch_position == self.rotors[i-1].position:
                self.rotors[i].rotate()


class Rotor:
    def __init__(self, wiring, notch_position):
        self.wiring = wiring
        self.position = 0
        self.notch_position = notch_position

    def encrypt(self, char):
        index = (ord(char) - 65 + self.position) % 26
        encrypted_index = (ord(self.wiring[index]) - 65 - self.position) % 26
        encrypted_char = chr(encrypted_index + 65)
        return encrypted_char

    def encrypt_inverse(self, char):
        index = (ord(char) - 65 + self.position) % 26
        encrypted_index = (self.wiring.index(chr((index + self.position) % 26 + 65)) - self.position) % 26
        encrypted_char = chr(encrypted_index + 65)
        return encrypted_char

    def rotate(self):
        self.position = (self.position + 1) % 26


class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, char):
        index = ord(char) - 65
        reflected_index = ord(self.wiring[index]) - 65
        reflected_char = chr(reflected_index + 65)
        return reflected_char


rotor_I_wiring = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor_II_wiring = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor_III_wiring = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
reflector_B_wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

rotor_I = Rotor(rotor_I_wiring, 16)
rotor_II = Rotor(rotor_II_wiring, 4)
rotor_III = Rotor(rotor_III_wiring, 21)
reflector_B = Reflector(reflector_B_wiring)

enigma_machine = Enigma([rotor_I, rotor_II, rotor_III], reflector_B)

message_to_encrypt = input(str('Input your message:\n')).upper()
encrypted_message_result = enigma_machine.encrypt(message_to_encrypt)
print(encrypted_message_result)
