#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = " Marcelo Tuller <marscrophimself@yahoo.com> "

import sys, os
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import MySQLdb
import gettext
from threading import Thread
from functools import partial
from collections import defaultdict, Counter
import twitter_api
import facebook_api
import time

lista_queries = defaultdict(list)
[lista_queries[i] for i in ['sismo', 'terremoto', 'inundacion', 'incendio', 'alud', 'maremoto', 'incendioforestal', 'sequia', 'tsunami', 'desprendimientodetierra', 'delizamientodetierra']]

class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.FULL_REPAINT_ON_RESIZE)
        ListCtrlAutoWidthMixin.__init__(self)

class semaforo(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, size=(80, 110))

        self.count = 0
        self.parent = parent
        self.SetBackgroundColour('#000000')
        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, event):

        dc = wx.PaintDC(self)

        if self.count < 100:
            dc.SetBrush(wx.Brush("#8B2323"))
            dc.DrawCircle(41, 70, 10)
            dc.SetBrush(wx.Brush("#CD8500"))
            dc.DrawCircle(41, 50, 10)
            dc.SetBrush(wx.Brush(wx.GREEN))
            dc.DrawCircle(41, 30, 10)
        elif (self.count < 200) and (self.count > 100):
            dc.SetBrush(wx.Brush("#8B2323"))
            dc.DrawCircle(41,70,10)
            dc.SetBrush(wx.Brush(wx.YELLOW))
            dc.DrawCircle(41,50,10)
            dc.SetBrush(wx.Brush("#426F42"))
            dc.DrawCircle(41,30,10)
        else:
            if (self.count < 1e+12) and (self.count > 200):
                dc.SetBrush(wx.Brush(wx.RED))
                dc.DrawCircle(41,70,10)
                dc.SetBrush(wx.Brush("#CD8500"))
                dc.DrawCircle(41,50,10)
                dc.SetBrush(wx.Brush("#426F42"))
                dc.DrawCircle(41,30,10)

