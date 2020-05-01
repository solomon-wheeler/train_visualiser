import requests
import json
import pygame
import time

cyan = (0, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
x = 600
y = 600
firstline = int(y / 2)
swrline = int(y / 3)
gwrline = int((y * 2) / 3)
down = int(x / 20)
pygame.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)


class trains():

    def __init__(self):
        self.screen = pygame.display.set_mode((x, y))
        self.key = ""
        data = None
        self.cords = []
        self.cords_swr = []
        self.cords_gwr = []
        self.firststations = []
        self.swrstations = []
        self.gwrstations = []
        self.crs_codes = [["RDG", "EAR", "WTI", "WNS", "WKM"],
                          ['BCE', 'MAO', 'ACT', 'SNG', 'LNG', 'VIR', 'EGH', 'SNS', 'FEL', 'TWI', 'RMD', 'CLJ',
                           'WAT'],
                          ['CRN', 'SND', 'BAW', 'FNN', 'NCM', 'ASH', 'GLD', 'SFR', 'CHL', 'GOM',"DKT" 'DPD', 'BTO', 'REI',
                           'RDH']]

        self.names_first_stations = ["Reading", "Earley", "Winnersh Triangle", "Winnersh", "Wokingham"]
        self.names_swr_stations = ["Bracknell", "Martins Heron", "Ascot ", "Sunningdale", "Longcross",
                                   "Virginia Water", "Egham", "Staines", "Feltham", "Twickenham", "Richmond ",
                                   "Clapham Junction", "Waterloo"]
        self.names_gwr_stations = ["Crowthorne", "Sandhurst", "Blackwater", "Farnbourough", "North Camp", "Ash",
                                   "Guildford", "Shalford", "Chilworth", "Gomshall","Dorking West", "Dorking Deppdene", "Betchworth",
                                   "Reigate", "Redhill"]  # Include gatwick?

    def setup(self):

        for x in self.names_first_stations:
            self.firststations.append(myfont.render(x, 1, cyan))
        for x in self.names_swr_stations:
            self.swrstations.append(myfont.render(x, 1, blue))
        for x in self.names_gwr_stations:
            self.gwrstations.append(myfont.render(x, 1, green))

    def setupdraw(self):
        downCur = 0
        x = 600
        y = 600
        firstline = int(y / 2)
        swrline = int(y / 3)
        gwrline = int((y * 2) / 3)
        down = int(x / 20)
        first_working = []
        cords_swr_working = []
        cords_gwr_working = []
        for count in range(0, len(self.names_first_stations)):
            #  print(str(len(firststations)))
            downCur = down * count
            self.screen.blit(self.firststations[count], (firstline, downCur))
            first_working.append([firstline, downCur])
        endpos = downCur
        self.cords.append(first_working)
        for count in range(0, len(self.names_swr_stations)):
            downCur = down * (count + len(self.names_first_stations))
            self.screen.blit(self.swrstations[count], (swrline, downCur))
            cords_swr_working.append([swrline, downCur])
        self.cords.append(cords_swr_working)

        endposswr = downCur
        for count in range(0, len(self.names_gwr_stations)):
            downCur = down * (count + len(self.names_first_stations))
            self.screen.blit(self.gwrstations[count], (gwrline, downCur))
            cords_gwr_working.append([gwrline, downCur])
        self.cords.append(cords_gwr_working)
        endposgwr = downCur

        pygame.draw.aaline(self.screen, cyan, (firstline, 0), (firstline, endpos))
        pygame.draw.aaline(self.screen, blue, (firstline, endpos), (swrline, endpos))
        pygame.draw.aaline(self.screen, green, (firstline, endpos), (gwrline, endpos))

        pygame.draw.aaline(self.screen, blue, (swrline, endpos), (swrline, endposswr))
        pygame.draw.aaline(self.screen, green, (gwrline, endpos), (gwrline, endposgwr))
        pygame.display.flip()

    def find_individual(self, line, station):
        y = 0
        if station == None:
            print("FOund none")
            return None
        else:
            for individual_station in line:
                if individual_station in station:
                    return y
                y += 1
            return None

    def addTrain(self, station, destination, amount, last_stop_name):
        done = False
        done_last = False
        overall_done = 0
        this_line_done = 0
        for line in self.crs_codes:
            position_located = self.find_individual(line, station)
            if position_located is not None:
                posi = self.cords[overall_done][position_located]
                done = True
                break
            overall_done += 1
        for line in self.crs_codes:
            position_located = self.find_individual(line, last_stop_name)
            if position_located is not None:
                posi_last = self.cords[this_line_done][position_located]
                done_last = True
                break
            this_line_done += 1
        if done == True:
            if done_last == True:
                difference_in_y = posi_last[1] - posi[1]
                distance_done = int(difference_in_y * amount)
            else:
                distance_done = 0
            if "Reading" in destination:
                posi1 = posi[0] - 10
            else:
                posi1 = posi[0] + 10
            pygame.draw.rect(self.screen, white, pygame.Rect(posi1, posi[1] + distance_done, 10, 10))
            pygame.display.flip()

    def subFinder(self):
        last_stop_time = None
        current_time = time.strftime("%H:%M", time.localtime())
        current_time = current_time.split(":")
        for currentstop in self.data['trainServices']:
            last_stop_time = None
            last_stop_name = None
            s = 0
            done = False
            destination = currentstop['destination'][0]['locationName']
            for x in currentstop['previousCallingPointsList'][0]['previousCallingPoints']:
                # print("working")
                if x['at'] == "On time":
                    work = x['st']
                else:
                    work = x['at']
                if work == None or work == "No report":
                    work = x['st']
                work = work.split(":")
                name = x['crs']
                # print(work)
                # print(name)
                if self.is_after(work) == True:
                    if done == False:
                        if last_stop_time != None:
                            amount = self.amount_through(work, last_stop_time)
                        else:
                            amount = 0
                        print(str(work))
                        print(str(name))
                        self.addTrain(name, destination, amount, last_stop_name)
                        done = True
                last_stop_time = work
                last_stop_name = name

    def is_after(self, station_time):
        current_time = time.strftime("%H:%M", time.localtime())
        current_time = current_time.split(":")
        comb_current_time = (int(current_time[0]) * 60) + int(current_time[1])
        comb_station_time = (int(station_time[0]) * 60) + int(station_time[1])
        if comb_current_time - comb_station_time > 720:
            comb_station_time += 1440
        if comb_station_time > comb_current_time and (comb_station_time - comb_current_time) < 30:
            return True
        else:
            return False

    def amount_through(self, station_time, last_station_time):
        current_time = time.strftime("%H:%M", time.localtime())
        current_time = current_time.split(":")
        comb_current_time = (int(current_time[0]) * 60) + int(current_time[1])
        comb_station_time = (int(station_time[0]) * 60) + int(station_time[1])
        comb_last_station_time = (int(last_station_time[0]) * 60) + int(last_station_time[1])
        if comb_station_time - comb_last_station_time < -720:
            comb_last_station_time += 1440
        difference_between_stops = comb_station_time - comb_last_station_time
        if comb_station_time - comb_current_time < -720:
            comb_current_time += 1440
        difference_between_actual = comb_station_time - comb_current_time  #
        if difference_between_stops == 0:
            return 0

        return float(difference_between_actual / difference_between_stops)

    def GetData(self, crs_code, via):
        response = ["WORKING HTTP RESPONSE = 200",
                    "HTTP RESPONSE = 400 Bad request, something was wrong in your request, double check the URL is correct especially api/v2.0/XXX and that the CRS code is correct",
                    "HTTP RESPONSE = 401 The national rail api key is wrong, if it's new wait 15 minutes, else double check its correct",
                    "HTTP RESPONSE = 429 Ohhh you sneeky devil thats way to many requests, calm yourself down",
                    "HTTP RESPONSE = 500, there has been a problem with the depature board io service, could be a problem with national rail or it can be a dodby request, check the request is ok",
                    "HTTP RESPONSE = 503, Like everything else national rail is involved with the national rail Data Portal ins't working at the moment, try again soon"]
        if via is None:
            paramaters = {"apiKey": self.key, "numServices": 10, "timeWindow": 120}
        else:
            paramaters = {"apiKey": self.key, "numServices": 10, "timeWindow": 120, "filterStation": via}
        r = requests.get(url="https://api.departureboard.io/api/v2.0/getArrivalsByCRS/" + crs_code + "/",
                         params=paramaters)
        self.data = r.json()
        stringr = str(r)
        if "200" in stringr:
            print(response[0])
        elif "400" in stringr:
            print(response[1])
        elif "401" in stringr:
            print(response[2])
        elif "429" in stringr:
            print(response[3])
        elif "500" in stringr:
            print(response[4])
        elif "503" in stringr:
            print(response[5])
        else:
            print("I'm sorry but you are properly screwed")
        #print(json.dumps(self.data, indent=3, sort_keys=True))
        if self.data['trainServices'] != None:
            self.subFinder()
        else:
            print("No services found")

this_data = trains()
this_data.setup()
for x in range(0, 80):
    this_data.screen.fill(black)
    this_data.setupdraw()
    this_data.GetData("RDG", "WKM")
    this_data.GetData("WAT", "WKM")
    this_data.GetData("RDH", "WKM")  # Need to cahnge once full service is resumed
    time.sleep(20)
    pygame.image.save(this_data.screen, "screenshot" + str(x) + ".jpg")

# pygame.event.get()  #
# x = input("Tpye something to finish")
