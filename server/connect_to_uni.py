import paramiko

ls = "ls -l"


def connect_to_nova(command):
    host = "nova.cs.tau.ac.il"
    port = 22
    username = "tamiryaari"
    password = ""  # TODO - insert password here

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    if ssh is not None:
        ssh.close()
        del ssh, stdin, stdout, stderr
    return lines


res = connect_to_nova(ls)
for i in range(len(res)):
    line = res[i].split(" ")
    if i > 0:
        print(line[-1])