class conexion():
    def __init__(self):
        self.conectar_base_de_datos = MySQLdb.connect(host= "localhost",
                  user=#nombre del usuario,
                  passwd=#password,
                  charset="utf8", #lectura de caracteres
                  db=#nombre de la base de datos)
        self.cursor = self.conectar_base_de_datos.cursor()

def usuario():                            
    comando_usuario = "SELECT usuario FROM tweets" 
    cursor = conexion().cursor
    cursor.execute(comando_usuario)
    resultados = []
    u = cursor.fetchall()
    for usuario in u:
         for valor in usuario:
              resultados.append(valor)
    return resultados

class usuario_fb():
    def __init__(self):                                 
        cursor = conexion().cursor                          
        comando_query = "SELECT usuario FROM facebook" 
        cursor.execute(comando_query)
        self.resultados = []    
        ufb = cursor.fetchall()
        self.fb_u_n = defaultdict(list)
        for query in ufb:
            self.fb_u_f = 0             
            self.fb_u_n[query].append(self.fb_u_f) 
            for valor in query:            
                self.resultados.append(valor)
                self.fb_u_n[query][0] += 1

class desastres_fb():
    def __init__(self):                                 
        cursor = conexion().cursor                          
        comando_query = "SELECT desastre FROM facebook" 
        cursor.execute(comando_query)
        self.resultados = []    
        dfb = cursor.fetchall()
        self.fb_q_n = defaultdict(list)
        for query in dfb:
            self.fb_q_f = 0             
            self.fb_q_n[query].append(self.fb_q_f) 
            for valor in query:            
                self.resultados.append(valor)
                self.fb_q_n[query][0] += 1

class desastres():                 
    def __init__(self):                                 
        cursor = conexion().cursor                          
        comando_query = "SELECT query FROM tweets"      
        cursor.execute(comando_query)
        self.resultados = []    
        d = cursor.fetchall()
        self.q_n = defaultdict(list)   
        for query in d:
            self.q_t = 0                
            self.q_n[query].append(self.q_t)       
            for valor in query:            
                self.resultados.append(valor)
                self.q_n[query][0] += 1

def link():    
    cursor = conexion().cursor                                                         
    comando_link = "SELECT link FROM tweets"                          
    cursor.execute(comando_link)                                      
    resultados = []                                                   
    l = cursor.fetchall()                                                             
    for link in l:                                               
        for valor in link:                                              
            resultados.append(valor)                                                    
    return resultados 

class tweet():
    def __init__(self): 
        cursor = conexion().cursor                             
        comando_tweet = "SELECT tweet FROM tweets"  
        cursor.execute(comando_tweet)
        self.resultados = []      
        t = cursor.fetchall()          
        for tweet in t:    
             for valor in tweet:                
                self.resultados.append(valor)

def fecha():
    cursor = conexion().cursor                              
    comando_fecha = "SELECT fecha FROM tweets" 
    cursor.execute(comando_fecha)
    resultados = []      
    f = cursor.fetchall()
    for fecha in f:
         for valor in fecha:  
            resultados.append(valor)
    return resultados

def fecha_fb():  
    cursor = conexion().cursor                            
    comando_fecha = "SELECT fecha FROM facebook" 
    cursor.execute(comando_fecha)
    resultados = []      
    ff = cursor.fetchall()
    for fecha in ff:
         for valor in fecha:  
            resultados.append(valor)
    return resultados

class posts_fb():  
    def __init__(self):
        cursor = conexion().cursor                          
        comando_fecha = "SELECT post FROM facebook" 
        cursor.execute(comando_fecha)
        self.resultados_fb = []      
        pf = cursor.fetchall()
        for post in pf:
             for valor in post:  
                self.resultados_fb.append(valor)

class MyFrame5(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Desastres Naturales", size = (wx.DisplaySize()[0]/2, wx.DisplaySize()[1]/2), style = wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR)

        self.__close_callback = None
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.notebook_2 = wx.Notebook(self, wx.ID_ANY)
        self.notebook_2_pane_1 = wx.Panel(self.notebook_2, wx.ID_ANY, style = wx.TAB_TRAVERSAL & wx.CLIP_CHILDREN | wx.NO_FULL_REPAINT_ON_RESIZE)

        self.foto = wx.BitmapFromImage(wx.Image("serveimage.png").Rescale(1050,300))

        self.banner0 = wx.StaticBitmap(self.notebook_2_pane_1, -1, self.foto, wx.DefaultPosition, style = wx.BITMAP_TYPE_PNG)

        self.label_0 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Sismo"), pos = (25,20))
        self.label_2 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Terremoto"), pos = (95,20))
        self.label_8 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Inundacion"), pos=(175,20))
        self.label_9 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Incendio"), pos=(265,20))
        self.label_6 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Alud"), pos=(365,20))
        self.label_4 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Maremoto"), pos=(430,20))
        self.label_1 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Incendio forestal"),pos=(500,20))
        self.label_7 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Sequia"),pos=(610,20))
        self.label_5 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Tsunami"),pos=(695,20))
        self.label_10 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Desprendimiento"),pos=(760,20))
        self.label_3 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, ("Delizamiento"),pos=(860,20))

        self.label_0.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_1.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_2.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_3.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_4.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_5.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_6.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_7.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_8.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_9.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))
        self.label_10.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL))

        self.label_0.SetForegroundColour((255, 165, 0,255)) #naranja
        self.label_2.SetForegroundColour((255, 140, 0, 255)) #naranja oscuro
        self.label_8.SetForegroundColour(wx.BLUE)
        self.label_9.SetForegroundColour(wx.YELLOW)
        self.label_6.SetForegroundColour(wx.WHITE)
        self.label_4.SetForegroundColour(wx.CYAN)
        self.label_1.SetForegroundColour((255, 0, 255, 255)) #color magenta
        self.label_7.SetForegroundColour((128, 128, 128, 255)) #gris
        self.label_5.SetForegroundColour((128, 0, 128, 255)) #purpura
        self.label_10.SetForegroundColour((178, 34, 34, 255)) #color ladrillo
        self.label_3.SetForegroundColour((139, 0, 0, 255)) #rojo oscuro

        self.semaforo0 = semaforo(self.notebook_2_pane_1, 1)
        self.semaforo2 = semaforo(self.notebook_2_pane_1, -1)
        self.semaforo8 = semaforo(self.notebook_2_pane_1, -1)
        self.semaforo9 = semaforo(self.notebook_2_pane_1, -1)
        self.semaforo6 = semaforo(self.notebook_2_pane_1, -1)
        self.semaforo4 = semaforo(self.notebook_2_pane_1, -1)
        self.semaforo1 = semaforo(self.notebook_2_pane_1, -1)
        self.semaforo7 = semaforo(self.notebook_2_pane_1, -1)
        self.semaforo5 = semaforo(self.notebook_2_pane_1, -1)
        self.semaforo10 = semaforo(self.notebook_2_pane_1, -1)
        self.semaforo3 = semaforo(self.notebook_2_pane_1, -1)

        self.tweet = tweet()
        self.posts_fb = posts_fb()
        self.notebook_2_pane_2 = wx.Panel(self.notebook_2, wx.ID_ANY, style = wx.TAB_TRAVERSAL)
        self.list_ctrl_2 = AutoWidthListCtrl(self.notebook_2_pane_2)          
        self.list_ctrl_2.InsertColumn(0, '       desastre        ')
        self.list_ctrl_2.InsertColumn(1, '       usuario         ')
        self.list_ctrl_2.InsertColumn(2, '                           link                        ')                
        self.list_ctrl_2.InsertColumn(3, '                           tweet                       ')
        self.list_ctrl_2.InsertColumn(4, '                           fecha                   ', wx.LIST_FORMAT_RIGHT)

        self.list_ctrl_2.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)  
        self.list_ctrl_2.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)     
        self.list_ctrl_2.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)    
        self.list_ctrl_2.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
        self.list_ctrl_2.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)

        self.notebook_2_pane_3 = wx.Panel(self.notebook_2, wx.ID_ANY, style = wx.TAB_TRAVERSAL)
        self.list_ctrl_1 = AutoWidthListCtrl(self.notebook_2_pane_3)

        self.banner1 = wx.StaticBitmap(self.notebook_2_pane_2, -1, self.foto, wx.DefaultPosition, style = wx.BITMAP_TYPE_PNG)

        self.banner2 = wx.StaticBitmap(self.notebook_2_pane_3, -1, self.foto, wx.DefaultPosition, style = wx.BITMAP_TYPE_PNG)

        self.list_ctrl_1.InsertColumn(0, '       desastre        ')  
        self.list_ctrl_1.InsertColumn(1, '       usuario         ')     
        self.list_ctrl_1.InsertColumn(2, '                           fecha                   ')    
        self.list_ctrl_1.InsertColumn(3, '                           post                    ', wx.LIST_FORMAT_RIGHT)

        self.list_ctrl_1.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)  
        self.list_ctrl_1.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)     
        self.list_ctrl_1.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)    
        self.list_ctrl_1.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)

        self.list_ctrl_1.SetScrollbar(wx.VERTICAL, 0, 0, 2, 0)
        self.list_ctrl_2.SetScrollbar(wx.VERTICAL, 0, 0, 2, 0)

        self.list_ctrl_1.Bind(wx.EVT_RIGHT_UP, partial(self.ShowPopup, cls = self.list_ctrl_1))
        self.list_ctrl_2.Bind(wx.EVT_RIGHT_UP, partial(self.ShowPopup, cls = self.list_ctrl_2))

        self.Centre(True)
        self.Maximize(True)

        self.onRun()

        self.__set_properties()
        self.__do_layout()


    def ShowPopup(self, event, cls):
        menu = wx.Menu()
        menu.Append(1, "Copiar")
        menu.Bind(wx.EVT_MENU, partial(self.CopyItems, cls = cls), id=1)
        self.PopupMenu(menu)


    def CopyItems(self, event, cls):
        selectedItems = []
        for i in xrange(cls.GetItemCount()):
            if cls.IsSelected(i):
                selectedItems.append(str([cls.GetItemText(i,j) for j in xrange(5 if cls == self.list_ctrl_2 else 4)]))

        clipdata = wx.TextDataObject()
        clipdata.SetText("\n".join(selectedItems))
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipdata)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")

    def OnScroll(self, evt):
            evt.Skip()
    def OnRefresh(self):
            try:
		    twitter_api.twitter_database()
		    facebook_api.facebook_database()
		    self.desastres = desastres().resultados          
		    self.usuario = usuario()
		    self.fecha = fecha()          
		    self.link = link()
		    self.tweet = tweet().resultados
		    self.desastres_fb = desastres_fb().resultados          
		    self.fecha_fb = fecha_fb()
		    self.usuario_fb = usuario_fb().resultados          
		    self.post = posts_fb().resultados_fb

		    tw = tuple(set([(self.desastres[i], self.usuario[i], self.link[i], self.tweet[i], self.fecha[i]) for i in xrange(len(self.usuario))])) 
		    fb = tuple(set([(self.desastres_fb[i], self.usuario_fb[i], self.fecha_fb[i], self.post[i]) for i in xrange(len(self.post))])) 

		    c_t = [tw[i][0] for i in xrange(len(tw))]
		    c_f = [fb[i][0] for i in xrange(len(fb))]
		    total_queries = (c_t, c_f)

		    conteo = [Counter(total_queries[i]).most_common() for i in range(len(total_queries))]

		    for i in tw:
		        self.index = self.list_ctrl_2.InsertStringItem(sys.maxint, i[0])
		        self.list_ctrl_2.SetStringItem(self.index,1,i[1])
		        self.list_ctrl_2.SetStringItem(self.index,2,i[2])
		        self.list_ctrl_2.SetStringItem(self.index,3,i[3])
		        self.list_ctrl_2.SetStringItem(self.index,4,i[4])
		                                 
		    for i in fb:
		        self.index = self.list_ctrl_1.InsertStringItem(sys.maxint, i[0])
		        self.list_ctrl_1.SetStringItem(self.index,1,str(i[1]))
		        self.list_ctrl_1.SetStringItem(self.index,2,i[2])
		        self.list_ctrl_1.SetStringItem(self.index,3,i[3])

		    for i in conteo:     
		        for j in range(len(i)):                                
		            if '#' in i[j][0]:                                 
		                m = i[j][0].split('#')[1]
		                if (#type the extra keywords in your generalized twitter query here) in m:
		                    m = m.split(#type the extra keywords in your query here)[0]
		                else:
		                    m = m
		            else:
		                m = i[j][0]
		            if m in lista_queries.keys():
		                lista_queries[m].append(i[j][1])
		            else:
		                pass

		    conteo_global = [sum(lista_queries[i]) for i in lista_queries] 

		    for i in xrange(len(conteo_global)):
		        if i == 0:      
		            self.semaforo0.count = conteo_global[i]
		            self.semaforo0.OnPaint(self)
		        if i == 1:
		            self.semaforo1.count = conteo_global[i]
		            self.semaforo1.OnPaint(self)
		        if i == 2:
		            self.semaforo2.count = conteo_global[i]
		            self.semaforo2.OnPaint(self)
		        if i == 3:
		            self.semaforo3.count = conteo_global[i]
		            self.semaforo3.OnPaint(self)
		        if i == 4:
		            self.semaforo4.count = conteo_global[i]
		            self.semaforo4.OnPaint(self)
		        if i == 5:
		            self.semaforo5.count = conteo_global[i]
		            self.semaforo5.OnPaint(self)
		        if i == 6:
		            self.semaforo6.count = conteo_global[i]
		            self.semaforo6.OnPaint(self)
		        if i == 7:
		            self.semaforo7.count = conteo_global[i]
		            self.semaforo7.OnPaint(self)
		        if i == 8:
		            self.semaforo8.count = conteo_global[i]
		            self.semaforo8.OnPaint(self)
		        if i == 9:
		            self.semaforo9.count = conteo_global[i]
		            self.semaforo9.OnPaint(self)
		        if i == 10:    
		            self.semaforo10.count = conteo_global[i]
		            self.semaforo10.OnPaint(self)
		    print "Actualizado"
            except Exception, e:
		    print e
		    pass

    def onRun(self):   
        td = Thread(target = self.__run)
        td.setDaemon(True)
        td.start() 
                         
    def __run(self):
        while True:
            wx.CallAfter(self.OnRefresh)
            print "Actualizando" 
            time.sleep(60 * 2)

    def register_close_callback(self, callback):
        self.__close_callback = callback

    def OnClose(self, event):
        doClose = True if not self.__close_callback else self.__close_callback()
        if doClose:
            event.Skip()

    def __set_properties(self):
        self.SetTitle(("Desastres Naturales"))
        self.SetMaxSize((1366, 300))
        self.SetBackgroundColour(wx.Colour(234, 231, 228))
        self.SetForegroundColour(wx.Colour(0, 0, 0))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.semaforo0, flag = wx.RIGHT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo1, flag = wx.RIGHT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo2, flag = wx.RIGHT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo3, flag = wx.RIGHT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo4, flag = wx.RIGHT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo5, flag = wx.RIGHT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo6, flag = wx.RIGHT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo7, flag = wx.RIGHT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo8, flag = wx.LEFT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo9, flag = wx.LEFT | wx.CENTER, border=5)
        sizer_5.Add(self.semaforo10, flag = wx.LEFT | wx.CENTER, border=5)

        self.notebook_2.AddPage(self.notebook_2_pane_1, ("Estado"))
        self.notebook_2.AddPage(self.notebook_2_pane_2, ("Tweets"))
        self.notebook_2.AddPage(self.notebook_2_pane_3, ("Facebook"))
        self.notebook_2_pane_1.SetSizer(sizer_5)
        sizer_6.Add(self.list_ctrl_2, 1, wx.EXPAND, 5)
        self.notebook_2_pane_2.SetSizer(sizer_6)
        sizer_7.Add(self.list_ctrl_1, 1, wx.EXPAND, 5)
        self.notebook_2_pane_3.SetSizer(sizer_7)
        sizer_4.Add(self.notebook_2, 1, wx.EXPAND, 5)
        sizer_1.Add(sizer_4, 1, wx.SHAPED, 0)
        self.SetSizerAndFit(sizer_1)
        self.Layout()

if __name__ == '__main__':
    try:
        app = wx.App(redirect = False)
        frame = MyFrame5()

        frame.Show(1)
        frame.Layout()

        frame.register_close_callback(lambda: True)

        app.MainLoop()
    except Exception, e:
        print e
        sys.exit(1)
