# 飞机类(包含机型和座位)


GRADE_SETTING = {'F': '1-1-1', 'J': '2-2-2', 'Y': '3-4-3'}


class Seat:
    # 座位类
    def __init__(self, grade: str, config: str, start: int, end: int):
        if grade not in list(GRADE_SETTING.keys()):
            raise ValueError('Grade error')
        self.grade = grade
        if config not in list(GRADE_SETTING.values()):
            raise ValueError('Seat configuration error')
        self.config = config
        if start > end:
            raise ValueError('start cannot be less than end')
        if start < 0:
            raise ValueError('The starting value cannot be less than 1')
        self.start = start
        self.end = end
        self.seat_info = self._get_seat_info()  # 这是座位的信息，编号是key，value是代表这个座位是否被遇到，0代表未被定，1是被预定了

    def _get_seat_info(self) -> dict:
        all_seat = []
        for ss in self.all_seat_mark():
            all_seat += ss
        return dict(zip(all_seat, [{'ava': 0, 'grade': self.grade} for i in range(len(all_seat))]))

    def _gen_seat_mark(self) -> range:
        # 这是一排座位的编号，A、B、C、D。。。。。
        # :return:

        if self.grade == 'F':
            seat_mark = range(65, 65 + 3)
        elif self.grade == 'j':
            seat_mark = range(65, 65 + 6)
        else:
            seat_mark = range(65, 65 + 10)
        return seat_mark

    def _gen_row_seat_index(self, row_number) -> list:
        return [f'{row_number}{chr(i)}' for i in self._gen_seat_mark()]

    def start_index(self) -> list:
        # 座位起始行的编号
        # :return:

        return self._gen_row_seat_index(self.start)

    def end_index(self) -> list:
        # 座位结束行的编号
        # :return:

        return self._gen_row_seat_index(self.end)

    def all_seat_mark(self) -> list:
        # 所有座位图
        # :return:

        result = []
        for i in range(self.start, self.end + 1):
            result.append(self._gen_row_seat_index(i))
        return result

    def number_of_seats(self) -> int:
        rows = self.end - self.start + 1
        if self.grade == 'F':
            return rows * 3
        elif self.grade == 'J':
            return rows * 6
        else:
            return rows * 10


class Aircraft:
    # 机型类
    def __init__(self, iata_code: str, model: str):
        self.cabins = []
        self.iata_code = iata_code
        self.model = model

    def add_cabin(self, grade: str, config: str, start: int, end: int):
        # 添加座位的方法
        self.cabins.append(Seat(grade, config, start, end))

    def get_all_cabin(self) -> list:
        # 获取所有座位等级
        return list(set([row.grade for row in self.cabins]))

    def get_cabin_info(self) -> dict:
        # 获取座位信息
        # :return:

        result = {}
        for row in self.cabins:
            result.update(row.seat_info)
        return result


class Boeing747(Aircraft):
    # Boeing 747 飞机类
    def __init__(self, iata_code: str):
        super(Boeing747, self).__init__(model='Boeing 747', iata_code=iata_code)
