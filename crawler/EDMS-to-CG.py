import win32serviceutil, win32service, win32event
import servicemanager

class Service(win32serviceutil.ServiceFramework):
    _svc_name_         = "EDMS-to-CG"
    _svc_display_name_ = "EDMS-to-CG Syncer"
    _svc_description_  = "Uploaded the EDMS database to Cartograph"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        servicemanager.LogInfoMsg('init')

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        servicemanager.LogInfoMsg('stop')

    def SvcDoRun(self):
        pausetime = 60 * 1000
        servicemanager.LogInfoMsg('run')
        while True:
            stopsignal = win32event.WaitForSingleObject(self.hWaitStop, pausetime)
            if stopsignal == win32event.WAIT_OBJECT_0: break
            self.runOneLoop()

    def runOneLoop(self):
        
        servicemanager.LogInfoMsg('Running')

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(Service)