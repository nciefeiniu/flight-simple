from datetime import datetime, timedelta
from aircraft import Aircraft


class AirFlight:
    # 飞机类

    def __init__(self, iata_code: str, out_flight_number: str, return_flight_number, origin_iata: str, des_iata: str,
                 departure_time: str, flight_time: str, stopover_duration: str, aircraft: Aircraft):
        self.seat_info = {}  # 座位信息，是否被预定
        self.iata_code = iata_code  # 航空公司代码
        self.out_flight_number = out_flight_number  # 出发航班号
        self.return_flight_number = return_flight_number  # 返回航班号
        self.origin_iata = origin_iata  # 出发机场代码
        self.des_iata = des_iata  # 目的地机场代码
        self.departure_time = departure_time  # 出发时间
        self.flight_time = flight_time  # 飞行时间
        self.stopover_duration = stopover_duration  # 停机时间
        self.aircraft = aircraft  # 机型
        self.seat_info = self.aircraft.get_cabin_info()  # 座位信息，这里可以存储是否被购买

        format_flight_time = flight_time.replace(' ', '')
        self.arrive_time = datetime.strptime(departure_time, '%d %b %y %I:%M %p') + \
                           timedelta(hours=int(format_flight_time.split('hour')[0]),
                                     minutes=int(format_flight_time.split('hour')[1].split('minute')[0]))
        self.all_cabin = self.aircraft.get_all_cabin()
        self.price = {}  # 票价

    def set_ticket_price(self, grade: str, price: int):
        # 设定票价，这里需要知道这个机型有哪些票价等级
        if grade not in self.all_cabin:
            raise ValueError('This Grade not in this aircraft')
        self.price[grade.upper()] = price

    def get_available_seat(self, grade=None) -> list:
        # {'1A': {'ava': 0, 'grade': "y"} }
        if not grade:
            return [{k: v} for k, v in self.seat_info.items() if v.get('ava') <= 0]
        else:
            return [{k: v} for k, v in self.seat_info.items() if v.get('ava') <= 0 and v.get('grade').lower() == grade.lower()]

    def book_air_tickets(self, seat_mark):
        # :param seat_mark: 座位编号
        # :return:

        if not seat_mark:
            print('Cannot be empty')
            return
        # print('当前预定的：',)
        seat_info = self.seat_info.get(seat_mark)
        if not seat_info:
            print('The seat information is not found')
            return
        self.seat_info[seat_mark].update({'ava': 1})