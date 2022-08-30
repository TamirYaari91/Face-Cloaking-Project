import os
import paramiko
import logging

ssh_port = 22
my_username = ""  # TODO - insert username here
my_password = ""  # TODO - insert password here
nova = "nova.cs.tau.ac.il"
c_005 = "c-005.cs.tau.ac.il"  # Chosen according to the average loads on TAU servers
filename_for_original_image = "original.jpg"
filename_for_perturbated_image_faceoff = "faceoff_perturbated.jpg"
faceoff_basepath = "/home/sharifm/teaching/uspw-0368-3544/2022-spring/group-04/face-off/"
filepath_for_original_image = faceoff_basepath + "data/test_imgs/myface/"

margin = str(6)  # default in Face-Off code
amplification = str(5.1)  # default in Face-Off code
commands = \
    [
        "conda activate tf-gpu",
        "cd " + faceoff_basepath,
        "python src/attack.py --source myface --pair-flag true --margin " + margin + " --amplification " + amplification
    ]

faceoff_full_command = "\n".join(commands)


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


def connect_to_host(host, username, password, port):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, port, username, password)
    return ssh_client


def faceoff_init(host, username, password, port, command, faceoff_error_dict):
    try:
        # Open connection
        ssh_client = connect_to_host(host, username, password, port)

        # Delete previous original image from UNI servers, if exists
        delete_file_from_path(ssh_client, filepath_for_original_image, filename_for_original_image)

        # Upload original image
        upload_file_from_path(ssh_client, filepath_for_original_image + filename_for_original_image,
                              os.getcwd() + '/' + filename_for_original_image)

        # Perform Face-Off
        stdin, stdout, stderr = ssh_client.exec_command(command)
        lines = stdout.readlines()

        # Download cloaked image
        final_perturbation_path = get_path_to_final_perturbation(lines)
        download_file_from_path(ssh_client, final_perturbation_path,
                                os.getcwd() + '/' + filename_for_perturbated_image_faceoff)

        # Delete original image from UNI servers
        delete_file_from_path(ssh_client, filepath_for_original_image, filename_for_original_image)

        # Close connection
        if ssh_client is not None:
            ssh_client.close()
            del ssh_client, stdin, stdout, stderr
        return lines
    except TimeoutError:
        faceoff_error_dict["error"] = "timeout"
    except Exception as e:
        faceoff_error_dict["error"] = "other"
        logging.exception(e)


def faceoff_wrapper(faceoff_error_dict):
    return faceoff_init(c_005, my_username, my_password, ssh_port, faceoff_full_command, faceoff_error_dict)
