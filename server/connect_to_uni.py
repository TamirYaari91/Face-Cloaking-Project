import os
import paramiko

ssh_port = 22
my_username = "tamiryaari"
my_password = ""  # TODO - insert password here
nova = "nova.cs.tau.ac.il"
c_008 = "c-008.cs.tau.ac.il"
filename_for_original_image = "original.jpg"
filename_for_perturbated_image = "cloaked.jpg"
face_off_basepath = "/home/sharifm/teaching/uspw-0368-3544/2022-spring/group-04/face-off/"
filepath_for_original_image = face_off_basepath + "data/test_imgs/myface/"

margin = str(6)
amplification = str(3)
commands = \
    [
        "conda activate tf-gpu",
        "cd " + face_off_basepath,
        "python src/attack.py --source myface --pair-flag true --margin " + margin + " --amplification " + amplification
    ]

face_off_full_command = "\n".join(commands)

ls_myface = ["cd " + filepath_for_original_image, "ls"]
ls_myface_full_command = "\n".join(ls_myface)


def get_path_to_final_perturbation(lines):
    last_pert_ind = -1
    pic_ind = 0
    for i in range(len(lines) - 1, -1, -1):
        line_start = lines[i][0:8]
        if line_start == "SUCCESS!":
            last_pert_ind = i
            pic_ind += 1
            if pic_ind == 2:
                break
    return lines[last_pert_ind].split("to ")[-1][:-1]


def download_file_from_path(ssh_client, remote_file_path, local_file_path):
    ftp_client = ssh_client.open_sftp()
    ftp_client.get(remote_file_path, local_file_path)
    ftp_client.close()


def upload_file_from_path(ssh_client, remote_file_path, local_file_path):
    ftp_client = ssh_client.open_sftp()
    ftp_client.put(local_file_path, remote_file_path)
    ftp_client.close()


def delete_file_from_path(ssh_client, filepath, filename):
    del_command = "rm -f -r " + filepath + filename
    ssh_client.exec_command(del_command)


face_off_ret_val = ['Loading Images...\n',
                    'SUCCESS! Images written to /home/sharifm/teaching/uspw-0368-3544/2022-spring/group-04/face-off/data/new_adv_imgs/cw_l2/small_center/hinge_loss/full/cw_l2_small_center_h_loss_face_pic_bill_marg_5.40_amp_2.500.png\n',
                    'SUCCESS! Images written to /home/sharifm/teaching/uspw-0368-3544/2022-spring/group-04/face-off/data/new_adv_imgs/cw_l2/small_center/hinge_loss/crop/cw_l2_small_center_h_loss_face_pic_bill_marg_5.40_amp_2.500.png\n',
                    'Amplifying and Writing Images----------------------5.195116334129125\n',
                    'Saving Numpy Array---------------------------------0.01307652611285448\n',
                    'total running time =  165.0762403011322\n']


def connect_to_host(host, username, password, port):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, port, username, password)
    return ssh_client


def face_off_init(host, username, password, port, command):
    # Open connection
    ssh_client = connect_to_host(host, username, password, port)

    # Upload original image
    upload_file_from_path(ssh_client, filepath_for_original_image + filename_for_original_image,
                          os.getcwd() + '/' + filename_for_original_image)

    # Perform Face-Off
    stdin, stdout, stderr = ssh_client.exec_command(command)
    lines = stdout.readlines()
    # lines = face_off_ret_val

    # Delete original image
    delete_file_from_path(ssh_client, filepath_for_original_image, filename_for_original_image)

    # Download cloaked image
    final_perturbation_path = get_path_to_final_perturbation(lines)
    download_file_from_path(ssh_client, final_perturbation_path, os.getcwd() + '/' + filename_for_perturbated_image)

    # Close connection
    if ssh_client is not None:
        ssh_client.close()
        del ssh_client, stdin, stdout, stderr
    return lines


def face_off_wrapper():
    return face_off_init(c_008, my_username, my_password, ssh_port, face_off_full_command)


# res = face_off_wrapper()
