import re
import os
from glob import glob
import fnmatch

# mc_elec_str = r'wine ~/.wine/drive_c/Program\ Files/Multi\ Channel\ Systems/MC_DataTool/MC_DataTool.com -bin -i "%input_filename%" -o "%output_filename%" -s "Electrode Raw Data:21" -s "Electrode Raw Data:31" -s "Electrode Raw Data:41" -s "Electrode Raw Data:51" -s "Electrode Raw Data:61" -s "Electrode Raw Data:71" -s "Electrode Raw Data:12" -s "Electrode Raw Data:22" -s "Electrode Raw Data:32" -s "Electrode Raw Data:42" -s "Electrode Raw Data:52" -s "Electrode Raw Data:62" -s "Electrode Raw Data:72" -s "Electrode Raw Data:82" -s "Electrode Raw Data:13" -s "Electrode Raw Data:23" -s "Electrode Raw Data:33" -s "Electrode Raw Data:43" -s "Electrode Raw Data:53" -s "Electrode Raw Data:63" -s "Electrode Raw Data:73" -s "Electrode Raw Data:83" -s "Electrode Raw Data:14" -s "Electrode Raw Data:24" -s "Electrode Raw Data:34" -s "Electrode Raw Data:44" -s "Electrode Raw Data:54" -s "Electrode Raw Data:64" -s "Electrode Raw Data:74" -s "Electrode Raw Data:84" -s "Electrode Raw Data:15" -s "Electrode Raw Data:25" -s "Electrode Raw Data:35" -s "Electrode Raw Data:45" -s "Electrode Raw Data:55" -s "Electrode Raw Data:65" -s "Electrode Raw Data:75" -s "Electrode Raw Data:85" -s "Electrode Raw Data:16" -s "Electrode Raw Data:26" -s "Electrode Raw Data:36" -s "Electrode Raw Data:46" -s "Electrode Raw Data:56" -s "Electrode Raw Data:66" -s "Electrode Raw Data:76" -s "Electrode Raw Data:86" -s "Electrode Raw Data:17" -s "Electrode Raw Data:27" -s "Electrode Raw Data:37" -s "Electrode Raw Data:47" -s "Electrode Raw Data:57" -s "Electrode Raw Data:67" -s "Electrode Raw Data:77" -s "Electrode Raw Data:87" -s "Electrode Raw Data:28" -s "Electrode Raw Data:38" -s "Electrode Raw Data:48" -s "Electrode Raw Data:58" -s "Electrode Raw Data:68" -s "Electrode Raw Data:78" -WriteHeader -ToSigned'
mc_elec_str = r'wine ~/.wine/drive_c/Program\ Files/Multi\ Channel\ Systems/MC_DataTool/MC_DataTool.com -bin -i "%input_filename%" -o "%output_filename%" -s "El" -WriteHeader -ToSigned'

# mc_analog_str = r'wine ~/.wine/drive_c/Program\ Files/Multi\ Channel\ Systems/MC_DataTool/MC_DataTool.com -bin -i "%input_filename%" -o "%output_filename%" -s "Analog Raw Data:A1" -WriteHeader -ToSigned'
mc_analog_str = r'wine ~/.wine/drive_c/Program\ Files/Multi\ Channel\ Systems/MC_DataTool/MC_DataTool.com -bin -i "%input_filename%" -o "%output_filename%" -s "An" -WriteHeader -ToSigned'


def convert_mcd(filename):
    """Convert .mcd to .raw and .analog binary files.

    Uses Wine and requires MC Datatool to be installed."""

    # os.system('wine wineboot --init')
    name, ext = os.path.splitext(filename)
    elec_file = name + '.raw'

    electrical = re.sub('%input_filename%', filename, mc_elec_str)
    electrical = re.sub('%output_filename%', elec_file, electrical)
    os.system(electrical)

    analog_file = name + '.alg'
    analog = re.sub('%input_filename%', filename, mc_analog_str)
    analog = re.sub('%output_filename%', analog_file, analog)
    os.system(analog)

    return (elec_file, analog_file)


def find_mcd_files(directory):
    """Find paths of mcd files in directory that are not yet processed.

    For .voltages, basename is matched while .raw looks for exact name. (e.g. name0001)"""
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.mcd'):
            filepath = os.path.join(root, filename)
            # only add if .voltages and .raw do not exist
            if (check_for_file(filepath, 'voltages')):
                # don't process
                print(filename + " has already been processed into voltages.")
            elif (check_for_file(filepath, 'raw')):
                # don't process
                print(filename + " has already been processed into raw.")
            else:
                matches.append(os.path.join(root, filename))
    return matches


