import re
import os
from glob import glob
import fnmatch


# mc_elec_str = r'wine ~/.wine/drive_c/Program\ Files/Multi\ Channel\ Systems/MC_DataTool/MC_DataTool.com -bin -i "%input_filename%" -o "%output_filename%" -s "Electrode Raw Data:21" -s "Electrode Raw Data:31" -s "Electrode Raw Data:41" -s "Electrode Raw Data:51" -s "Electrode Raw Data:61" -s "Electrode Raw Data:71" -s "Electrode Raw Data:12" -s "Electrode Raw Data:22" -s "Electrode Raw Data:32" -s "Electrode Raw Data:42" -s "Electrode Raw Data:52" -s "Electrode Raw Data:62" -s "Electrode Raw Data:72" -s "Electrode Raw Data:82" -s "Electrode Raw Data:13" -s "Electrode Raw Data:23" -s "Electrode Raw Data:33" -s "Electrode Raw Data:43" -s "Electrode Raw Data:53" -s "Electrode Raw Data:63" -s "Electrode Raw Data:73" -s "Electrode Raw Data:83" -s "Electrode Raw Data:14" -s "Electrode Raw Data:24" -s "Electrode Raw Data:34" -s "Electrode Raw Data:44" -s "Electrode Raw Data:54" -s "Electrode Raw Data:64" -s "Electrode Raw Data:74" -s "Electrode Raw Data:84" -s "Electrode Raw Data:15" -s "Electrode Raw Data:25" -s "Electrode Raw Data:35" -s "Electrode Raw Data:45" -s "Electrode Raw Data:55" -s "Electrode Raw Data:65" -s "Electrode Raw Data:75" -s "Electrode Raw Data:85" -s "Electrode Raw Data:16" -s "Electrode Raw Data:26" -s "Electrode Raw Data:36" -s "Electrode Raw Data:46" -s "Electrode Raw Data:56" -s "Electrode Raw Data:66" -s "Electrode Raw Data:76" -s "Electrode Raw Data:86" -s "Electrode Raw Data:17" -s "Electrode Raw Data:27" -s "Electrode Raw Data:37" -s "Electrode Raw Data:47" -s "Electrode Raw Data:57" -s "Electrode Raw Data:67" -s "Electrode Raw Data:77" -s "Electrode Raw Data:87" -s "Electrode Raw Data:28" -s "Electrode Raw Data:38" -s "Electrode Raw Data:48" -s "Electrode Raw Data:58" -s "Electrode Raw Data:68" -s "Electrode Raw Data:78" -WriteHeader -ToSigned'
mc_elec_str = r'wine ~/.wine/drive_c/Program\ Files/Multi\ Channel\ Systems/MC_DataTool/MC_DataTool.com -bin -i "%input_filename%" -o "%output_filename%" -s "El" -WriteHeader -ToSigned'

# mc_analog_str = r'wine ~/.wine/drive_c/Program\ Files/Multi\ Channel\ Systems/MC_DataTool/MC_DataTool.com -bin -i "%input_filename%" -o "%output_filename%" -s "Analog Raw Data:A1" -WriteHeader -ToSigned'
mc_analog_str = r'wine ~/.wine/drive_c/Program\ Files/Multi\ Channel\ Systems/MC_DataTool/MC_DataTool.com -bin -i "%input_filename%" -o "%output_filename%" -s "An" -WriteHeader -ToSigned'

def convert_mcd(filename):
    """Convert .mcd to .raw and .analog binary files."""

    # os.system('wine wineboot --init')
    name, ext = os.path.splitext(filename)

    electrical = re.sub('%input_filename%', filename, mc_elec_str)
    electrical = re.sub('%output_filename%', name + '.raw', electrical)
    print("> " + electrical)
    os.system(electrical)

    analog = re.sub('%input_filename%', filename, mc_analog_str)
    analog = re.sub('%output_filename%', name + '.analog', analog)
    os.system(analog)

def find_mcd_files(directory):
    """Find paths of mcd files in directory that are not yet processed."""

    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.mcd'):
            name, ext = os.path.splitext(filename)

            # only add if .raw does not exist
            if os.path.isfile(os.path.join(root, name + '.raw')):
                print(filename + " has already been processed.")
            else:
                matches.append(os.path.join(root, filename))

    return matches

if __name__ == '__main__':
    mcd_files = find_mcd_files('/data')
    for mcd in mcd_files:
        convert_mcd(mcd)
    print("Finished processing!")
