import time

sec = 0
while True:
    print ("SLEEP ... [" + str(sec) + " / 60s ]")
    if sec >= 60:
        break
    time.sleep(5)
    sec += 5
