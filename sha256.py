from textwrap import wrap

_k = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

INITIAL_HASH = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

INT_BITS = 32

def rightRotate(n, d): 
  
    # In n>>d, first d bits are 0. 
    # To put last 3 bits of at  
    # first, do bitwise or of n>>d 
    # with n <<(INT_BITS - d)  
    return (n >> d)|(n << (INT_BITS - d)) 

def pre_processing():
    x = input("What is your name? ")
    print(x)

    binaryEncode = bytearray(x, 'ascii')

    #Binary is encoded
    # a bit 1 is appended
    binaryEncodeLength = len(x)  * 8 
    binaryEncode.append(0x80)
    #let l be length and let k be 0 bits appeneded to the end then l+1+k congruent 448 mod 512
    
    while (( ( len(binaryEncode) * 8 + 64)  % 512) != 0):
        binaryEncode.append(0x00)
        

    binaryEncode += binaryEncodeLength.to_bytes(8, 'big')
    
    
    return binaryEncode

def processing(binaryEncode):
    

    block = []
    for i in range(0, len(binaryEncode), 64):
        block.append(binaryEncode[i:i+64])


    for blockNum in block:
        w = [] 
        
        #Intializes the 32 bit list of size 64 to contain w_0 - w_15
        index = 0
        for index in range(0,64):
            if index < 16:
                w.append(bytes(blockNum[index*4:(index*4)+4]))


            else:

                sigma0 = sig0(int.from_bytes(w[index-15], 'big'))
                tmp1 = int.from_bytes(w[index-16], 'big')
                tmp2 =  int.from_bytes(w[index -7], 'big')
                sigma1 = sig1(int.from_bytes(w[index-2], 'big'))
                datum = ( (tmp1 + sigma0 + tmp2 + sigma1)  % (2**32)).to_bytes(4, 'big')
                w.append(datum)


        assert(len(w) == 64)

        a = INITIAL_HASH[0]
        b = INITIAL_HASH[1]
        c = INITIAL_HASH[2]
        d = INITIAL_HASH[3]
        e = INITIAL_HASH[4]
        f = INITIAL_HASH[5]
        g = INITIAL_HASH[6]
        h = INITIAL_HASH[7]

        i = 0
        while i < 64:
            sigm0 = s0(a)
            sigm1 = s1(e)
            ch = (e & f) ^ ( ~e & g)
            temp1 = (h+ sigm1 + ch + _k[i] + int.from_bytes(w[i], 'big')) % (2**32)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (sigm0 + maj) % (2**32)
            
            h = g
            g = f
            f = e
            e = (d+ temp1) % 2**32
            d = c
            c = b
            b = a
            a= (temp1 + temp2) % (2**32)

            i +=1

        h0 = (INITIAL_HASH[0] + a) % (2**32)
        h1 = (INITIAL_HASH[1] + b) % (2**32)
        h2 = (INITIAL_HASH[2] + c) % (2**32)
        h3 = (INITIAL_HASH[3] + d) % (2**32)
        h4 = (INITIAL_HASH[4] + e) % (2**32)
        h5 = (INITIAL_HASH[5] + f) % (2**32)
        h6 = (INITIAL_HASH[6] + g) % (2**32)
        h7 = (INITIAL_HASH[7] + h) % (2**32)


        return (
            
            (h0).to_bytes(4, 'big') + (h1).to_bytes(4, 'big') + (h2).to_bytes(4, 'big') +
            (h3).to_bytes(4, 'big') + (h4).to_bytes(4, 'big') + (h5).to_bytes(4, 'big') +
            (h6).to_bytes(4, 'big') + (h7).to_bytes(4, 'big')
        )
        
    
def sig0(num: int):
    return (rightRotate((num), 7) ^ rightRotate((num), 18)
            ^ ((num) >> 3))
def sig1(num):
    return (rightRotate((num), 17) ^ rightRotate((num), 19) ^ ((num) >> 10))

def s0(a: int):
    tmp = rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)
    #print(tmp)
    return tmp

def s1(e: int):
    tmp = rightRotate(e,6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)
    #print(tmp)
    return tmp

if __name__ == '__main__':
    binaryEncode = pre_processing()
    hashValue = processing(binaryEncode)
    print(hashValue.hex())