def find_raw_files(directory):
    """Search directory for .raw files, return list."""
    matches = []

    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.raw'):
            filepath = os.path.join(root, filename)
            # only add if .voltages does not exist
            if check_for_file(filepath, 'voltages'):
                # don't process
                print(filename + " has already been processed into voltages.")
            else:
                matches.append(filepath)

    return matches


def find_analog_files(directory):
    """Search directory for .alg files, return list."""
    matches = []

    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.alg'):
            filepath = os.path.join(root, filename)
            # only add if .voltages does not exist
            if check_for_file(filepath, 'analog'):
                # don't process
                print(filename + " has already been processed into analog.")
            else:
                matches.append(filepath)

    return matches


def check_for_file(filepath, ext):
    """Return boolean if a .{{ext}} file exists with path & name of filepath."""
    rest_regex = re.compile('^(.+)(\d{4})\.\w+$')
    first_regex = re.compile('^(.+)\.\w+$')

    match = re.match(rest_regex, filepath)
    if not match:
        match = re.match(first_regex, filepath)
    if match:
        if os.path.isfile(match.group(1) + "." + ext):
            return True
        else:
            return False
    else:
        raise('Bad filepath {}'.format(filepath))

def fix_header(filename):
    """Change MCS .raw header encoding from Windows-1252 to UTF-8.

    A new .data file will be created. To launch, type 'glia' on the command
    line."""


    name, ext = os.path.splitext(filename)

    header_end = "EOH\r\n".encode("Windows-1252")
    newfile_name = name + '.voltages'

    # if file exists, do not run
    if os.path.isfile(newfile_name):
        return

    with open(filename, mode='rb') as file:
        with open(newfile_name, 'wb') as newfile:
            for line in file:
                if line == header_end:
                    newfile.write(header_end)
                    break
                newline = line.decode("Windows-1252", errors='replace')
                newline = re.sub('µ', 'u', newline)
                newfile.write(newline.encode("Windows-1252"))

            next_chunk = "placeholder"
            while next_chunk != b'':
                next_chunk = file.read(2**28)
                newfile.write(next_chunk)

    # delete old file
    os.remove(filename)
    return newfile_name


def merge_raw_files(files_to_merge, output_file_name):
    """Take multiple MCS raw files with header and combine into one file.

    Copies header from first file. Assumes exported as int16 from MCS
    DataTool."""
    print("Now merging", files_to_merge)
    # copy header
    header = open(files_to_merge[0], mode='rb')
    with open(output_file_name, 'wb') as newfile:
        # read header from file then write to newfile
        for line in header:
            newfile.write(line)
            if line == b"EOH\r\n":
                break
        header.close()
        
        chunksize = 8192 
        
        for file in files_to_merge:
            with open(file, "rb") as f:
                while True:
                    chunk = f.read(chunksize)
                    if chunk:
                        newfile.write(chunk)
                    else:
                        break


def sort_split_files(filenames):
    """Takes list of filename and returns a dictionary of related files with base name as key."""
    out_files = {}

    def append_to_out_files(base_name, fn):
        if base_name in out_files:
            out_files[base_name].append(fn)
        else:
            out_files[base_name] = [fn]

    rest_regex = re.compile('^(.+)(\d{4})\.\w+$')
    first_regex = re.compile('^(.+)\.\w+$')
    for fn in filenames:
        # look for rest first to catch the \d{4}
        rest_match = re.match(rest_regex, fn)
        if rest_match:
            base_name = rest_match.group(1)
            append_to_out_files(base_name, fn)
            continue

        first_match = re.match(first_regex, fn)
        if first_match:
            base_name = first_match.group(1)
            append_to_out_files(base_name, fn)


    # ensure order is 0,1,2,3 and validate
    for k, v in out_files.items():
        v.sort()
        l = len(v)
        match = re.match(rest_regex, v[l-1])

        if int(match.group(2)) + 1 != l:
            raise("Missing an mcd file for {}".match.group(1))

    return out_files


def delete_files(files):
    for f in files:
        os.remove(f)

if __name__ == '__main__':
    mcd_files = find_mcd_files('/data')
    for mcd in mcd_files:
        elec_file, analog_file = convert_mcd(mcd)
    to_combine = find_raw_files('/data')
    raw_files = sort_split_files(to_combine)
    to_combine = find_analog_files('/data')
    analog_files = sort_split_files(to_combine)



    for k, v in raw_files.items():
        if len(v) > 0:
            name, ext = os.path.splitext(v[0])
            merge_raw_files(v, name + '.voltages')
            delete_files(v)

    for k, v in analog_files.items():
        if len(v) > 0:
            name, ext = os.path.splitext(v[0])
            merge_raw_files(v, name + '.analog')
            delete_files(v)

    print("Finished processing!")
