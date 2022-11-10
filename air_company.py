from air_flight import AirFlight
from aircraft import Aircraft


class AirCompany:
    # 航空公司
    aircraft_types = []  # 这家航空公司有哪些机型
    flights = []  # 这家航空公司有哪些航线

    def __init__(self, name: str, airline_code: str, aircraft_types=None, flights=None):
        self.name = name  # 航空公司名
        if flights is None:
            flights = []
        if aircraft_types is None:
            aircraft_types = []
        self.airline_code = airline_code  # IATA Code 国际航空运输协会代码
        self.aircraft_types = aircraft_types
        self.flights = flights

    def add_flight(self, flight: AirFlight):
        # 增加航线
        self.flights.append(flight)

    def add_aircraft_type(self, aircraft_type: Aircraft):
        # 增加机型
        if aircraft_type.model in [row.model for row in self.aircraft_types]:
            print('This model already exists, discard')
            return
        self.aircraft_types.append(aircraft_type)

    def get_all_flight(self) -> list:
        # 获取该公司所有航线，返回的是 AirFlight 类
        return self.flights

    def get_all_aircraft_types(self):
        # 获取所有机型
        return self.aircraft_types

    def get_aircraft_type_by_model(self, model) -> Aircraft or None:
        for row in self.aircraft_types:
            if row.model == model:
                return row
        return None


class SingaporeAirlines(AirCompany):
    # 新加坡航空公司
    def __init__(self, aircraft_types=None, flights=None):
        super(SingaporeAirlines, self).__init__(name='Singapore Airlines', airline_code='SQ',
                                                aircraft_types=aircraft_types, flights=flights)


class QantasAirlines(AirCompany):
    # Qantas航空公司
    def __init__(self, aircraft_types=None, flights=None):
        super(QantasAirlines, self).__init__(name='Qantas', airline_code='QF',
                                             aircraft_types=aircraft_types, flights=flights)


class AirlinesCompanies:
    # 航空公司组，也就是所有航空公司的集合，所有的航空公司都会在这里面
    companies = []

    def __init__(self):
        self.companies += [SingaporeAirlines(), QantasAirlines()]

    def add_company(self, company_name, airline_code):
        # 增加航空公司
        if company_name in [com.name for com in self.companies]:
            print('Duplicate company name')
            return
        if airline_code in [com.airline_code for com in self.companies]:
            print('Duplicate airline code')
            return
        self.companies.append(AirCompany(name=company_name, airline_code=airline_code))
        print(f'Successful Wearing Airline. company name: {company_name}, airline_code: {airline_code}')

    def add_cabin(self, iata_code, aircraft_type, cabin_type, conf, start_num, end_num):
        # 增加座位配置
        # :param iata_code: 航空公司代码
        # :param aircraft_type: 机型名字
        # :param cabin_type: 座位等级，Y、F、J
        # :param conf:  座位配置，1-1-1 2-2-2 3-4-3
        # :param start_num: 位置起始行
        # :param end_num:  位置结束行
        # :return:

        aircraft = self.get_aircraft_by_name(iata_code, aircraft_type)  # 获取到这个机型
        if not aircraft:
            print('The model you need is not found')
            return
        try:
            aircraft.add_cabin(cabin_type, conf, start_num, end_num)
        except ValueError:
            print(ValueError)
            return
        # print(f'Aircraft Type {aircraft_type} created for {iata_code}')

    def _get_company_by_iata_code(self, iata_code) -> AirCompany:
        # 根据iata_code代码，找到这家航空公司
        company = None
        for com in self.companies:
            if com.airline_code == iata_code:
                company = com
        return company

    def get_aircraft_by_name(self, iata_code, name) -> Aircraft:
        # 根据iata_code和name获取这个机型，这里是拿到机型这个类，如果拿不到，就返回的None
        company = self._get_company_by_iata_code(iata_code)
        if not company:
            print('The airline you entered is not found')
            return None
        return company.get_aircraft_type_by_model(name)

    def get_all_companies_code(self):
        return [com.airline_code for com in self.companies]

    def get_company_aircraft_types(self, iata_code):
        # 获取某家航空公司的所有机型
        company = self._get_company_by_iata_code(iata_code)
        if not company:
            print('The airline you entered is not found')
            return []
        return [air.model for air in company.get_all_aircraft_types()]

    def add_aircraft(self, iata_code, model):
        # 添加机型
        # :param iata_code: 航空公司代码
        # :param model: 飞机型号
        # :return:

        company = self._get_company_by_iata_code(iata_code)
        if not company:
            print('The airline you entered is not found')
            return
        # print(f'开始添加： ', company.__dict__)
        company.add_aircraft_type(Aircraft(iata_code, model))

    def add_flight(self, iata_code, flight: AirFlight):
        company = self._get_company_by_iata_code(iata_code)
        company.add_flight(flight)


if __name__ == '__main__':
    test = SingaporeAirlines()
