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
    result = []
    # 12 subkeys from keytable
    k0 = bin(int(keyTable[round][0], 16))[2:]
    k1 = bin(int(keyTable[round][1], 16))[2:]
    k2 = bin(int(keyTable[round][2], 16))[2:]
    k3 = bin(int(keyTable[round][3], 16))[2:]
    k4 = bin(int(keyTable[round][4], 16))[2:]
    k5 = bin(int(keyTable[round][5], 16))[2:]
    k6 = bin(int(keyTable[round][6], 16))[2:]
    k7 = bin(int(keyTable[round][7], 16))[2:]
    k8 = bin(int(keyTable[round][8], 16))[2:]
    k9 = bin(int(keyTable[round][9], 16))[2:]
    k10 = bin(int(keyTable[round][10], 16))[2:]
    k11 = bin(int(keyTable[round][11], 16))[2:]

    T0 = int(G(r0, k0, k1, k2, k3), 2)
    T1 = int(G(r1, k4, k5, k6, k7), 2)
    F0 = (T0+2*T1+int(k8+k9, 2)) % 16
    F1 = (2*T0+T1+int(k10+k11, 2)) % 16
    result.append(F0)
    result.append(F1)
    return result


def G(r0, k0, k1, k2, k3):
    spliter = []
    # split into left 8 bits and right 8 bits
    for i in range(0, len(r0), 8):
        spliter.append(r0[i:i+8])

    g1 = spliter[0]
    g2 = spliter[1]
    tablelookup1 = int(g2, 2) ^ int(k0, 2)
    g3 = table[tablelookup1] ^ int(g1, 2)
    tablelookup2 = g3 ^ int(k1, 2)
    g4 = table[tablelookup2] ^ int(g2, 2)
    tablelookup3 = g4 ^ int(k2, 2)
    g5 = table[tablelookup3] ^ g3
    tablelookup4 = g5 ^ int(k3, 2)
    g6 = table[tablelookup4] ^ g4

    return bin(g5)[2:]+bin(g6)[2:]  # return concatenation of g5 and g6


# driver function
def driver(plaintxt, key):
    binarizedWord = bin(plaintxt)[2:]
    binarizedKey = bin(key)[2:]
    keyTable = genKeyTable(binarizedKey)
    wordblock = genWords(binarizedWord)
    keyblock = genKeys(binarizedKey)
    r = xor(wordblock, keyblock)
    for round in range(16):
        newr2 = r[0]
        newr3 = r[1]
        f = F(r[0], r[1], round, keyTable)
        newr0 = bin(f[0] ^ int(r[2], 2))[2:]
        newr1 = bin(f[1] ^ int(r[3], 2))[2:]
        r = []
        r.append(newr0)
        r.append(newr1)
        r.append(newr2)
        r.append(newr3)

    y0 = r[2]
    y1 = r[3]
    y2 = r[0]
    y3 = r[1]

    c0 = int(y0, 2) ^ int(keyblock[0], 2)
    c1 = int(y1, 2) ^ int(keyblock[1], 2)
    c2 = int(y2, 2) ^ int(keyblock[2], 2)
    c3 = int(y3, 2) ^ int(keyblock[3], 2)

    print(hex(c0))
    print(hex(c1))
    print(hex(c2))
    print(hex(c3))

    #index = str(0x7a)
    # print(hex(table[int(index)]))


if __name__ == "__main__":
    # 1 read plaintext and key from txt file
    plaintext = 0x0123456789abcdef
    key = 0xabcdef0123456789
    driver(plaintext, key)
    # print(hex(table[0]))

    #binarizedWord = "{0:b}".format(plaintext)
    #binarizedKey = "{0:b}".format(key)
    #keyTable = genKeyTable(binarizedKey)
    #wordblock = genWords(binarizedWord)
    #keyblock = genKeys(binarizedKey)
    #xor(wordblock, keyblock)
