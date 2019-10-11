




import Pyro4


from multiprocessing import Process
import time
from typing import List




class Main_manager:

    def __init__(self, IP):
        self.isRunning = True
        self.local_job_server = Pyro4.core.Proxy('PYRO:Greeting@' + IP + ':9090')
        self.job_results:List[int] = []
        self.main_process = Process(target=self.run)


    def start(self):
        print("Starting master client")
        self.main_process.start()

    def stop(self):
        print("Stopping master client")
        self.main_process.close()

    def run(self):
        print("Started main() as process")


        self.waiting_for_isDone()


        print("Returning from main()")


    def waiting_for_isDone(self):
        isRunning = True

        while isRunning:
            print("Testing if clients are done")
            if self.local_job_server.get_isDone():

                self.isRunning=False
                print("Jobs are done. Printing results, then returning")
                self.job_results = self.local_job_server.get_jobs_results()
                print(self.job_results)
                print(sum(self.job_results))
                return
            else:
                print("Not all jobs are done...")
                print(self.local_job_server.get_jobs_amount())
                time.sleep(5)