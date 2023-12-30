import sys, pdb, os, base64, time, datetime, locale, traceback, curses, urllib.request, urllib.parse, urllib.error, json
from threading import Thread
from os.path import basename
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection
os.system('cls')
while True:
          class Keyboard(Thread) :
              def __init__(self) :
                  Thread.__init__(self)
              def run(self):
                  global stop
                  stdscr = curses.initscr()
                  s = stdscr.getstr(20,0,1) 
                  stop = True
          
          class Ping(Thread) :
              def __init__(self) :
                  Thread.__init__(self)
              def run(self):
                  global iPing
                  global stop
                  global timePing
                  while not stop :
                      try :
                          req= urllib.request.Request(pingUrl)
                          req.add_header('User-Agent', "lte")
                          timePing = 0
                          timeStart = time.time()
                          rep =  (urllib.request.urlopen(req).read()).decode("utf-8")
                          timeStop = time.time()
                          if len(rep) == 0 :
                              iPing = -2
                          else :
                              iPing += 1
                              timePing = timeStop - timeStart
                          time.sleep(1)
                      except Exception as e :
                          iPing = -2
          
          class Stat(Thread) :
              def __init__(self) :
                  Thread.__init__(self)
              def run(self):
                  global stop
                  global timePing
                  stdscr = curses.initscr()
                  curses.start_color()
                  curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
                  curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
                  curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
                  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
                  curses.init_pair(69, curses.COLOR_CYAN, curses.COLOR_BLACK)
                  win = curses.newwin(22, 120, 0, 0)
                  win.scrollok(1)
                  while not stop :
                      bandRead = str(client.net.net_mode()["LTEBand"])
                      if band == -2 :
                          bandPrint = bandRead
                      else :
                          bandPrint = ""
                          for bandl in bandsList :
                              if bool(int(bandRead, 16) & int(bandl[3],16)) :
                                  bandPrint = bandPrint + bandl[1] + "-" + bandl[2] + " "
                      locale.setlocale(locale.LC_ALL, '') 
                      date = time.strftime('%d %B %Y - %H:%M:%S',time.localtime())

                      bdw = client.monitoring.traffic_statistics()
                      download = int(bdw['CurrentDownloadRate'])*8//(1024*1024)
                      upload = int(bdw['CurrentUploadRate'])*8//(1024*1024)

                      sig = client.device.signal()
                      rsrp = sig["rsrp"]
                      rsrq = sig["rsrq"]
                      sinr = sig["sinr"]
                      plmn = sig["plmn"]
                      cell_id = sig["cell_id"]

                      stat = client.monitoring.month_statistics()

                      dataUsed = int((int(stat["CurrentMonthDownload"]) + int(stat["CurrentMonthUpload"])) / (1024*1024*1024))
                      forfait = int(client.monitoring.start_date()["DataLimit"].replace("GB", "").replace("MB", ""))
                      dataAllowed = int((int(stat["MonthDuration"]) / (60 * 60 * 24)) * forfait / 31)
                      delta = dataAllowed - dataUsed
                      y = 1
                      win.erase()
                      win.addstr(y, 1, date , curses.color_pair(69)|curses.A_BOLD)
                      y += 2
                      win.addstr(y, 1, "Ping http : ", curses.color_pair(1))
                      if iPing == -2 :
                          win.addstr(y, 16, "KO", curses.color_pair(1)) 
                      elif iPing== -1 :
                          win.addstr(y, 16, "0", curses.color_pair(1))
                      else :
                          win.addstr(y, 16, str(iPing + 1), curses.color_pair(1))
                          if timePing != 0 :
                              win.addstr(y, 20, str(int(timePing * 1000)) + " ms", curses.color_pair(1))
                      win.addstr(4, 1,"Jaringan : ", curses.color_pair(1))
                      win.addstr(4, 16, "4G" if client.monitoring.status()["CurrentNetworkTypeEx"] != "1011" else "4G+"	      
                      , curses.color_pair(3) if client.monitoring.status()["CurrentNetworkTypeEx"] == "1011" else curses.color_pair(4))
                      y += 2
                      win.addstr(y, 1, "Band : ", curses.color_pair(1))
                      win.addstr(y, 16, bandPrint + "Mhz", curses.color_pair(1))
                      y += 2
                      win.addstr(y, 1, "rsrp :         " + str(rsrp), curses.color_pair(1))
                      y += 1
                      win.addstr(y, 1, "rsrq :         " + str(rsrq), curses.color_pair(1))
                      y += 1
                      win.addstr(y, 1, "sinr :         ",curses.color_pair(1))
                      win.addstr(y, 16, str(sinr), curses.color_pair(1))
                      
                      y += 1
                      win.addstr(y, 1, "cell_id :      " + str(cell_id), curses.color_pair(1))
                      y += 1
                      win.addstr(y, 1, "plmn :         " + str(plmn), curses.color_pair(1))
                      y += 2
                      win.addstr(y, 1, "Download :     " + str(download), curses.color_pair(1))
                      win.addstr(y, 20, "Mbit/s", curses.color_pair(1))

                      y += 1
                      win.addstr(y, 1, "Upload :       " + str(upload), curses.color_pair(1))
                      win.addstr(y, 20, "Mbit/s", curses.color_pair(1))
                      y += 2
                      win.addstr(y, 1, "Data used :    " + str(dataUsed), curses.color_pair(1))
                      win.addstr(y, 20, "Gbyte", curses.color_pair(1))
                      y += 2
                      win.refresh()
                      time.sleep(1)
                  curses.endwin()
          # Main program
          os.system('cls')
          stop = False
          iPing = -1
          timePing = 0
          rep = "OK"
          bandsList = [
              ('b1', 'FDD', '2100', '1'),
              ('b2', 'FDD', '1900', '2'),
              ('b3', 'FDD', '1800', '4'),
              ('b4', 'FDD', '1700', '8'),
              ('b5', 'FDD', '850', '10'),
              ('b6', 'FDD', '800', '20'),
              ('b7', 'FDD', '2600', '40'),
              ('b8', 'FDD', '900', '80'),
              ('b19', 'FDD', '850', '40000'),
              ('b20', 'FDD', '800', '80000'),
              ('b26', 'FDD', '850', '2000000'),
              ('b28', 'FDD', '700', '8000000'),
              ('b32', 'FDD', '1500', '80000000'),
              ('b38', 'TDD', '2600', '2000000000'),
              ('b40', 'TDD', '2300', '8000000000'),
              ('b41', 'TDD', '2500', '10000000000'),
              ('b42', 'TDD', '3500', '20000000000'),
          ]

          script_dir = os.path.dirname(os.path.realpath(__file__))
          config_path = os.path.join(script_dir, "config.json")
          with open(config_path, "r") as config_file:
              config_data = json.load(config_file)

          ip = config_data["ip"]
          password = config_data["password"]

          pingUrl = "http://www.google.com"
          band = -1
          keyboardThread = Keyboard() 
          statThread = Stat()
          pingThread = Ping()
          
          pil = input("═════════════════════\n        MENU         \n═════════════════════\n0. Check Network Status\n1. Band 1 (2100)\n2. Band 3 (1800)\n3. Band 8 (900)\n4. Band 1 (2100) + Band 3 (1800)\n5. Band 3 (1800) + Band 8 (900)\n6. Band 1 (2100) + Band 3 (1800) + Band 8 (900)\nq. Exit\n═════════════════════\nMasukkan Pilihan : ")
          with Connection('http://admin:indonesia@192.168.8.1/') as connection:
            client = Client(connection)
            if pil == '2':
                os.system('cls') 
                client.net.set_net_mode('4','3FFFFFFF','03')
                print("═════════════════════")
                print("SUCCESS CHANGE TO Band 3 (1800)")
            elif pil == '1':
                os.system('cls') 
                client.net.set_net_mode('3','3FFFFFFF','03')
                print("═════════════════════")
                print("SUCCESS CHANGE TO Band 1 (2100)")
            elif pil == '4':
                os.system('cls') 
                client.net.set_net_mode('5','3FFFFFFF','03')
                print("═════════════════════")
                print("SUCCESS CHANGE TO Band 1 + Band 3 (1800) (2100)")
            elif pil == '3':
                os.system('cls') 
                client.net.set_net_mode('80','3FFFFFFF','03')
                print("═════════════════════")
                print("SUCCESS CHANGE TO Band 8 (900)")
            elif pil == '6':
                os.system('cls') 
                client.net.set_net_mode('85','3FFFFFFF','03')
                print("═════════════════════")
                print("SUCCESS CHANGE TO Band 1 (2100) + Band 3 (1800) + Band 8 (900)")
            elif pil == '5':
                os.system('cls') 
                client.net.set_net_mode('84','3FFFFFFF','03')
                print("═════════════════════")
                print("SUCCESS CHANGE TO Band 3 (1800) + Band 8 (900)")
            elif pil == '0':
                try:
                    pingThread.start()
                    keyboardThread.start()
                    statThread.start()
                    keyboardThread.join()
                    statThread.join()
                except Exception as e :
                    os.system('cls')
                    print(e)
                    stop = True
                    keyboardThread.join()
                    statThread.join()
            elif pil.lower() == 'q':
                os.system('cls')
                break
            else:
                os.system('cls')