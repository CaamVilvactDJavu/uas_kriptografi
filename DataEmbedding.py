# Mengimpor library yang diperlukan
import bitstring
import numpy as np


def extract_encoded_data_from_DCT(dct_blocks):
    # Inisialisasi string untuk menyimpan data yang diekstrak
    extracted_data = ""

    # Loop untuk setiap blok DCT dalam gambar
    for current_dct_block in dct_blocks:
        # Loop untuk setiap koefisien dalam blok DCT
        for i in range(1, len(current_dct_block)):
            # Konversi koefisien ke tipe data integer 32-bit
            curr_coeff = np.int32(current_dct_block[i])
            # Jika nilai koefisien lebih besar dari 1
            if (curr_coeff > 1):
                # Ambil bit terakhir dari nilai koefisien, tambahkan ke string ekstraksi
                extracted_data += bitstring.pack('uint:1',
                                                 np.uint8(current_dct_block[i]) & 0x01)

    # Kembalikan data yang diekstrak sebagai string
    return extracted_data


def embed_encoded_data_into_DCT(encoded_bits, dct_blocks):
    # Inisialisasi variabel untuk menandai apakah seluruh data telah di embed
    data_complete = False

    # Reset posisi bit pada objek bitstring yang berisi data terenkripsi
    encoded_bits.pos = 0

    # Ambil panjang data terenkripsi, lalu konversi ke format 32-bit
    encoded_data_len = bitstring.pack('uint:32', len(encoded_bits))

    # Inisialisasi list untuk menyimpan blok DCT yang telah dikonversi
    converted_blocks = []

    # Loop melalui setiap blok DCT dalam gambar
    for current_dct_block in dct_blocks:
        # Loop melalui setiap koefisien dalam blok DCT
        for i in range(1, len(current_dct_block)):
            # Konversi koefisien ke tipe data integer 32-bit
            curr_coeff = np.int32(current_dct_block[i])

            # Jika nilai koefisien lebih besar dari 1
            if (curr_coeff > 1):
                # Konversi koefisien ke tipe data uint8
                curr_coeff = np.uint8(current_dct_block[i])

                # Set data_complete menjadi True jika posisi bit terakhir mencapai akhir
                if (encoded_bits.pos == (len(encoded_bits) - 1)):
                    data_complete = True
                    break
                pack_coeff = bitstring.pack('uint:8', curr_coeff)

                # Jika posisi bit terakhir pada panjang data belum mencapai akhir
                if (encoded_data_len.pos <= len(encoded_data_len) - 1):
                    # Tambahkan bit terakhir dari panjang data ke koefisien
                    pack_coeff[-1] = encoded_data_len.read(1)
                else:
                    pack_coeff[-1] = encoded_bits.read(1)
                # Tambahkan bit terakhir dari data terenkripsi ke koefisien
                current_dct_block[i] = np.float32(pack_coeff.read('uint:8'))

        # Tambahkan blok DCT yang telah dikonversi ke dalam list
        converted_blocks.append(current_dct_block)

    # Jika data belum sepenuhnya tertanam, raise ValueError
    if not (data_complete):
        raise ValueError(
            "Data tidak sepenuhnya dapat di embed ke dalam gambar!")

    # Kembalikan blok DCT yang telah dikonversi
    return converted_blocks
