import queue
import threading
from fund_scrawl import scrawl_data, get_fund_id

if __name__ == '__main__':
    fund_list = get_fund_id()[:1000]
    fund_code_queue = queue.Queue(len(fund_list))
    start_date = '2017-06-30'
    end_date = '2020-06-30'
    save_path = './data/'
    #将需要抓去的基金放入队列
    for i in range(len(fund_list)):
        fund_code_queue.put(fund_list[i])
    # mutex_lock = threading.Lock()
    # for i in range(3):
    #     t = threading.Thread(target=scrawl_data(fund_code_queue, start_date, end_date, save_path=save_path), name='LoopThread'+str(i))
    #     t.start()
    if not os.path.exists(save_path):
      os.makedirs(save_path)
    scrawl_data(fund_code_queue, start_date, end_date, save_path)
