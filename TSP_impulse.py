import sounddevice as sd
import soundfile as sf
import numpy as np
import os
import struct
from tqdm import tqdm
import sys
import time
import datetime


# TSPの設定
def normal_tsp_func(n, gain=50, repeat=1):
    N = 2**n
    m = N//4

    A = 50
    L = N//2 - m
    k = np.arange(0, N)

    tsp_freq = np.zeros(N, dtype=np.complex128)
    tsp_exp = np.exp(-1j*4*m*np.pi*(k/N)**2)

    tsp_freq[0:N//2+1] = tsp_exp[0:N//2+1]
    tsp_freq[N//2+1: N+1] = np.conj(tsp_exp[1 : N//2][::-1])

    tsp_inv_freq = 1 / tsp_freq

    tsp = np.real(np.fft.ifft(tsp_freq))
    tsp = gain * np.roll(tsp, L)

    tsp_repeat = np.r_[np.tile(tsp, repeat+1), np.zeros(N)]

    tsp_inv = np.real(np.fft.ifft(tsp_inv_freq))
    tsp_inv =  gain * np.roll(tsp_inv, -L)

    tsp_inv_repeat = np.r_[np.tile(tsp_inv, repeat+1), np.zeros(N)]

    return tsp_repeat, tsp_inv

# 同期加算
def sychronous_addition(filename, repeat, N, channel):

    if channel == 1:
        data, fs = sf.read(filename)


        # add zeros if length is too short
        if len(data) < (repeat + 1) * N:
            data = np.r_[data, np.zeros((repeat + 1) * N - len(data))]

        mean = np.zeros(N)
        for i in range(repeat):
            mean += data[(i + 1) * N : (i + 2) * N]
        mean = mean / repeat

        return mean
    else:
        data, fs = sf.read(filename)
        datal = data[:, 0]
        datar = data[:, 1]

        # add zeros if length is too short
        if len(datal) < (repeat + 1) * N:
            datal = np.r_[datal, np.zeros((repeat + 1) * N - len(datal))]
            datar = np.r_[datar, np.zeros((repeat + 1) * N - len(datar))]

        meanl = np.zeros(N)
        meanr = np.zeros(N)
        for i in range(repeat):
            meanl += datal[(i + 1) * N: (i + 2) * N]
            meanr += datar[(i + 1) * N: (i + 2) * N]
        meanl = meanl / repeat
        meanr = meanr / repeat

        return meanl, meanr

def makedir():
    if channel == 1:
        os.makedirs(datapath+"/raw", exist_ok=True)
        os.makedirs(datapath + "/Impulse", exist_ok=True)
        print("dir : " + datapath + "\n")
    elif channel ==2:
        os.makedirs(datapath + "/raw", exist_ok=True)
        os.makedirs(datapath + "/Impulse/L", exist_ok=True)
        os.makedirs(datapath + "/Impulse/R", exist_ok=True)
        print("dir : " + datapath + "\n")


if __name__ == '__main__':
    name = "Unknown" #名前
    length = 14 #長さ(2^?)
    amp = 1 #振幅(MAX=1に対する倍率)
    repeat = 1 #同期加算回数
    times = 10 #測定回数
    interval = 3 #待ち時間
    sleep_times = 3 # 測定間隔[sec]

    # オーディオデバイス設定
    input_device = 17
    output_device = 17
    channel = 1
    sample_rate = 44100

    args = sys.argv

    if len(args) == 9:
        name = str(args[1])
        length = int(args[2])
        repeat = int(args[3])
        times = int(args[4])
        sample_rate = int(args[5])
        channel = int(args[6])
        input_device = int(args[7])
        output_device = int(args[8])

    # データパス設定
    datapath = "DDB/" + name + "_" + str(datetime.date.today()) + "-" + str(datetime.datetime.now().strftime('%H-%M'))

    makedir()


    sd.default.device = [int(input_device), int(output_device)]  # 入出力デバイス番号[in,out]
    sd.default.channels = channel

    normal_tsp1, normal_tsp_inv1 = normal_tsp_func(int(length), repeat=int(repeat))


    if channel == 2:
        normal_tsp2 = []

        for i in range(len(normal_tsp1)):
            normal_tsp2.append([normal_tsp1[i], normal_tsp1[i]])


        sf.write('normal_tsp.wav', normal_tsp2,int(sample_rate))

    elif channel == 1:
        normal_tsp2 = normal_tsp1
        sf.write('normal_tsp.wav', normal_tsp2, int(sample_rate))

    else:
        exit()


    if channel == 1:
        # 録音設定＆録音
        play_filename = "normal_tsp.wav"


        playwav, fs = sf.read(play_filename)

        print("\n------------start------------\n")
        time.sleep(1)

        for count in tqdm(range(times)):
            record_filename = str(datapath) + "/raw/" + str(count) + ".wav"
            record_data = sd.playrec(playwav, fs, dtype='int16')# Play＆Rec
            print("\n  Play & Recording...")
            sd.wait()


            sf.write(record_filename, record_data, int(sample_rate))

            n = int(length)
            N = 2 ** n
            fs = int(sample_rate)
            normal_mean = sychronous_addition(record_filename, int(repeat), N,1)
            normal_tsp, normal_tsp_inv = normal_tsp_func(n)
            normal_tsp_inv_freq = np.fft.fft(normal_tsp_inv)

            H_normal = np.fft.fft(normal_mean) * normal_tsp_inv_freq

            h_normal = np.fft.ifft(H_normal)

            f = np.linspace(0, fs/2, N//2)


            # インパルス応答の保存
            h_normal2 = h_normal.real/max(abs(h_normal.real))
            with open(str(datapath) + "/Impulse/"+str(count)+".DDB", "wb") as fout:
                for k in range(len(h_normal2)):
                    fout.write(struct.pack("d", h_normal2[k]))

            # 繰り返し用スリープ
            for sleeptime in range(sleep_times):
                sys.stdout.write(str(sleep_times-sleeptime) + ' ')
                sys.stdout.flush()
                time.sleep(1)



    elif channel == 2:
        # 録音設定＆録音
        play_filename = "normal_tsp.wav"

        playwav, fs = sf.read(play_filename)

        print("\n------------start------------\n")
        time.sleep(1)

        for count in tqdm(range(times)):
            record_filename = str(datapath) + "/raw/" + str(count) + ".wav"
            record_data = sd.playrec(playwav, fs, dtype='int16')  # Play＆Rec
            print("\n  Play & Recording...")
            sd.wait()


            sf.write(record_filename, record_data, int(sample_rate))

            n = int(length)
            N = 2 ** n
            fs = int(sample_rate)
            normal_meanl, normal_meanr = sychronous_addition(record_filename, int(repeat), N,2)
            normal_tsp, normal_tsp_inv = normal_tsp_func(n)
            normal_tsp_inv_freq = np.fft.fft(normal_tsp_inv)

            H_normall = np.fft.fft(normal_meanl) * normal_tsp_inv_freq
            H_normalr = np.fft.fft(normal_meanr) * normal_tsp_inv_freq

            h_normall = np.fft.ifft(H_normall)
            h_normalr = np.fft.ifft(H_normalr)

            f = np.linspace(0, fs / 2, N // 2)



            h_normall2 = h_normall.real / max(abs(h_normall.real))
            h_normalr2 = h_normalr.real / max(abs(h_normalr.real))
            with open(str(datapath) + "/Impulse/L/"+str(count)+".DDB", "wb") as flout:
                for k in range(len(h_normall2)):
                    flout.write(struct.pack("d", h_normall2[k]))
            with open(str(datapath) + "/Impulse/R/"+str(count)+".DDB", "wb") as frout:
                for q in range(len(h_normalr2)):
                    frout.write(struct.pack("d", h_normalr2[q]))

            # スリープ設定
            for sleeptime in range(sleep_times):
                sys.stdout.write(str(sleep_times-sleeptime) + ' ')
                sys.stdout.flush()
                time.sleep(1)
