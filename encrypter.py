
import itertools


def genWords(txt):
    w = []  # store each word block
    n = 16  # size of each word block

    if len(txt) < 64:
        padding = txt.zfill(64)  # fill with 0s if not 64 bits
        for i in range(0, len(padding), n):
            w.append(padding[i:i+n])
    else:
        for i in range(0, len(txt), n):
            w.append(txt[i:i+n])

    return w


def genKeys(key):
    k = []
    n = 16  # size of each key block

    for i in range(0, len(key), n):
        k.append(key[i:i+n])

    return k


def xor(word, key):
    r = []
    for w, k in zip(word, key):
        print(w, k)
    return


def genKeyTable(key):
    keyTable = []
    n = 8

    # iterate throgh 16 times (all rounds)
    for round in range(16):
        subKey = []
        for i in range(3):
            for j in range(4):
                shiftedKey = leftRotate(key)
                key = shiftedKey

                block = []
                for k in range(0, len(key), n):
                    block.append(key[k:k+n])
                block.reverse()
                index = (4*round+j) % 8
                subKey.append(block[index])

        list = []
        for c in subKey:
            h = hex(int(c, 2))
            list.append(h)
        keyTable.append(list)

    return keyTable


def leftRotate(var):
    shifter = []

    for i in range(0, len(var), 1):
        shifter.append(var[i:i+1])

    mostSig = shifter.pop(0)
    shifter.append(mostSig)

    t = [''.join(shifter)]
    return t[0]
    #p = int(t[0], 2)
    # return hex(p)


if __name__ == "__main__":
    # 1 read plaintext and key from txt file
    # 2 generate w0 to w4 based on the plaintext
    # 3 generate keys from k0 to k7
    # 4 generate 7 subkeys and rotate after
    plaintext = 0x0123456789abcdef
    key = 0xabcdef0123456789
    binarizedWord = "{0:b}".format(plaintext)
    binarizedKey = "{0:b}".format(key)
    w = genKeyTable(binarizedKey)

    wordblock = genWords(binarizedWord)
    keyblock = genKeys(binarizedKey)
    xor(wordblock, keyblock)

    #test = leftRotate(binarize)
