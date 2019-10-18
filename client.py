





import Pyro4
import pyglet

import uuid



def doJob(job):
    return job[0]*job[1]



def lookforjob(dt):

    job = job_server.get_job()

    if job is None:
        print("Didn't get a job")

        pyglet.clock.unschedule(lookforjob)
        pyglet.clock.schedule_interval_soft(lookforjob, 2)

    else:
        print("Got a job", job)
        pyglet.clock.unschedule(lookforjob)

        joboutput = doJob(job)
        print(joboutput)
        job_server.return_job_results(joboutput)

        pyglet.clock.schedule_interval_soft(lookforjob, 1)


if __name__ == '__main__':
    # ipAddressServer = "10.19.38.66" # TODO add your server remote IP here
    ipAddressServer = "localhost"

    job_server = Pyro4.core.Proxy('PYRO:Greeting@' + ipAddressServer + ':9090')

    workerid = uuid.uuid1()
    slots = 50

    job_server.register_worker(workerid, slots)
    print(job_server.get_workers_amount())

    # jobless = True
    print("Starting client; waiting for jobs")

    pyglet.clock.schedule_interval_soft(lookforjob, 4)


    pyglet.app.run()


    print("Stopping client")