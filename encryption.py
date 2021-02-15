from operator import xor
from ftable import table
import binascii


def plain_to_bin(txt):
    arr = []
    for i in txt:
        temp = ord(i)
        arr.append(bin(temp)[2:].zfill(8))
    return "".join(arr)


def build_64bit_blocks(binarizedWord):
    array = []
    n = 1
    for i in range(0, len(binarizedWord), n):
        array.append(binarizedWord[i:i+n])
    array.reverse()

    reversedBits = "".join(array)
    array.clear()

    for j in range(0, len(reversedBits), 64):
        array.append(reversedBits[j:j+64])

    # reverse back array and grab the first element for padding
    array.reverse()
    temp = []
    for k in range(0, len(array[0]), n):
        temp.append(array[0][k:k+n])

    temp.reverse()
    letsPadding = "".join(temp)
    padded = letsPadding.zfill(64)

    # remove the first element, don't need it anymore
    array.pop(0)
    restOfBits = "".join(array)
    array.clear()

    # now need to reverse back the rest of the bits
    for back in range(0, len(restOfBits), n):
        array.append(restOfBits[back:back+n])
    array.reverse()
    motodouri = "".join(array)
    array.clear()

    array.append(padded)
    array.append(motodouri)
    finalProcess = "".join(array)
    array.clear()

    for a in range(0, len(finalProcess), 64):
        array.append(finalProcess[a:a+64])

    return array


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
    if len(key) < 64:
        padding = key.zfill(64)
        for i in range(0, len(padding, n)):
            k.append(padding[i:i+n])
    else:
        for i in range(0, len(key), n):
            k.append(key[i:i+n])

    return k


def xor(word, key):
    # xor word + key: return a list r
    r = []
    for w, k in zip(word, key):
        xored = int(w, 2) ^ int(k, 2)
        # convert from decimal to binary, padding if necessary
        binarizedXor = bin(xored)[2:].zfill(16)
        r.append(binarizedXor)
    return r


def genKeyTable(key):
    table = []
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

        eachRow = []
        for c in subKey:
            h = hex(int(c, 2))
            if len(h[2:]) < 2:
                addZero = "0x0" + h[2:]
                eachRow.append(addZero)
            else:
                eachRow.append(h)
        table.append(eachRow)

    return table


def leftRotate(var):
    shifter = []

    for i in range(0, len(var), 1):
        shifter.append(var[i:i+1])

    mostSig = shifter.pop(0)
    shifter.append(mostSig)

    t = [''.join(shifter)]
    return t[0]
    # p = int(t[0], 2)
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
    # k9 = bin(int(keyTable[round][9], 16))[2:]
    k9 = keyTable[round][9]
    k10 = bin(int(keyTable[round][10], 16))[2:]
    k11 = keyTable[round][11]
    # k11 = bin(int(keyTable[round][11], 16))[2:]

    T0 = int(G(r0, k0, k1, k2, k3), 16)  # convert from hex to decimal
    T1 = int(G(r1, k4, k5, k6, k7), 16)
    # print("T0 is : ", hex(T0), ":", T0)
    # print("T1 is : ", hex(T1), ":", T1)
    # k9temp = hex(int(k9, 2))
    # k11temp = hex(int(k11, 2))
    # concat1 = hex(int(k8, 2))+k9temp[2:]
    concat1 = hex(int(k8, 2))+k9[2:]
    # concat2 = hex(int(k10, 2))+k11temp[2:]
    concat2 = hex(int(k10, 2))+k11[2:]
    F0 = (T0+2*T1+int(concat1, 16)) % 65536  # mod 2^16
    F1 = (2*T0+T1+int(concat2, 16)) % 65536
    # print(hex(F0))
    # print(hex(F1))
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
    #print("g1:", hex(int(g1, 2)))
    #print("g2:", hex(int(g2, 2)))
    tablelookup1 = int(g2, 2) ^ int(k0, 2)
    g3 = table[tablelookup1] ^ int(g1, 2)
    #print("g3:", hex(int(g3)))
    tablelookup2 = g3 ^ int(k1, 2)
    g4 = table[tablelookup2] ^ int(g2, 2)
    #print("g4:", hex(int(g4)))
    tablelookup3 = g4 ^ int(k2, 2)
    g5 = table[tablelookup3] ^ g3
    #print("g5:", hex(int(g5)))
    tablelookup4 = g5 ^ int(k3, 2)
    g6 = table[tablelookup4] ^ g4
    #print("g6:", hex(int(g6)))
    check = hex(int(g6))[2:]
    if len(check) < 2:
        return hex(int(g5)) + "0"+check

    return hex(int(g5)) + hex(int(g6))[2:]
    # return bin(g5)[2:]+bin(g6)[2:]  # return concatenation of g5 and g6


# driver function
def driver(plaintxt, key):
    #b = bin(0x0123456789abcdef)[2:]
    binarizedKey = bin(int(key, 16))[2:]
    keyTable = genKeyTable(binarizedKey)
    binarizedWord = plain_to_bin(plaintxt)

    # if the length of plaintext is within 64 bits
    if len(binarizedWord) <= 64:
        wordblock = genWords(binarizedWord)
        keyblock = genKeys(binarizedKey)
        r = xor(wordblock, keyblock)

        cipher = encryption(r, keyblock, keyTable)
        f = open("ciphertext.txt", "w")
        f.write("0x"+cipher)
        f.close()
    else:  # otherwise separate plaintext and concatenate the results
        bit_blocks = build_64bit_blocks(binarizedWord)
        result = []
        for i in range(len(bit_blocks)):
            wordblock = genWords(bit_blocks[i])
            keyblock = genKeys(binarizedKey)
            r = xor(wordblock, keyblock)

            cipher = encryption(r, keyblock, keyTable)
            result.append(cipher)

        concat = "".join(result)
        f = open("ciphertext.txt", "w")
        f.write("0x"+concat)
        f.close()


def encryption(r, keyblock, keyTable):
    for round in range(16):
        newr2 = r[0]
        newr3 = r[1]
        f = F(r[0], r[1], round, keyTable)
        newr0 = bin(f[0] ^ int(r[2], 2))[2:]
        newr1 = bin(f[1] ^ int(r[3], 2))[2:]
        r = []
        r.append(newr0.zfill(16))
        r.append(newr1.zfill(16))
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

    return hex(c0)[2:] + hex(c1)[2:] + hex(c2)[2:] + hex(c3)[2:]


if __name__ == "__main__":
    plaintext = None
    key = None

    p = open('p4.txt', 'r')
    plaintext = p.read().strip('\n')
    p.close()
    k = open('key.txt', 'r')
    key = k.read()
    k.close()

    j = int(key, 16)
    driver(plaintext, hex(j))
