import json
import os
import uuid
from lunarcalendar import Converter, Lunar

class Icswriter(object):
    def __init__(self, year=50, file_loc='calender.json', save_dir='输出目录'):
        '''
        :param year: 想生成多少年的，比如10年的生日
        :param file_loc: 日历json的位置，一般不用管
        :param save_dir: 输出文件夹
        '''
        self.year = year
        self.dir = save_dir
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

    def run(self, name: str, month: int, day: int):
        '''
        :param name: 姓名
        :param month:  农历月份，输入数字
        :param day: 农历日份，输入数字
        :return:
        '''
        if month not in range(1, 13) or day not in range(1, 31):
            return 'error'
        f = open(os.path.join(self.dir, name + '.ics'), 'w', encoding='utf-8')
        f.write('BEGIN:VCALENDAR' + '\n')
        f.write('PRODID:-//SabreDAV//SabreDAV//EN' + '\n')
        f.write('VERSION:2.0' + '\n')
        for i in range(2025, 2025 + self.year):
            # 定义农历日期，例如 2025 年农历二月初二
            lunar_date = Lunar(i, month, day, isleap=False)

            # 进行转换
            solar_date = Converter.Lunar2Solar(lunar_date)
            data = solar_date.to_date().strftime("%Y%m%d")
            self.writefile(f, name, data)
        f.write('END:VCALENDAR' + '\n')
        f.close()

    def writefile(self, f, name, data):
        f.write('BEGIN:VEVENT' + '\n')
        f.write('DTSTART;TZID=Asia/Shanghai:' + data + '\n')
        f.write('DTEND;TZID=Asia/Shanghai:' + str(int(data) + 1) + '\n')
        f.write('CLASS:PRIVATE' + '\n')
        f.write('DESCRIPTION:' + '\n')
        f.write('LOCATION:' + '\n')
        f.write('SEQUENCE:2' + '\n')
        f.write('UID:' + str(uuid.uuid4()) + '\n')
        f.write('STATUS:CONFIRMED' + '\n')
        f.write('SUMMARY:' + name + '生日' + '\n')
        f.write('TRANSP:TRANSPARENT' + '\n')

        f.write('BEGIN:VALARM' + '\n')
        f.write('ACTION:DISPLAY' + '\n')
        f.write('TRIGGER;RELATED=START:PT0S' + '\n')
        f.write('SUMMARY:' + name + '生日' + '\n')
        f.write('DESCRIPTION:This is an event reminder' + '\n')
        f.write('END:VALARM' + '\n')
        f.write('END:VEVENT' + '\n')


if __name__ == '__main__':
    ics = Icswriter(10)
    ics.run('老哥', 6, 27)
