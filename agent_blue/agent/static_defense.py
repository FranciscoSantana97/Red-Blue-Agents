import os
import json
import datetime
from subprocess import run, PIPE


class StaticDefense():

	def _cmd_run(self, command):
		result = run(command, stdout=PIPE, stderr=PIPE,
					 universal_newlines=True, shell=True)
		return result

	# basic configuration check
	def basic_check(self, json_file=None):

		result_dir = os.getcwd() + "/agent/static_result"
		if not os.path.exists(result_dir):
			os.mkdir(result_dir)
		result = open(result_dir + "/basic_check_result.txt", "a+", encoding="utf-8")
		result.write("[[ Start Date : %s ]]\n" % datetime.datetime.now())

		command = "sudo find / -type d -perm -0002 -exec ls -dl {} \; 2>/dev/null"
		write_other_dir = self._cmd_run(command)
		result.write("[ Write Permission at directory with other user ]\n\n")
		result.write(write_other_dir.stdout + "\n")

		command = "sudo find / -type f -perm -0002 -exec ls -al {} \; 2>/dev/null"
		write_other_file = self._cmd_run(command)
		result.write("[ Write Permission at file with other user ]\n\n")
		result.write(write_other_file.stdout + "\n")

		command = "sudo find / -type d -perm -2000 -o -perm -4000 -exec ls -dl {} \; 2>/dev/null"
		setuid_n_gid_dir = self._cmd_run(command)
		result.write("[ Directory with SETUID/SETGID ]\n\n")
		result.write(setuid_n_gid_dir.stdout + "\n")

		command = "sudo find / -type f -perm -2000 -o -perm -4000 -exec ls -al {} \; 2>/dev/null"
		setuid_n_gid_file = self._cmd_run(command)
		result.write("[ File with SETUID/SETGID ]\n\n")
		result.write(setuid_n_gid_file.stdout + "\n")

		command = "sudo find / -type f -name '*.conf' -perm -0002 -exec ls -al {} \; 2>/dev/null"
		write_other_conf = self._cmd_run(command)
		result.write("[ Write Permission at configure file with other user ]\n\n")
		result.write(write_other_conf.stdout + "\n")

		command = "sudo find / -name '*.sudo_as_admin_successful' -exec ls -dl {} \; 2>/dev/null"
		read_other_sudolog = self._cmd_run(command)
		result.write("[ SUDO AS ADMIN SUCCESSFUL file ]\n\n")
		result.write(read_other_sudolog.stdout + "\n")

		command = "sudo cat /etc/passwd | awk -F: '$3 == 0 { print $1}' 2>/dev/null"
		superuser_info = self._cmd_run(command)
		result.write("[ SuperUser Information ]\n\n")
		result.write(superuser_info.stdout + "\n")

		command = "awk -F: '($2 == "") {print}' /etc/shadow 2>/dev/null"
		user_without_pwd = self._cmd_run(command)
		result.write("[ User without password ]\n\n")
		result.write(user_without_pwd.stdout + "\n")

		# command = "lpstat -a 2>/dev/null"
		# conn_printer_info = self._cmd_run(command)

		command = "sudo ps -ef | grep root | grep -v grep 2>/dev/null"
		root_proc_info = self._cmd_run(command)
		result.write("[ Process list with root privilege ]\n\n")
		result.write(root_proc_info.stdout + "\n")

		command = "sudo find / -name '*.rhost' -exec ls -dl {} \; 2>/dev/null"
		rhost_file_info = self._cmd_run(command)
		result.write("[ rhost file list ]\n\n")
		result.write(rhost_file_info.stdout + "\n")

		if(json_file is not None):
			result.write("[ Customized File result ]\n\n")
			with open(json_file, 'r') as file:
				data = json.load(file)
				for cmd in data["commands"]:
					file_cmd = self._cmd_run(cmd)
					if(file_cmd.returncode == 0):
						result.write(file_cmd.stdout + "\n")
						print("Command '" + cmd + "' executed SUCCESSFULLY.")
					else:
						print("Error at execute '" + cmd + "'.")

		result.close()

	# enable linux rsyslog
	def enable_log(self):

		command = "dpkg -l | grep rsyslog 2>/dev/null"
		rsyslog_chk = self._cmd_run(command)

		if(rsyslog_chk.stdout == ""):
			command = "sudo apt-get install -y rsyslog"
			install_rsyslog = self._cmd_run(command)

		command = "sudo sed -i 's/\#cron\.\*/cron\.\*/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#daemon\.\*/daemon\.\*/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#kern\.\*/kern\.\*/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#lpr\.\*/lpr\.\*/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#mail\.\*/mail\.\*/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#user\.\*/user\.\*/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)

		command = "sudo sed -i 's/\#mail\.info/mail\.info/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#mail\.warn/mail\.warn/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#mail\.err/mail\.err/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)

		command = "sudo sed -i 's/\#\*\.\=debug/\*\.\=debug/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#	auth\,authpriv\.none\;/	auth\,authpriv\.none\;/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#	news\.none\;mail\.none/	news\.none\;mail\.none/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)

		command = "sudo sed -i 's/\#\*\.\=info\;\*\.\=notice\;\*\.\=warn/\*\.\=info\;\*\.\=notice\;\*\.\=warn/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#	cron\,daemon\.none/	cron\,daemon\.none/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)
		command = "sudo sed -i 's/\#	mail\,news\.none/	mail\,news\.none/' /etc/rsyslog.d/50-default.conf"
		self._cmd_run(command)

		command = "sudo service rsyslog status | grep Active: | awk -F ' ' '{print $2}'"
		rsyslog_status = self._cmd_run(command)
		print(rsyslog_status)

		if(rsyslog_status.stdout == "active\n"):
			command = "sudo service rsyslog restart"
		else:
			command = "sudo service rsyslog start"
		service_result = self._cmd_run(command)
		if(service_result.returncode == 0):
			print("rsyslog service started SUCCESSFULLY.")
		else:
			print("Error at rsyslog service start")

	# change misconfiguration
	def change_file(self, json_file=None):
		sudoers_path = "/etc/sudoers"
		log_dir = os.getcwd() + "/agent/static_result"
		if not os.path.exists(log_dir):
			os.mkdir(log_dir)
		result = open(log_dir + "/change_log.txt", "a+", encoding="utf-8")
		result.write("[[ Start Date : %s ]]\n" % datetime.datetime.now())

		with open(sudoers_path, 'r') as r:
			lines = r.readlines()
		with open(sudoers_path, 'w') as f:
			for line in lines:
				if not("NOPASSWD" in line and "/usr/bin/find" in line):
					f.write(line)
				else:
					result.write("Removed line : " + line + "\n\n")

		if(json_file is not None):
			with open(json_file, 'r') as file:
				data = json.load(file)
				for idx in data:
					for file_data in data[idx]:
						file_path = file_data["file_path"]
						keywords = file_data["keywords"]
						if(os.path.exists(file_path)):
							with open(file_path, 'r') as r:
								lines = r.readlines()
							with open(file_path, 'w') as w:
								for line in lines:
									if not any(word in line for word in keywords):
										w.write(line)
									else:
										result.write(line)
							print("File change DONE with '" + file_path + "'.")
						else:
							print("Error at '" + file_path + "'. File not exists.")
		result.close()
