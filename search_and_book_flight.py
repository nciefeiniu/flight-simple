from datetime import datetime, timedelta

from air_company import AirlinesCompanies


class SearchAndBookFlight:
    def __init__(self, trip_type, origin, destination, departure_date, cabin_class, number_of_passengers,
                 return_date, companies: AirlinesCompanies):
        # :param trip_type:  单向还是往返
        # :param origin:  出发地代码
        # :param destination:   目的地代码
        # :param departure_date: 出发时间
        # :param cabin_class: 座舱的等级
        # :param number_of_passengers: 预定人数
        # :param return_date: 返回时间
        # :param companies: 航空公司管理类

        self.trip_type = trip_type
        self.origin = origin
        self.destination = destination
        self.departure_date = datetime.strptime(departure_date, '%d %b %y')  # 出发时间
        self.cabin_class = cabin_class
        self.number_of_passengers = int(number_of_passengers)
        self.return_date = return_date
        self.airline_companies = companies

    def search(self):
        if self.trip_type == 'One-Way':
            return self._search(self.origin, self.destination, self.departure_date, self.number_of_passengers,
                                self.cabin_class), [], self._search_transfer(self.origin, self.destination,
                                                                             self.departure_date,
                                                                             self.number_of_passengers,
                                                                             self.cabin_class), []
        elif self.trip_type == 'Return':
            a = self._search(self.origin, self.destination, self.departure_date, self.number_of_passengers,
                             self.cabin_class)
            b = self._search(self.destination, self.origin, self.return_date, self.number_of_passengers,
                             self.cabin_class)
            c = self._search_transfer(self.origin, self.destination, self.departure_date, self.number_of_passengers,
                                      self.cabin_class)  # 中转航班
            d = self._search_transfer(self.destination, self.origin, self.return_date, self.number_of_passengers,
                                      self.cabin_class)  # 中转航班
            return a, b, c, d
        else:
            print('Wrong Trip Type entered')
            return [], [], [], []

    def _search(self, start_code, end_code, departure_date, number_of_passengers, cabin_class=None) -> list:
        _s_d = departure_date - timedelta(days=1)
        _e_d = (departure_date + timedelta(days=1)).replace(hour=23, minute=59, second=59)
        result = []
        for company in self.airline_companies.companies:
            for flight in company.flights:
                if flight.origin_iata == start_code and flight.des_iata == end_code and \
                        _s_d <= datetime.strptime(flight.departure_time, '%d %b %y %I:%M %p') <= _e_d:
                    ava_seat = flight.get_available_seat(cabin_class)
                    if len(ava_seat) >= number_of_passengers:
                        result.append(flight)
        return result

    def _search_transfer(self, start_code, end_code, departure_date, number_of_passengers, cabin_class=None) -> list:
        # 这是搜索带中转的航班
        _s_d = departure_date - timedelta(days=1)
        _e_d = (departure_date + timedelta(days=1)).replace(hour=23, minute=59, second=59)
        result = {}
        # 第一步，先把所有出发地的飞机选出来，按航空公司分组（座位需要满足要求）
        for company in self.airline_companies.companies:
            for flight in company.flights:
                if flight.origin_iata == start_code and flight.des_iata != end_code and \
                        _s_d <= datetime.strptime(flight.departure_time, '%d %b %y %I:%M %p') <= _e_d:
                    ava_seat = flight.get_available_seat(cabin_class)
                    if len(ava_seat) >= number_of_passengers:
                        if flight.iata_code not in result:
                            result[flight.iata_code] = {'start': [flight]}
                        else:
                            result[flight.iata_code]['start'].append(flight)
        # 第二步，找出到达地点是需要的飞机，按航空公司分组（座位需要满足要求）
        for company in self.airline_companies.companies:
            for flight in company.flights:
                if flight.origin_iata != start_code and flight.des_iata == end_code and \
                        _s_d <= datetime.strptime(flight.departure_time, '%d %b %y %I:%M %p') <= _e_d:
                    ava_seat = flight.get_available_seat(cabin_class)
                    if len(ava_seat) >= number_of_passengers:
                        if flight.iata_code in result:
                            if 'end' not in result[flight.iata_code]:
                                result[flight.iata_code]['end'] = [flight]
                            else:
                                result[flight.iata_code]['end'].append(flight)

        ava_transfer_flights = []
        # 第三步，找出合理的中转飞机，第一个航班的到达时间和第二个航班的出发时间要在1小时以上。以及第一个航班的到达地点和第二个航班的出发地点一致
        for flight_iata_code, flights in result.items():
            if not flights.get('end'):
                continue
            first_flights = flights['start']
            second_flights = flights['end']
            for _flight in first_flights:
                for _flight_2 in second_flights:
                    if _flight.des_iata == _flight_2.origin_iata and \
                            (datetime.strptime(_flight.departure_time, '%d %b %y %I:%M %p') + timedelta(
                                hours=1)) < _flight_2.arrive_time:
                        # 如果 第一个航班的到达地是 第二个航班的出发地，并且中间相隔在一个小时以上，那就是可行的中转航班
                        ava_transfer_flights.append([_flight, _flight_2])
        return ava_transfer_flights
