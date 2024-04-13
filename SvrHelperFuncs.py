import os
import shutil

tf_file_dir = r"D:\SteamLibrary\steamapps\common\Team Fortress 2\tf" # set tf folder here
svr_file_dir = r"D:\svr\data\cfg" # set cfg folder for SVR here
prec_file_dir = r"D:\SteamLibrary\steamapps\common\Team Fortress 2\tf\demos" # set prec folder here

demo_length_bytes_location = 1063
i_neg_offset = -2000
i_pos_offset = 200
demo_ffw_factor = 5

stadium_exec = 'stadiumfog'
arena2_exec = 'arena2fog'


def get_demo_list(path):  # function to get list of titles in cfg file
    titles_txt = open(path, "r")  # open titles file
    demos = titles_txt.read()  # read titles into string
    demos_list = demos.split("\n")  # split string into list
    titles_txt.close()  # close file
    return demos_list  # return list


def get_demo_length(title):  # get length of demo from title
    demo = open(prec_file_dir + r'\\' + title.replace(r'"', '') + ".dem", "rb")  # open demo file
    tick = demo.read(demo_length_bytes_location)  # read first 1063 bytes for the 3 bytes containing tick length
    demo.close()  # close file
    tick = int.from_bytes(tick[-3:], 'little')  # convert last 3 bytes to int
    return tick  # return length in an integer


def clean_demo_title(title):  # make an os-safe filename for the recordings
    title = title.replace('\'', '')
    title = title.replace('(', '')
    title = title.replace(')', '')
    title = title.replace('\"', '')
    return title


def get_demo_ticks(title):  # grab ticks from Killstreaks.txt for a certain demo in prec dir
    print(title)
    killstreaks_txt = open(prec_file_dir + r'\\' + "Killstreaks.txt")  # open killstreak file
    bookmarks = killstreaks_txt.read()  # read file as string into var
    killstreaks_txt.close()  # close file
    bookmarks_list = bookmarks.split("\n\n")  # split killstreaks string across two newlines
    demo = [i for i in bookmarks_list if title in i]  # list comprehension to get only list elements with title
    # print(demo)
    demo = demo[0].split("\n")  # split these elements across newline
    length = len(demo)  # very bad way to iterate across elements of that list
    # print(length)
    ticks = []
        # try:
    for i in range(0, length):
        # print(demo[i])
        demo[i] = demo[i].split(" ")  # split elements across space
        # print(i)
        # print(demo[i])
        print(demo[i][6].strip(")"))
        ticks.append(int(demo[i][6].strip(")")))  # get whatever comes after 6 spaces ie the tick
        # except:
        # print(demo[i])
    # print(demo)
    # print(ticks)
    return ticks


def intersection(i1, i2):  # determine if two intervals intersect
    if i1[0] <= i2[0] <= i1[1] or i2[0] <= i1[0] <= i2[1]:  # probably a better way to do this
        # possible refactor: i2[0] - i1[0] <= i1[1] - i1[0] or i1[0] - i2[0] <= i2[1] - i2[0]
        return 1
    else:
        return 0


def distance(i1, i2):  # determine distance between two intervals
    d = max(i1[0], i2[0]) - min(i1[1], i2[1])
    return d


def union(i1, i2):  # create the union of two intervals
    u = (min(i1[0], i2[0]), max(i2[1], i1[1]))
    return u


def complement(intervals, end):  # create the complement of a set of intervals
    complement_intervals = [(0, intervals[0][0])]
    for i in range(1, len(intervals)):
        complement_intervals.append((intervals[i-1][1], intervals[i][0]))
    complement_intervals.append((intervals[len(intervals)-1][1], end))
    return complement_intervals

def generate_intervals(ticks, end):
    intervals = [(max(0, ticks[0]+i_neg_offset), min(end, ticks[0]+i_pos_offset))]
    j = 0
    for i in range(1, len(ticks)):
        candidate = (max(0, ticks[i]+i_neg_offset), min(end, ticks[i]+i_pos_offset))
        if intersection(candidate, intervals[j]):
            intervals[j] = union(candidate, intervals[j])
        else:
            intervals.append(candidate)
            j = j+1
    print(intervals)
    return intervals


