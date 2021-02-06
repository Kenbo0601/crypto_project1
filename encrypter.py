
#p2 = 0x579bde02468acf13

# return [w0,w1,w2,w3]
def genWords(txt):
    w = []  # store each word block
    n = 16  # size of each word block

    print(txt)
    for i in range(0, len(txt), n):
        w.append(txt[i:i+n])

    return w


def genKeys(key):
    k = []
    n = 8  # size of each key block

    for i in range(0, len(key), n):
        k.append(key[i:i+n])

    return k


def genKeyTable(key):
    keyTable = []
    n = 8
    subKey = []

    # iterate throgh 12 times
    for i in range(3):
        for j in range(4):
            shiftedKey = leftRotate(key)
            copyKey = shiftedKey
            key = shiftedKey

            block = []
            for k in range(0, len(key), n):
                block.append(key[k:k+n])
            block.reverse()
            index = 4*0+j
            subKey.append(block[index])

            #print(hex(int(shiftedKey, 2)))

    t = [''.join(subKey)]
    print(hex(int(t[0], 2)))


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
    plainTxt = 0xabcdef0123456789
    binarize = "{0:b}".format(plainTxt)
    genKeyTable(binarize)

    wordblock = genWords(binarize)
    keyblock = genKeys(binarize)
    print(keyblock)

    #test = leftRotate(binarize)
