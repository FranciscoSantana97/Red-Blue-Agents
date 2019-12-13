import json
import os
import hashlib
import shutil


class Monitor():
    # install osqueryd
    # def install_osqueryd():
    #   command = "sudo sh " + os.cwd() + "/install/install_osqueryd.sh"
    #   if (os.system("%s" % (command)) != 0):
    #       print("Installing osqueryd Failed......")
    #       sys.exit()
    #   else:
    #       print("osqueryd Installed")

    def file_hash(self, filelist):
        jsonData = {}

        for i in filelist:
            # filelist[i] 가 file path임
            f = open(filelist[i], 'rb')
            data = f.read()
            f.close()

            hashed = hashlib.md5(data)
            jsonData[i] = hashed.hexdigest()
            # 경로 변경 필요
            backupPath = os.getcwd() + "/agent/backup/"
            if (not(os.path.exists(backupPath))):
                os.mkdir(backupPath)
            shutil.copy2(filelist[i], backupPath + i)
            print("Done with File Backup")

            self._add_mon_file(i, filelist[i])

        with open(os.getcwd() + '/agent/json/file_hash.json', 'w+') as output:
            json.dump(jsonData, output)

        command = "systemctl restart osqueryd"
        p = os.system("%s" % (command))
        print("Restart osqueryd")

    def _add_mon_file(self, filename, path):
        innerData = []
        
        with open(os.getcwd() + "/agent/json/user_fim.json", "r") as file:
            data = json.load(file)
            innerData.append(path)
            data["file_paths"][filename] = innerData

        jsonVal = json.dumps(data)

        with open("/usr/share/osquery/packs/fim.conf", "w") as file:
            file.write(jsonVal)
        print("Done with Add fim.conf file")

    def monitoring(self, filelist, ctime):
        with open("/var/log/osquery/osqueryd.results.log",
                  "r+", os.O_NONBLOCK) as file:
            data = file.readlines()
        with open(os.getcwd() + '/agent/json/file_hash.json', 'r') as hashfile:
            hashdata = json.load(hashfile)
        files = []
        changed = 0
        for i in filelist:
            files.append(filelist[i])
        for i in data:
            jsData = json.loads(i)
            if "columns" in jsData:
                if "target_path" in jsData["columns"]:
                    if jsData["columns"]["target_path"] in files:
                        if "action" in jsData["columns"]:
                            if jsData["columns"]["action"] == "UPDATED":
                                if jsData["columns"]["ctime"] != '':
                                    if int(jsData["columns"]["ctime"]) > ctime:
                                        tmp = jsData["columns"]["target_path"].split("/")
                                        if jsData["columns"]["md5"] != hashdata[tmp[-1]]:
                                            backupPath = os.getcwd() + "/agent/backup/"
                                            command = "cp " + backupPath + tmp[-1] + " " + jsData["columns"]["target_path"]
                                            p = os.system("%s" % (command))
                                            print("File Changed.")
                                            changed = 1

            if changed == 1:
                log_path = "/var/log/osquery/osqueryd.results.log"
                log_backup_path = os.getcwd() + "/agent/backup/osqueryd.results.log.bak"
                if os.path.exists(log_backup_path):
                    command = "cat " + log_path + " >> " + log_backup_path
                else:
                    command = "cp " + log_path + " " + log_backup_path
                p = os.system("%s" % (command))
                command = "cat /dev/null > " + log_path
                p = os.system("%s" % (command))