def generate_vdm(title, next_title, ci, stop=0):
    exec_cfg = 'autosvr_default'
    if ('pass_arena2' in title) or ('goalfix_conveyor3' in title):
        exec_cfg = arena2_exec
    if 'pass_stadium' in title:
        exec_cfg = stadium_exec
    print(exec_cfg)

    vdm = open(prec_file_dir + r'\\vdm\\' + title.replace(r'"', '') + ".vdm", "w")
    vdm.write("demoactions\n{\n")
    j = 1
    k = 0

    vdm.write(f'\t"{j}"\n')
    j = j + 1
    vdm.write("\t{\n")
    vdm.write("\t\tfactory \"PlayCommands\"\n")
    vdm.write(f'\t\tname "execcfg{j}"\n')
    vdm.write(f'\t\tstarttick "{0}"\n')
    vdm.write(f'\t\tcommands "exec {exec_cfg}"\n')
    vdm.write("\t}\n")

    for i in range(0, len(ci)-1):
        vdm.write("\t\"" + str(j) + "\"\n")
        j = j + 1
        vdm.write("\t{\n")
        vdm.write("\t\tfactory \"ChangePlaybackRate\"\n")
        vdm.write("\t\tname \"changerate" + str(j) + "\"\n")
        vdm.write("\t\tstarttick \"" + str(ci[i][0]) + "\"\n")
        vdm.write("\t\tstoptick \"" + str(ci[i][1]) + "\"\n")
        vdm.write("\t\tplaybackrate \"" + str(demo_ffw_factor) + "\"\n")
        vdm.write("\t}\n")

        vdm.write("\t\"" + str(j) + "\"\n")
        j = j + 1
        vdm.write("\t{\n")
        vdm.write("\t\tfactory \"ChangePlaybackRate\"\n")
        vdm.write("\t\tname \"changerate" + str(j) + "\"\n")
        vdm.write("\t\tstarttick \"" + str(ci[i][1]) + "\"\n")
        vdm.write("\t\tstoptick \"" + str(ci[i][1]) + "\"\n")
        vdm.write("\t\tplaybackrate \"" + str(1) + "\"\n")
        vdm.write("\t}\n")

        vdm.write("\t\"" + str(j) + "\"\n")
        j = j + 1
        vdm.write("\t{\n")
        vdm.write("\t\tfactory \"PlayCommands\"\n")
        vdm.write("\t\tname \"startrecord" + str(j) + "\"\n")
        vdm.write("\t\tstarttick \"" + str(ci[i][1]+1) + "\"\n")
        vdm.write("\t\tcommands \"startmovie " + clean_demo_title(title).replace(r'"', '') + '_' + str(i) + "\"\n")
        vdm.write("\t}\n")

        vdm.write("\t\"" + str(j) + "\"\n")
        j = j + 1
        vdm.write("\t{\n")
        vdm.write("\t\tfactory \"PlayCommands\"\n")
        vdm.write("\t\tname \"stoprecord" + str(j) + "\"\n")
        vdm.write("\t\tstarttick \"" + str(ci[i+1][0]-2) + "\"\n")
        vdm.write("\t\tcommands \"endmovie\"\n")
        vdm.write("\t}\n")
        k = k + 1
        print(i)

    print(j)
    if stop:
        vdm.write("\t\"" + str(j) + "\"\n")
        vdm.write("\t{\n")
        vdm.write("\t\tfactory \"PlayCommands\"\n")
        vdm.write("\t\tname \"nextdemo" + str(j) + "\"\n")
        vdm.write("\t\tstarttick \"" + str(min(ci[k][0] + 100, ci[-1][1])-1) + "\"\n")
        vdm.write("\t\tcommands \"stopdemo\"\n")
        vdm.write("\t}\n")
    else:
        vdm.write("\t\"" + str(j) + "\"\n")
        vdm.write("\t{\n")
        vdm.write("\t\tfactory \"PlayCommands\"\n")
        vdm.write("\t\tname \"nextdemo" + str(j) + "\"\n")
        vdm.write("\t\tstarttick \"" + str(min(ci[k][0] + 100, ci[-1][1])-1) + "\"\n")
        vdm.write("\t\tcommands \"playdemo " + next_title.replace("\"", "") + "\"\n")
        vdm.write("\t}\n")
    vdm.write("}")
    vdm.close()


def copy_files(title):
    # os.popen(f'copy {prec_file_dir}\\{title}.dem {tf_file_dir}\\{title}.dem')
    # os.popen(f'copy {prec_file_dir}\\vdm\\{title}.vdm {tf_file_dir}\\{title}.vdm')
    title = title.replace(r'"', '')
    source_demo = f'{prec_file_dir}\\{title}.dem'
    source_vdm = f'{prec_file_dir}\\vdm\\{title}.vdm'
    dest_demo = f'{tf_file_dir}\\{title}.dem'
    dest_vdm = f'{tf_file_dir}\\{title}.vdm'
    shutil.copyfile(source_demo, dest_demo)
    shutil.copyfile(source_vdm, dest_vdm)

# print(get_demo_list()[0])
# demo_list = get_demo_list()
# print(get_demo_length(demo_list[0]))
#
# title = demo_list[0]
# ticks = get_demo_ticks(title)
# length = get_demo_length(title)
# intervals = generate_intervals(ticks, length)
# print(complement(intervals, length))
# complement_intervals = complement(intervals, length)
# generate_vdm(title, demo_list[1], complement_intervals)


