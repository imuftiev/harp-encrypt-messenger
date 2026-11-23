import enum


class Encryption(str, enum.Enum):
    RSA_ENCRYPT = "RSA_ENCRYPT"
    STREEBOG = "STREEBOG_ENCRYPT"
    PLAIN = "PLAIN"
