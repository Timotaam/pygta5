"""
A very crude debug view for a 360 controller
Only supports both thumbsticks and triggers at the moment
"""

import tkinter as tk
from tkinter import ttk
import threading

class X360DebugWindow(threading.Thread): 
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.start()

    def run(self):
        self.view = X360DebugView()
        self.view.mainloop()

    def stop(self):
        self.view.destroy()

class X360DebugView(ttk.Frame):
    MAX_TS_VAL = 32768
    MAX_TRG_VAL = 255

    def __init__(self):
        ttk.Frame.__init__(self)
        self.master.title('X360 Controller Debug View')
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        demoPanel = ttk.Frame(self, name='')
        demoPanel.grid()

        # Left trigger
        self.ltrg = ttk.Progressbar(demoPanel, orient=tk.VERTICAL, mode='indeterminate', name='ltrg', maximum=self.MAX_TRG_VAL)
        self.ltrg.grid(row=2, column=1, columnspan=1)

        # left thumbschtick
        self.lts_xp = ttk.Progressbar(demoPanel, orient=tk.HORIZONTAL, mode='indeterminate', name='lts_xp', maximum=self.MAX_TS_VAL)
        self.lts_yp = ttk.Progressbar(demoPanel, orient=tk.VERTICAL, mode='indeterminate', name='lts_yp', maximum=self.MAX_TS_VAL)
        self.lts_xn = ttk.Progressbar(demoPanel, orient=tk.HORIZONTAL, mode='indeterminate', name='lts_xn', maximum=self.MAX_TS_VAL)
        self.lts_yn = ttk.Progressbar(demoPanel, orient=tk.VERTICAL, mode='indeterminate', name='lts_yn', maximum=self.MAX_TS_VAL)

        self.lts_yp.grid(row=1, column=4, columnspan=1)
        self.lts_xp.grid(row=2,  column=6, columnspan=1)
        self.lts_xn.grid(row=2, column=2, columnspan=1)
        self.lts_yn.grid(row=3, column=4, columnspan=1)

        # Right trigger
        self.rtrg = ttk.Progressbar(demoPanel, orient=tk.VERTICAL, mode='indeterminate', name='rtrg', maximum=self.MAX_TRG_VAL)
        self.rtrg.grid(row=2, column=50, columnspan=1)

        # right thumbschtick
        self.rts_xp = ttk.Progressbar(demoPanel, orient=tk.HORIZONTAL, mode='indeterminate', name='rts_xp', maximum=self.MAX_TS_VAL)
        self.rts_yp = ttk.Progressbar(demoPanel, orient=tk.VERTICAL, mode='indeterminate', name='rts_yp', maximum=self.MAX_TS_VAL)
        self.rts_xn = ttk.Progressbar(demoPanel, orient=tk.HORIZONTAL, mode='indeterminate', name='rts_xn', maximum=self.MAX_TS_VAL)
        self.rts_yn = ttk.Progressbar(demoPanel, orient=tk.VERTICAL, mode='indeterminate', name='rts_yn', maximum=self.MAX_TS_VAL)

        self.rts_yp.grid(row=1, column=20, columnspan=1)
        self.rts_xp.grid(row=2,  column=40, columnspan=1)
        self.rts_xn.grid(row=2, column=10, columnspan=1)
        self.rts_yn.grid(row=3, column=20, columnspan=1)

        self.setLts_x(1)
        self.setLts_y(1)
        self.setRts_x(1)
        self.setRts_y(1)

        self.setLtrg(1)
        self.setRtrg(1)

    def updateViewWithPacket(self, packet):
        self.setLts_x(packet['LTS']['X']*self.MAX_TS_VAL)
        self.setLts_y(packet['LTS']['Y']*self.MAX_TS_VAL)
        self.setRts_x(packet['RTS']['X']*self.MAX_TS_VAL)
        self.setRts_y(packet['RTS']['Y']*self.MAX_TS_VAL)

        self.setLtrg(packet['TRG']['L']*self.MAX_TRG_VAL)
        self.setRtrg(packet['TRG']['R']*self.MAX_TRG_VAL)

    def setLts_x(self, var):
        lts_xp_val = self.lts_xp['value']
        lts_xn_val = self.lts_xn['value']
        
        if var > 0:
            self.lts_xn.step(self.MAX_TS_VAL-lts_xn_val)

            if lts_xp_val > var: 
                self.lts_xp.step(-(lts_xp_val-var))
            elif lts_xp_val < var:
                self.lts_xp.step(var-lts_xp_val)
        elif var < 0:
            self.lts_xp.step(-lts_xp_val)

            var = var + self.MAX_TS_VAL
            if lts_xn_val > var: 
                self.lts_xn.step(-(lts_xn_val-var))
            elif lts_xn_val < var:
                self.lts_xn.step(var-lts_xn_val)

    def setLts_y(self, var):
        lts_yp_val = self.lts_yp['value']
        lts_yn_val = self.lts_yn['value']
        
        if var > 0:
            self.lts_yn.step(-lts_yn_val)

            var = var + self.MAX_TS_VAL
            if lts_yp_val > var: 
                self.lts_yp.step(-(lts_yp_val-var))
            elif lts_yp_val < var:
                self.lts_yp.step(var-lts_yp_val)
        elif var < 0:
            self.lts_yp.step(self.MAX_TS_VAL-lts_yp_val)

            if lts_yn_val > var:
                self.lts_yn.step(-(lts_yn_val-var))
            elif lts_yn_val < var:
                self.lts_yn.step(var-lts_yn_val)

    def setRts_x(self, var):
        rts_xp_val = self.rts_xp['value']
        rts_xn_val = self.rts_xn['value']
        
        if var > 0:
            self.rts_xn.step(self.MAX_TS_VAL-rts_xn_val)

            if rts_xp_val > var: 
                self.rts_xp.step(-(rts_xp_val-var))
            elif rts_xp_val < var:
                self.rts_xp.step(var-rts_xp_val)
        elif var < 0:
            self.rts_xp.step(-rts_xp_val)

            var = var + self.MAX_TS_VAL
            if rts_xn_val > var: 
                self.rts_xn.step(-(rts_xn_val-var))
            elif rts_xn_val < var:
                self.rts_xn.step(var-rts_xn_val)

    def setRts_y(self, var):
        rts_yp_val = self.rts_yp['value']
        rts_yn_val = self.rts_yn['value']
        
        if var > 0:
            self.rts_yn.step(-rts_yn_val)

            var = var + self.MAX_TS_VAL
            if rts_yp_val > var: 
                self.rts_yp.step(-(rts_yp_val-var))
            elif rts_yp_val < var:
                self.rts_yp.step(var-rts_yp_val)
        elif var < 0:
            self.rts_yp.step(self.MAX_TS_VAL-rts_yp_val)

            if rts_yn_val > var:
                self.rts_yn.step(-(rts_yn_val-var))
            elif rts_yn_val < var:
                self.rts_yn.step(var-rts_yn_val)

    def setLtrg(self, var):
        trg_val = self.ltrg['value']

        var = var + self.MAX_TRG_VAL

        if trg_val > var: 
            self.ltrg.step(-(trg_val-var))
        elif trg_val < var:
            self.ltrg.step(var-trg_val)

    def setRtrg(self, var):
        trg_val = self.rtrg['value']

        var = var + self.MAX_TRG_VAL

        if trg_val > var: 
            self.rtrg.step(-(trg_val-var))
        elif trg_val < var:
            self.rtrg.step(var-trg_val) 
