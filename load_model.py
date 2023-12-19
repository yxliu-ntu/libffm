import math
import struct  # Importing the struct module
import sys
import numpy as np

class FFMModel:
    def __init__(self, n, m, k, normalization, W):
        self.n = n
        self.m = m
        self.k = k
        self.normalization = normalization
        self.W = np.reshape(W, (n, m, 2*k))

    def save_model(self, fpath):
        filtered_model_W = self.W[:, :, :self.k]
        print('Save weight of shape', filtered_model_W.shape)
        np.save(fpath, filtered_model_W)

def get_k_aligned(k, use_sse=False):
    ALIGN_BYTE = 16 if use_sse else 4
    ALIGN = ALIGN_BYTE // 4  # sizeof(ffm_float) is 4 bytes in Python
    return math.ceil(k / ALIGN) * ALIGN, ALIGN

def get_w_size(n, m, k, use_sse=False):
    k_aligned, ALIGN = get_k_aligned(k, use_sse)
    return n * m * k_aligned * 2

def ffm_load_model(path, use_sse=False):
    with open(path, 'rb') as f_in:
        n = struct.unpack('i', f_in.read(4))[0]
        m = struct.unpack('i', f_in.read(4))[0]
        k = struct.unpack('i', f_in.read(4))[0]
        normalization = struct.unpack('?', f_in.read(1))[0]

        w_size = get_w_size(n, m, k, use_sse)
        W = np.zeros(w_size, dtype=np.float32)

        CHUNK_SIZE = 1024  # Adjust as needed
        for offset in range(0, w_size, CHUNK_SIZE):
            next_offset = min(w_size, offset + CHUNK_SIZE)
            size = next_offset - offset
            W[offset:next_offset] = struct.unpack(f'{size}f', f_in.read(4 * size))

        return FFMModel(n, m, k, normalization, W)

model = ffm_load_model(sys.argv[1], True)
print(model.W.shape)
print(model.m, model.n, model.k, model.normalization)
model.save_model('./init_model.npy')
