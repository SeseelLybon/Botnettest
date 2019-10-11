

import Pyro4

import sys

from multiprocessing import Process
from typing import List
import time

import masterclient


def job_creator(lhs:int, rhs:int):
    lhs_deconst = int_deconstructor(lhs)
    rhs_deconst = int_deconstructor(rhs)


    jobs = []
    for lhs_p in lhs_deconst:
        for rhs_p in rhs_deconst:
            jobs.append((lhs_p, rhs_p))

    return jobs



def int_deconstructor(a):
    dec_places = []
    isRunning = True
    decs = 1
    while isRunning:
        if (a%(decs*10)//decs)*decs == 0 and decs > a:
            isRunning = False
            continue

        dec_places.append((a%(decs*10)//decs)*decs)
        decs*=10
    return dec_places

@Pyro4.expose
class Job_server(object):



    def __init__(self, jobs):
        self.workers = []
        self.isDone = False
        self.job_results = []
        self.jobs = jobs

    def get_job(self):

        if len(self.jobs) > 0:
            return self.jobs.pop()
        else:
            self.isDone = True
            return None

    def get_isDone(self):
        return self.isDone

    def get_jobs_results(self):
        return self.job_results

    def get_jobs_amount(self):
        return len(self.jobs)

    def set_jobs(self, jobs):
        self.jobs = jobs

    def return_job_results(self, job_out):
        self.job_results.append(job_out)

    def register_worker(self, newworker, callback):
        self.workers.append((newworker, callback))
        print("Worker registered to labour force", newworker, callback)

    def unregister_worker(self, oldworker):
        for w, c in self.workers:
            if w == oldworker:
                self.workers.remove((w, c))
                print("Worker", oldworker, "left the labour force")
                break


if __name__ == "__main__":
    #server_IP = "10.19.38.66"
    server_IP = "localhost"
    print("Starting server.py as __main__")

    #lhs = int(sys.argv[1])
    #rhs = int(sys.argv[2])
    lhs = 2**100
    rhs = 3**100

    print(lhs,"*",rhs,"=",str(lhs*rhs))

    jobbers = job_creator(lhs, rhs)

    print(jobbers)

    job_server_o = Job_server(jobbers)

    main_manager = masterclient.Main_manager(server_IP)

    main_manager.start()

    JobserverDaemon = Pyro4.Daemon.serveSimple({
        job_server_o: 'Greeting',
    }, host=server_IP, port=9090, ns=False, verbose=True)


    main_manager.stop()

    print("Done with server.py as __main__")