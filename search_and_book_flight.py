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
                                self.cabin_class), []
        elif self.trip_type == 'Return':
            a = self._search(self.origin, self.destination, self.departure_date, self.number_of_passengers,
                             self.cabin_class)
            b = self._search(self.destination, self.origin, self.return_date, self.number_of_passengers,
                             self.cabin_class)
            return a, b
        else:
            print('Wrong Trip Type entered')
            return [], []

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

    def _search_transfer(self):
        pass