#coding=utf-8
import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk




class xianlan_test:
    #UI
    __Win=None

    __LabelFrame1=None
    __LabelFrame2 = None
    __LabelFrame3 = None

    __Com_Label=None
    __Com_Combobox=None
    __Com_comboBoxVar=None
    __Com_Button=None
    __Com_Button_Var=None

    __Channel_Checkbutton_0=None
    __Channel_Checkbutton_1 = None
    __Channel_Checkbutton_2 = None
    __Channel_Checkbutton_3 = None
    __Channel_Checkbutton_4 = None
    __Channel_Checkbutton_5 = None
    __Channel_Checkbutton_6 = None
    __Channel_Checkbutton_7 = None

    __Channel_Checkbutton_Var0=0
    __Channel_Checkbutton_Var1 = 0
    __Channel_Checkbutton_Var2 = 0
    __Channel_Checkbutton_Var3 = 0
    __Channel_Checkbutton_Var4 = 0
    __Channel_Checkbutton_Var5 = 0
    __Channel_Checkbutton_Var6 = 0
    __Channel_Checkbutton_Var7 = 0
    __Channel_button=None

    __SourceRadiobutton_Inter=None
    __SourceRadiobutton_Ext = None
    __SourceRadiobuttonVar=None

    __SourceButton=None

    # 串口句柄
    __ComHandle = None
    __Baudrate=115200
    __Com_Connet_Timeout=2
    # 串口打开状态
    __OpenState = "closed"
    # 串口端口
    __ComPort = None
    __PortInfoList=[]


    __ComProtocolCmd=None
    __ComProtocolData = None


    def Com_Send_Cmd(self,cmd,data):
        if(self.__OpenState!='opened'):
            return 0
        buf=[]
        parity=0x00
        buf.append(0xa5)
        buf.append(0x01)
        buf.append(cmd)
        buf.append(data)
        for i in range(4):
            parity^=buf[i]
        buf.append(parity)
        buf.append(0x5a)
        self.__ComHandle.write(buf)

    def Com_Button_Callback(self):
        if self.__OpenState=="closed":
            print('self.__ComPort:',self.__ComPort)
            self.__ComHandle = serial.Serial(port=self.__ComPort, baudrate=self.__Baudrate,bytesize=8, parity='N', stopbits=1, timeout=20)
            if self.__ComHandle.is_open:
                self.__OpenState = "opened"
                print("串口打开成功")
                self.__Com_Button_Var.set("关闭串口")
                self.__SourceRadiobutton_Inter.state(['!disabled'])
                self.__SourceRadiobutton_Ext.state(['!disabled'])
                self.__Channel_button.state(['!disabled'])

            else:
                print("串口打开失败")
        elif self.__OpenState=="opened":
            self.__ComHandle.close()
            if not self.__ComHandle.is_open:
                self.__OpenState = "closed"
                self.__Com_Button_Var.set("打开串口")
                self.__SourceRadiobutton_Inter.state(['disabled'])
                self.__SourceRadiobutton_Ext.state(['disabled'])
                self.__Channel_button.state(['disabled'])
                print("串口关闭成功")
            else:
                print("串口关闭失败")

    def Com_Combobox_Callback(self,*args):
        comstr=self.__Com_Combobox.get()
        comstrlist=comstr.split()
        self.__ComPort=comstrlist[0]

    def ChannelButton_Callback(self):
        print("self.__Channel_Checkbutton_Var0:",self.__Channel_Checkbutton_Var0.get())
        print("self.__Channel_Checkbutton_Var1:", self.__Channel_Checkbutton_Var1.get())
        print("self.__Channel_Checkbutton_Var2:", self.__Channel_Checkbutton_Var2.get())
        print("self.__Channel_Checkbutton_Var3:", self.__Channel_Checkbutton_Var3.get())
        print("self.__Channel_Checkbutton_Var4:", self.__Channel_Checkbutton_Var4.get())
        print("self.__Channel_Checkbutton_Var5:", self.__Channel_Checkbutton_Var5.get())
        print("self.__Channel_Checkbutton_Var6:", self.__Channel_Checkbutton_Var6.get())
        print("self.__Channel_Checkbutton_Var7:", self.__Channel_Checkbutton_Var7.get())

        self.__ComProtocolData=0x01
        if(self.__Channel_Checkbutton_Var0.get()==0):
            self.__ComProtocolData=self.__ComProtocolData&(~0x01)
        else:
            self.__ComProtocolData = self.__ComProtocolData | (0x01)

        if (self.__Channel_Checkbutton_Var1.get() == 0):
            self.__ComProtocolData = self.__ComProtocolData & (~0x02)
        else:
            self.__ComProtocolData = self.__ComProtocolData | (0x02)

        if (self.__Channel_Checkbutton_Var2.get() == 0):
            self.__ComProtocolData = self.__ComProtocolData & (~0x04)
        else:
            self.__ComProtocolData = self.__ComProtocolData | (0x04)

        if (self.__Channel_Checkbutton_Var3.get() == 0):
            self.__ComProtocolData = self.__ComProtocolData & (~0x08)
        else:
            self.__ComProtocolData = self.__ComProtocolData | (0x08)

        if (self.__Channel_Checkbutton_Var4.get() == 0):
            self.__ComProtocolData = self.__ComProtocolData & (~0x10)
        else:
            self.__ComProtocolData = self.__ComProtocolData | (0x10)

        if (self.__Channel_Checkbutton_Var5.get() == 0):
            self.__ComProtocolData = self.__ComProtocolData & (~0x20)
        else:
            self.__ComProtocolData = self.__ComProtocolData | (0x20)

        if (self.__Channel_Checkbutton_Var6.get() == 0):
            self.__ComProtocolData = self.__ComProtocolData & (~0x40)
        else:
            self.__ComProtocolData = self.__ComProtocolData | (0x40)

        if (self.__Channel_Checkbutton_Var7.get() == 0):
            self.__ComProtocolData = self.__ComProtocolData & (~0x80)
        else:
            self.__ComProtocolData = self.__ComProtocolData | (0x80)
        print("ChannelVar:",self.__ComProtocolData)
        self.Com_Send_Cmd(0x02,self.__ComProtocolData)


    def SourceButton_Callback(self):
        pass
    def SourceSel_Callback(self):
        print("You selected the option " + str(self.__SourceRadiobuttonVar.get()))
        self.Com_Send_Cmd(0x01, self.__SourceRadiobuttonVar.get())


        #构造函数
    def __init__(self):
        #属性初始化
        # 串口句柄
        __ComHandle = None
        # 串口打开状态
        __OpenState = "closed"
        # 串口端口
        __Port = "COM1"
        #串口可选串口列表
        __PortInfoList=list(serial.tools.list_ports.comports())


        self.__Win = tk.Tk()
        self.__Win.title("线缆检测测试软件")

        self.__LabelFrame1 = ttk.LabelFrame(self.__Win, text=" 串口控制 ")
        self.__LabelFrame1.grid(row=0,column=0,sticky=tk.EW)
        self.__LabelFrame2 = ttk.LabelFrame(self.__Win, text=" 通道切换:(勾选状态：信号源)")
        self.__LabelFrame2.grid(row=1,column=0,sticky=tk.EW)
        self.__LabelFrame3 = ttk.LabelFrame(self.__Win, text=" 信号发生器切换 ")
        self.__LabelFrame3.grid(row=2,column=0,sticky=tk.EW)

        # 串口标签
        self.__Com_Label=ttk.Label(self.__LabelFrame1, text="串口：").grid(row=0, column=0)
        #串口combbox
        self.__Com_comboBoxVar = tk.StringVar()
        self.__Com_Combobox = ttk.Combobox(self.__LabelFrame1, width=12, textvariable=self.__Com_comboBoxVar)
        self.__Com_Combobox["values"] = list(serial.tools.list_ports.comports())
        self.__Com_Combobox["state"] = "readonly"
        if len(self.__Com_Combobox["values"])!=0:
            self.__Com_Combobox.current(0)
            comstr_tmp = self.__Com_Combobox.get()
            comstrlist_tmp = comstr_tmp.split()
            self.__ComPort = comstrlist_tmp[0]
        self.__Com_Combobox.bind("<<ComboboxSelected>>", self.Com_Combobox_Callback)
        self.__Com_Combobox.grid(row=0, column=1)

        #打开串口按钮
        # players.bind("<<ComboboxSelected>>", show_msg)
        self.__Com_Button_Var = tk.StringVar()
        self.__Com_Button_Var.set("打开串口")
        self.__Com_Button = ttk.Button(self.__LabelFrame1, textvariable=self.__Com_Button_Var, command=self.Com_Button_Callback)

        self.__Com_Button.grid(row=0, column=2)
        # 通道控制

        self.__Channel_Checkbutton_Var0 = tk.IntVar()
        self.__Channel_Checkbutton_Var1 = tk.IntVar()
        self.__Channel_Checkbutton_Var2 = tk.IntVar()
        self.__Channel_Checkbutton_Var3 = tk.IntVar()
        self.__Channel_Checkbutton_Var4 = tk.IntVar()
        self.__Channel_Checkbutton_Var5 = tk.IntVar()
        self.__Channel_Checkbutton_Var6 = tk.IntVar()
        self.__Channel_Checkbutton_Var7 = tk.IntVar()

        self.__Channel_Checkbutton_0=ttk.Checkbutton(self.__LabelFrame2,text="通道0",
                                                     variable=self.__Channel_Checkbutton_Var0).grid(row=0,column=0)
        self.__Channel_Checkbutton_0 = ttk.Checkbutton(self.__LabelFrame2, text="通道1",
                                                       variable=self.__Channel_Checkbutton_Var1).grid(row=1,column=0)
        self.__Channel_Checkbutton_0 = ttk.Checkbutton(self.__LabelFrame2, text="通道2",
                                                       variable=self.__Channel_Checkbutton_Var2).grid(row=2,column=0)
        self.__Channel_Checkbutton_0 = ttk.Checkbutton(self.__LabelFrame2, text="通道3",
                                                       variable=self.__Channel_Checkbutton_Var3).grid(row=3,column=0)
        self.__Channel_Checkbutton_0 = ttk.Checkbutton(self.__LabelFrame2, text="通道4",
                                                       variable=self.__Channel_Checkbutton_Var4).grid(row=4,column=0)
        self.__Channel_Checkbutton_0 = ttk.Checkbutton(self.__LabelFrame2, text="通道5",
                                                       variable=self.__Channel_Checkbutton_Var5).grid(row=5,column=0)
        self.__Channel_Checkbutton_0 = ttk.Checkbutton(self.__LabelFrame2, text="通道6",
                                                       variable=self.__Channel_Checkbutton_Var6).grid(row=6,column=0)
        self.__Channel_Checkbutton_0 = ttk.Checkbutton(self.__LabelFrame2, text="通道7",
                                                       variable=self.__Channel_Checkbutton_Var7).grid(row=7,column=0)
        self.__Channel_button=ttk.Button(self.__LabelFrame2,text='切换通道',command=self.ChannelButton_Callback)
        self.__Channel_button.state(['disabled'])
        self.__Channel_button.grid(row=7,column=1,sticky=tk.E)

        #信号源切换

        self.__SourceRadiobuttonVar = tk.IntVar()
        self.__SourceRadiobuttonVar.set(0)
        self.__SourceRadiobutton_Inter=ttk.Radiobutton(self.__LabelFrame3, variable=self.__SourceRadiobuttonVar, text='内置信号发生器', value=0,command=self.SourceSel_Callback)
        self.__SourceRadiobutton_Ext= ttk.Radiobutton(self.__LabelFrame3, variable=self.__SourceRadiobuttonVar, text='外置信号发生器', value=1,command=self.SourceSel_Callback)
        self.__SourceRadiobutton_Inter.state(['disabled'])
        self.__SourceRadiobutton_Ext.state(['disabled'])
        self.__SourceRadiobutton_Inter.grid(row=0,column=0)
        self.__SourceRadiobutton_Ext.grid(row=1,column=0)
        #self.__Channel_button = ttk.Button(self.__LabelFrame3, text='切换信号源',command = self.SourceButton_Callback).grid(row=1, column=1,sticky=tk.E)


        self.__Win.mainloop()
if __name__ == '__main__':
    win=xianlan_test()
