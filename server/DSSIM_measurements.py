import os

original_images_folder_path = "/Users/tamiryaari/Desktop/UNI/Year3/FCP/Testing/OriginalImages"
cloaked_images_folder_base_path = "/Users/tamiryaari/Desktop/UNI/Year3/FCP/Testing/TestingNumberOfIterations/FinalCloakedImages"


def calc_dssim(folder_num):
    retval = 0
    output_filename = "dssim" + folder_num + ".txt"
    files = os.listdir(original_images_folder_path)

    with open(output_filename, 'a') as f:
        for file in files:
            if ".jpeg" in file or ".jpg" in file:
                command = "dssim " + original_images_folder_path + "/" + file + " " + cloaked_images_folder_base_path + folder_num + "/" + file
                output = os.popen(command).read()
                output = [val.strip() for val in output.split('\t')]
                string_to_append = file + "," + output[0] + "\n"
                f.write(string_to_append)
                retval += float(output[0])

    return [retval, len(files)]


folder_nums = ["100", "150", "200", "250", "300"]

# for num in folder_nums:
#     res = calc_dssim(num)
#     print("average dssim for " + num + " iterations = " + str(res[0] / res[1]))


# calc_dssim(folder_nums[0])


def remove_whitespace(path):
    files = os.listdir(path)
    for file in files:
        file_without_space = file.replace(" ", "")
        old_name = path + "/" + file
        new_name = path + "/" + file_without_space
        os.rename(old_name, new_name)

# remove_whitespace(original_images_folder_path)

# for num in folder_nums:
#     folder_path = cloaked_images_folder_base_path + num
#     remove_whitespace(folder_path)
