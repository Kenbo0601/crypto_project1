from operator import xor
from ftable import table


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
    # xor word + key: return a list r
    r = []
    for w, k in zip(word, key):
        xored = int(w, 2) ^ int(k, 2)
        binarizedXor = bin(xored)[2:]  # convert from decimal to binary
        r.append(binarizedXor)
    return r


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


def F(r0, r1, round, keyTable):
    # 12 subkeys from keytable
    return


def G(r0, k0, k1, k2, k3, round):
    spliter = []
    # split into left 8 bits and right 8 bits
    for i in range(0, len(r0), 8):
        spliter.append(r0[i:i+8])

    g1 = spliter[0]
    g2 = spliter[1]
    tablelookup1 = int(g2, 2) ^ int(k0, 2)
    g3 = table[tablelookup1] ^ int(g1, 2)
    print(g3)
    return


# driver function
def driver(plaintxt, key):
    binarizedWord = bin(plaintxt)[2:]
    binarizedKey = bin(key)[2:]
    keyTable = genKeyTable(binarizedKey)
    wordblock = genWords(binarizedWord)
    keyblock = genKeys(binarizedKey)
    r = xor(wordblock, keyblock)

    # keytable[round#][loc of hex]
    k0 = bin(int(keyTable[0][0], 16))[2:]
    k1 = bin(int(keyTable[0][0], 16))[2:]
    k2 = bin(int(keyTable[0][0], 16))[2:]
    k3 = bin(int(keyTable[0][0], 16))[2:]
    #print(bin(int(k0, 16))[2:])
    G(r[0], k0, k1, k2, k3, 0)
    index = str(0x7a)
    print(hex(table[int(index)]))


if __name__ == "__main__":
    # 1 read plaintext and key from txt file
    plaintext = 0x0123456789abcdef
    key = 0xabcdef0123456789
    driver(plaintext, key)
    print(hex(table[0]))

    #binarizedWord = "{0:b}".format(plaintext)
    #binarizedKey = "{0:b}".format(key)
    #keyTable = genKeyTable(binarizedKey)
    #wordblock = genWords(binarizedWord)
    #keyblock = genKeys(binarizedKey)
    #xor(wordblock, keyblock)
