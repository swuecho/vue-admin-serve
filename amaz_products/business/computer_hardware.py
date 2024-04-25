def cal_computer_spec_combination(diskSizeList, memSizeList, os: str):
    isPro = False if "home" in os.lower() else True
    combination = []
    for mem in memSizeList:
        for disk in diskSizeList:
            if isPro:
                combination.append((mem, disk, "pro"))
            else:
                combination.append((mem, disk, "pro"))
                combination.append((mem, disk, "home"))
    return combination
