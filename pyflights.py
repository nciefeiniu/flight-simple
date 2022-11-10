from air_company import AirlinesCompanies
from air_flight import AirFlight
from search_and_book_flight import SearchAndBookFlight


class Main:
    airlines_companies = AirlinesCompanies()

    def __init__(self):
        self.load_data()

    def load_data(self):
        self.airlines_companies.add_aircraft('SQ', 'Boeing 747')
        self.airlines_companies.add_cabin('SQ', 'Boeing 747', 'F', '1-1-1', 1, 10)
        self.airlines_companies.add_cabin('SQ', 'Boeing 747', 'J', '2-2-2', 11, 20)
        self.airlines_companies.add_cabin('SQ', 'Boeing 747', 'Y', '3-4-3', 21, 30)

        self.airlines_companies.add_aircraft('QF', 'Boeing 747')
        self.airlines_companies.add_cabin('QF', 'Boeing 747', 'F', '1-1-1', 1, 10)
        self.airlines_companies.add_cabin('QF', 'Boeing 747', 'J', '2-2-2', 11, 20)
        self.airlines_companies.add_cabin('QF', 'Boeing 747', 'Y', '3-4-3', 21, 30)

        def _add_flight(iata_code, out_flight_number, return_flight_number, origin_iata, des_iata, departure_time,
                        flight_time, stopover_duration, model, f_price, j_price, y_price):
            aircraft = self.airlines_companies.get_aircraft_by_name(iata_code, model)
            airflight = AirFlight(iata_code, out_flight_number, return_flight_number, origin_iata, des_iata,
                                  departure_time,
                                  flight_time, stopover_duration, aircraft)
            airflight.set_ticket_price('F', f_price)
            airflight.set_ticket_price('J', j_price)
            airflight.set_ticket_price('Y', y_price)

            self.airlines_companies.add_flight('SQ', airflight)

        all_flights = [
            'SQ, 123, 321, SIN, NRT, 5 Dec 22 10:00 AM, 6 hour 30 minute, 3 hour, Boeing 747, F, 2000, J, 1000, Y, 500',
            'SQ, 456, 654, SYD, SIN, 4 Dec 22 10:00 PM, 8 hour 0 minute, 2 hour, Boeing 747, F, 1500, J, 750, Y, 300',
            'SQ, 789, 987, SYD, NRT, 5 Dec 22 09:00 AM, 14 hour 0 minute, 2 hour, Boeing 747, F, 3500, J, 2500, Y, 1500',
            'QF, 789, 987, SYD, NRT, 5 Dec 22 01:00 PM, 14 hour 30 minute, 2 hour, Boeing 747, F, 3200, J, 2200, Y, 1200',
            'SQ, 123, 321, SIN, NRT, 12 Dec 22 10:00 AM, 6 hour 30 minute, 3 hour, Boeing 747, F, 2000, J, 1000, Y, 500',
            'SQ, 456, 654, SYD, SIN, 11 Dec 22 10:00 PM, 8 hour 0 minute, 2 hour, Boeing 747, F, 1500, J, 750, Y, 300',
            'SQ, 789, 987, SYD, NRT, 12 Dec 22 09:00 AM, 14 hour 0 minute, 2 hour, Boeing 747, F, 3500, J, 2500, Y, 1500',
            'QF, 789, 987, SYD, NRT, 12 Dec 22 01:00 PM, 14 hour 30 minute, 2 hour, Boeing 747, F, 3200, J, 2200, Y, 1200'
        ]
        for row in all_flights:
            _tmp = [_.strip() for _ in row.split(',')]
            _add_flight(_tmp[0], _tmp[1], _tmp[2], _tmp[3], _tmp[4], _tmp[5], _tmp[6], _tmp[7], _tmp[8], int(_tmp[10]),
                        int(_tmp[12]), int(_tmp[14]))

    @staticmethod
    def menu():
        print('-' * 50)
        print('1. Create Airline')
        print('2. Create Aircraft Type')
        print('3. Create Flight')
        print('4. Search and Book Flight')
        print('0. Exit the system')
        print('-' * 50)

    def run(self):
        _run = True
        while _run:
            self.menu()
            choice = input('>>>')
            if choice == '1':
                self.create_airline()
            elif choice == '2':
                self.create_aircraft_type()
            elif choice == '3':
                self.create_flight()
            elif choice == '4':
                self.search()
            elif choice == '0':
                _run = False
                print('bye-bye')
            else:
                print('Wrong selection, please select again')

    def create_airline(self):
        # 创建航空公司
        # :return:

        company_name = input('Please enter the name of the airline: ')
        iata_code = input('IATA Code: ')
        self.airlines_companies.add_company(company_name, iata_code)

    def create_aircraft_type(self):
        # 创建机型，并设置座位
        # :return:

        exists_code = self.airlines_companies.get_all_companies_code()  # 获取已经存在的航空公司代码
        iata_code = input('Airline IATA Code: ')
        if iata_code not in exists_code:
            print('The Airline IATA Code you entered does not exist. Please check and create it again')
            return
        aircraft_types = self.airlines_companies.get_company_aircraft_types(iata_code)  # 获取公司已经存在的所有机型
        aircraft_type_name = input('Aircraft Type Name: ')  # 机型
        if aircraft_type_name in aircraft_types:
            print('The model already exists, please try again')
            return

        self.airlines_companies.add_aircraft(iata_code, aircraft_type_name)  # 把这个机型加入到航空公司去

        def add_cabin(cabin_type, conf, start, end):
            # 这是增加座位配置
            self.airlines_companies.add_cabin(iata_code, aircraft_type_name, cabin_type, conf, start, end)

        add = input('Add Cabin Class? Y or N: ')
        if add.lower() == 'y':
            run = True
        else:
            run = False

        while run:
            # 添加座位
            ct = input('Cabin Class: ')
            sc = input('Seat Configuration: ')
            srn = int(input('Starting Row Number: '))
            ern = int(input('Ending Row Number: '))
            add_cabin(ct, sc, srn, ern)
            add = input('Add Cabin Class? Y or N: ')
            if add.lower() == 'y':
                run = True
            else:
                run = False
        # 完成后，需要输出信息
        print('-' * 50)
        print('Output:')
        print(f'Aircraft Type {aircraft_type_name} created for {iata_code}')

        aircraft = self.airlines_companies.get_aircraft_by_name(iata_code, aircraft_type_name)  # 这个机型
        if not aircraft:
            print("\033[4;33;45mSomething unexpected happened, please try again later\033[0m")
            return
        seats = 0
        for cabin in aircraft.cabins:
            print(
                f'Cabin Class {cabin.grade} – Seat {cabin.start_index()[0]} to {cabin.start_index()[-1]} through '
                f'{cabin.end_index()[0]} to {cabin.end_index()[-1]}, {cabin.number_of_seats()} seats')

            seats += cabin.number_of_seats()
        print(f'Total {seats} seats')

    def create_flight(self):
        # 创建航线
        # :return:

        exists_code = self.airlines_companies.get_all_companies_code()  # 获取已经存在的航空公司代码
        iata_code = input('Airline IATA Code: ')
        if iata_code not in exists_code:
            print('The Airline IATA Code you entered does not exist. Please check and create it again')
            return
        ofn = input('Outbound Flight Number: ')
        rfn = input('Return Flight Number (Optional): ')
        oa_IATA = input('Origin Airport IATA Code: ')
        da_IATA = input('Destination Airport IATA Code: ')
        departure_time = input('Departure Date/Time: ')
        flight_time = input('Flight Time: ')
        stopover_duration = input('Stopover Duration: ')
        aircraft_types = self.airlines_companies.get_company_aircraft_types(iata_code)  # 获取公司已经存在的所有机型
        if not aircraft_types:
            print("This airline does not have any available models, please increase the models first")
            return
        aircraft_type_name = input('Aircraft Type Name: ')  # 机型
        if aircraft_type_name not in aircraft_types:
            print('The model you entered does not exist, please check and enter again')
            return
        aircraft = self.airlines_companies.get_aircraft_by_name(iata_code, aircraft_type_name)

        _flight = AirFlight(iata_code=iata_code, out_flight_number=ofn, return_flight_number=rfn, origin_iata=oa_IATA,
                            des_iata=da_IATA, departure_time=departure_time, flight_time=flight_time,
                            stopover_duration=stopover_duration, aircraft=aircraft)  # 创建航线类

        print('Fare Amount: ')
        aircraft = self.airlines_companies.get_aircraft_by_name(iata_code, aircraft_type_name)  # 这个机型
        for seat_grade in [row.grade for row in aircraft.cabins]:
            price = input(f'Cabin Class {seat_grade} $: ')
            _flight.set_ticket_price(seat_grade, int(price))
        self.airlines_companies.add_flight(iata_code, _flight)
        print('-' * 50)
        print('Output:')
        print(f'Successfully configured this route, departure_time: {departure_time}. IATA code: {iata_code}.'
              f'Aircraft: {aircraft_type_name}. Outbound Flight Number: {ofn}, Return Flight Number (Optional): {rfn}'
              f'Origin Airport IATA Code: {oa_IATA}, Destination Airport IATA Code: {da_IATA}, Flight Time: {flight_time}'
              f'Stopover Duration: {stopover_duration}')

    def search(self):
        trip_type = input('Trip Type – One-Way (Return or One-Way, Default One-Way): ') or 'One-Way'
        origin = input('Origin: ')
        destination = input('Destination: ')
        departure_date = input('Departure Date: ')
        return_date = None
        if trip_type == 'Return':
            return_date = input('Return Departure Date: ')
        cabin_class = input('Cabin Class: (F, J, W, Y or No Preference)') or None
        p_number = int(input('Number of Passengers: '))
        search_handle = SearchAndBookFlight(trip_type, origin, destination, departure_date, cabin_class, p_number,
                                            return_date, self.airlines_companies)
        search_result, return_result = search_handle.search()  # 这里返回了2个结果，第一个是去程的，第二个是返程的（如果选了返程）。
        checked_seats = []
        checked_seats_return = []

        # 下面是显示以及选择航班

        check_flights = self.handle_search_result(cabin_class, p_number, search_result)  # 页面显示的这些航线
        select_flight = input('Select Flight（Enter 0 to return to the main menu））: ')  # 选择那个航班
        if select_flight == '0':
            return
        _select = int(select_flight.strip().split(' ')[1])
        selected_flight = check_flights[_select - 1]  # 选中的航班 数据是这样的：{'flight': AirFlight, 'grade': 'F'}
        print('Optional seats: ')
        can_choice_seat = []
        for seat in selected_flight['flight'].get_available_seat(grade=selected_flight['grade']):
            can_choice_seat.append(list(seat.keys())[0])
        print(can_choice_seat)
        print('*' * 50)

        for i in range(p_number):
            checked_seat = input(f'Select Seat for Passenger, This is the {i+1}th, {p_number} in all（Enter 0 to return to the main menu）')
            if checked_seat == '0':
                return
            checked_seats.append(checked_seat)

        if trip_type == 'Return':
            print('*' * 50)
            print('Select return flight: ')
            check_flights = self.handle_search_result(cabin_class, p_number, return_result)  # 页面显示的这些航线
            select_flight = input('Select Flight（Enter 0 to return to the main menu））: ')  # 选择那个航班
            if select_flight == '0':
                return
            _select = int(select_flight.strip().split(' ')[1])
            selected_flight_return = check_flights[_select - 1]  # 选中的航班 数据是这样的：{'flight': AirFlight, 'grade': 'F'}
            print('Optional seats: ')
            can_choice_seat = []
            for seat in selected_flight_return['flight'].get_available_seat(grade=selected_flight_return['grade']):
                can_choice_seat.append(list(seat.keys())[0])
            print(can_choice_seat)
            print('*' * 50)

            for i in range(p_number):
                checked_seat = input(
                    f'Select Seat for Passenger, This is the {i + 1}th, {p_number} in all（Enter 0 to return to the main menu）')
                if checked_seat == '0':
                    return
                checked_seats_return.append(checked_seat)

        for _s in checked_seats:
            selected_flight['flight'].book_air_tickets(_s)

        if trip_type == 'Return':
            for _s2 in checked_seats_return:
                selected_flight_return['flight'].book_air_tickets(_s2)

        _flight = selected_flight['flight']

        print(f'Your flight is confirmed. {_flight.iata_code} {_flight.out_flight_number}, '
              f'Departure Time: {_flight.departure_time}, '
              f'Estimated time of arrival: {_flight.arrive_time.strftime("%d %b %y %I:%M %p")},'
              f'Seat: {",".join(checked_seats)}')

        if trip_type == 'Return':
            _return_flight = selected_flight_return['flight']
            print(f'Return flight. {_flight.iata_code} {_flight.out_flight_number}, '
                  f'Departure Time: {_flight.departure_time}, '
                  f'Estimated time of arrival: {_flight.arrive_time.strftime("%d %b %y %I:%M %p")},'
                  f'Seat: {",".join(checked_seats)}')

    @staticmethod
    def handle_search_result(cabin_class, p_number, search_result) -> list:
        num = 1
        check_flights = []
        for index, flight in enumerate(search_result):
            print('-' * 50)
            if not cabin_class:
                ava_seats = flight.get_available_seat()  # {'1A': {'ava': 0, 'grade': "y"} }
                ava_grade_seats = {}  # 获取所有等级可用的座位量
                for row in ava_seats:
                    for k, v in row.items():
                        if v.get('ava') <= 0 and v.get('grade') not in ava_grade_seats:
                            ava_grade_seats[v.get('grade')] = 1
                        elif v.get('ava') <= 0 and v.get('grade') in ava_grade_seats:
                            ava_grade_seats[v.get('grade')] += 1
                for k, v in ava_grade_seats.items():
                    if v >= p_number:
                        print(f'Result {num}')
                        print(f'{flight.iata_code}{flight.out_flight_number}, {flight.origin_iata} to {flight.des_iata}, '
                              f'Depart {flight.departure_time}, '
                              f'Arrive {flight.arrive_time.strftime("%d %b %y %I:%M %p")}, Class {k}'
                              f' ${flight.price.get(k.upper())}')
                        check_flights.append({'flight': flight, 'grade': k.upper()})
                        print('*' * 50)
                        num += 1
            else:
                print(f'Result {num}')
                print(f'{flight.iata_code}{flight.out_flight_number}, {flight.origin_iata} to {flight.des_iata}, Depart {flight.departure_time}, '
                      f'Arrive {flight.arrive_time.strftime("%d %b %y %I:%M %p")}, '
                      f'Class {cabin_class} ${flight.price.get(cabin_class.upper())}')
                print('*' * 50)
                num += 1
                check_flights.append({'flight': flight, 'grade': cabin_class.upper()})
        return check_flights


if __name__ == '__main__':
    Main().run()

