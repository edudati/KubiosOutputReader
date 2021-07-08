import os
from os import listdir
from os.path import join


def main():
    path = 'Data'
    list_file = []
    """Main list with Header"""
    list_output = [
        ['FILE_NAME', 'DATE', 'TIME', 'VERSION', 'PARAMETERS ->', 'FILE_TYPE', 'CHANNEL_LABEL', 'DATA_LEGHT', 'LAMBDA',
         'AVG_HR', 'NNxx/pNNxx', 'Freq_VLF', 'Freq_LF', 'Freq_HF', 'INTERPOLATION', 'POINTS_FREQ_DOM',
         'FFT_OPTIONS_WIDTH', 'FFT_OPTIONS_OVERLAP', 'AR_MODEL', 'AR_FACTORIZATION', 'DETRENDING_NONLINEAR',
         'ENTROPY_DIMENSION', 'ENTROPY_TOLERANCE', 'DFA_short-term', 'DFA_long-term', 'INTERVAL_SAMPLES ->',
         'START_TIME_INTERVAL', 'END_TIME_INTERVAL', 'ARTIFACT_CORRECTION', 'ARTIFACT_%', 'RESULTS ->', 'PNS index',
         'SNS index', 'Stress index', 'Mean RR  (ms)', 'STD RR (ms)', 'Mean HR (beats/min)', 'STD HR (beats/min)',
         'Min HR (beats/min)', 'Max HR (beats/min)', 'RMSSD (ms)', 'NNxx (beats)', 'pNNxx (%)', 'SDANN (ms)',
         'SDNN index (ms)', 'RR tri index', 'TINN (ms)', 'VLF_FTT (Hz)', 'LF_FTT (Hz)', 'HF_FTT (Hz)', 'VLF_FTT (ms^2)',
         'LF_FTT (ms^2)', 'HF_FTT (ms^2)', 'VLF_FTT (log)', 'LF_FTT (log)', 'HF_FTT (log)', 'VLF_FTT (%)', 'LF_FTT (%)',
         'HF_FTT (%)', 'LF_FTT (nu)', 'HF_FTT (nu)', 'Total_PWR_FTT (ms^2)', 'LF/HF_FTT ratio', 'VLF_AR (Hz)',
         'LF_AR (Hz)', 'HF_AR (Hz)', 'VLF_AR (ms^2)', 'LF_AR (ms^2)', 'HF_AR (ms^2)', 'VLF_AR (log)', 'LF_AR (log)',
         'HF_AR (log)', 'VLF_AR (%)', 'LF_AR (%)', 'HF_AR (%)', 'LF_AR (nu)', 'HF_AR (nu)', 'Total_PWR_AR (ms^2)',
         'LF/HF_AR ratio', 'SD1 (ms)', 'SD2 (ms)', 'SD2/SD1 ratio', 'ApEn', 'SampEn', 'alpha 1', 'alpha 1']]

    """Check if the folder that will receive the files with RR intervals exists and create it if not"""
    new_path = 'RR_intervals'
    if not os.path.exists(join(path, new_path)):
        os.makedirs(join(path, new_path))

    """Read .txt files into the path"""
    for f in listdir(path):
        if join(path, f).endswith('.txt'):
            file = join(path, f)
            name = os.path.splitext(f)[0]

            with open(file, "r") as kubiosInput:

                """File Header"""
                list_input = [line.strip() for line in kubiosInput]
                list_file.append(file)  # NAME
                list_file.append(list_input[0].split(' ')[4])  # DATE
                list_file.append(list_input[0].split(' ')[5])  # TIME
                list_file.append(list_input[2])  # VERSION

                """Parameters"""
                list_file.append(" ")  # Division for Parameters
                list_file.append(list_input[9].split(' ')[2])  # FILE_TYPE
                list_file.append(list_input[10].split(': ')[1])  # CHANNEL_LABEL
                list_file.append(list_input[11].split(' ')[2])  # DATA_LENGHT
                list_file.append(list_input[16][43:46])  # LAMBDA
                for i in range(17, 36):  # Loop from 'AVG_HR' TO 'DFA_long-term'
                    if len(list_input[i].split(': ')) == 2:
                        list_file.append(list_input[i].split(': ')[1])

                """RR Interval Samples Selected"""
                list_file.append(" ")  # Division for Interval Samples
                list_file.append(list_input[39].split(',')[1].split('-')[0])  # START_TIME_INTERVAL
                list_file.append(list_input[39].split(',')[1].split('-')[1])  # END_TIME_INTERVAL
                list_file.append(list_input[41].split(': ')[1])  # ARTIFACT_CORRECTION
                list_file.append(str.strip(list_input[42].split(',')[1]))  # ARTIFACT_%

                """Results - Loop for Overview: From 'PNS index' to 'Stress index'  """
                list_file.append(" ")  # Division for Results
                for i in range(48, 51):
                    list_file.append(str.lstrip(list_input[i].split(',')[1]))

                """Results - Time-Domain: From 'Mean RR  (ms)' to 'TINN (ms)'  """
                for i in range(54, 68):
                    if list_input[i].split(',')[1] != "":
                        list_file.append(str.lstrip(list_input[i].split(',')[1]))

                """Results - Frequency-Domain FTT-spectrum: From 'VLF_FTT (Hz)' to 'LF/HF_FTT ratio'  """
                for i in range(71, 90):
                    if len(list_input[i].split(',')) != 2:
                        list_file.append(str.strip(list_input[i].split(',')[1]))

                """Results - Frequency-Domain AR-spectrum: From 'VLF_AR (Hz)' to 'LF/HF_AR ratio' """
                for i in range(71, 90):
                    if len(list_input[i].split(',')) != 2:
                        list_file.append(str.strip(list_input[i].split(',')[2]))

                """ Results - NonLinear: From 'SD1 (ms)' to 'alpha 1'  """
                for i in range(94, 102):
                    if len(list_input[i].split(',')) != 2:
                        list_file.append(str.strip(list_input[i].split(',')[1]))

                """add the file data as a 'new line' in the main list"""
                list_output.append(list_file.copy())
                list_file.clear()

                """Extract RR intervals to a list"""
                list_rr = []
                for i in range(109, len(list_input)):
                    if len(list_input[i].split(',')) > 1:
                        # print(list_input[i].split(',')[2])
                        list_rr.append(str.strip(list_input[i].split(',')[2]))

                """Create individual .txt files with only RR intervals"""
                with open('{}\{}_rr.txt'.format(join(path, new_path), name), "w") as output:
                    for number in list_rr:
                        output.write(number)
                        output.write("\n")
                    output.close()

    with open('{}\Output.csv'.format(path), "w") as output:
        for row in list_output:
            for collumn in row:
                output.write("{},".format(collumn))
            output.write("\n")
        output.close()


if __name__ == "__main__":
    main()
