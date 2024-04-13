import SvrHelperFuncs
import os

svr_file_dir = r"D:\svr\data\cfg" # set cfg folder for SVR here
prec_file_dir = r"D:\SteamLibrary\steamapps\common\Team Fortress 2\tf\demos" # set prec demos folder here
title_keyword = 'RecordTitles'

prec_files = os.listdir(prec_file_dir)
title_files = [f for f in prec_files if (os.path.isfile(os.path.join(prec_file_dir, f)) and f.startswith(title_keyword)
                                         and f.endswith('.txt'))]

for f in title_files:
    demo_list = SvrHelperFuncs.get_demo_list(os.path.join(prec_file_dir, f))
    first_title = demo_list[-1]
    print(first_title)
    first_ticks = SvrHelperFuncs.get_demo_ticks(first_title)
    print(first_ticks)
    first_length = SvrHelperFuncs.get_demo_length(first_title)
    print(first_length)
    first_intervals = SvrHelperFuncs.generate_intervals(first_ticks, first_length)
    print(first_intervals)
    first_ci = SvrHelperFuncs.complement(first_intervals, first_length)
    SvrHelperFuncs.generate_vdm(first_title, "shart", first_ci, stop=1)
    SvrHelperFuncs.copy_files(first_title)

    for i in range(0, len(demo_list)-1):
        title = demo_list[i]
        ticks = SvrHelperFuncs.get_demo_ticks(title)
        length = SvrHelperFuncs.get_demo_length(title)
        intervals = SvrHelperFuncs.generate_intervals(ticks, length)
        ci = SvrHelperFuncs.complement(intervals, length)
        SvrHelperFuncs.generate_vdm(title, demo_list[i+1], ci)
        SvrHelperFuncs.copy_files(title)

    print(demo_list)
