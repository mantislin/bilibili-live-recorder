from Live import BiliBiliLive
import os, sys
import requests
import time
import config
import utils
import multiprocessing
import urllib3
urllib3.disable_warnings()


class BiliBiliLiveRecorder(BiliBiliLive):
    def __init__(self, room_id):
        super().__init__(room_id)
        self.inform = utils.inform
        self.print = utils.print_log
        self.room_title = None
        self.host_name = None

    def check(self, interval):
        while True:
            try:
                room_info = self.get_room_info()
                if room_info['status']:
                    self.inform(room_id=self.room_id,desp=room_info['roomname'])
                    self.print(self.room_id, room_info['roomname'])
                    self.room_title = room_info['roomname']
                    self.host_name = room_info['hostname']
                    break
                else:
                    self.print(self.room_id, '等待开播')
            except Exception as e:
                print(e)
                pass
            time.sleep(interval)
        return self.get_live_urls()

    def record(self, record_url, output_filename):
        self.print(self.room_id, '√ 正在录制...' + self.room_id)
        try:
            resp = requests.get(record_url, stream=True)
        except Exception as e:
            print(e)
            pass
        else:
            try:
                with open(output_filename, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024*3):
                        f.write(chunk) if chunk else None
            except Exception as e:
                print(e)
                pass

    def run(self):
        while True:
            try:
                urls = self.check(interval=10)
                filename = utils.generate_filename(self.host_name + '__' + self.room_title, self.room_id)
                c_filename = os.path.join(os.getcwd(), 'files', filename)
                self.record(urls[0], c_filename)
                self.print(self.room_id, '录制完成')
            except Exception as e:
                print(e)
                pass


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 2:
        input_id = [str(sys.argv[1])]
    elif len(sys.argv) == 1:
        input_id = config.rooms  # input_id = '917766' '1075'
    else:
        raise ZeroDivisionError('请检查输入的命令是否正确 例如：python3 run.py 10086')

    mp = multiprocessing.Process
    tasks = [mp(target=BiliBiliLiveRecorder(room_id).run) for room_id in input_id]
    for i in tasks:
        i.start()
    for i in tasks:
        i.join()
