#! /usr/bin/python
# coding:utf-8
import ptxconftools
from ptxconftools import ConfController
from ptxconftools.gtk import MonitorSelector
import pygtk
import appindicator
pygtk.require('2.0')
import gtk
import os

iconpath = os.path.dirname( ptxconftools.__file__ )+"/iconStyle03_256.png"

class PTXConfUI():
    def __init__(self):
        # create systray interface
        self.systray = appindicator.Indicator( "testname", iconpath, appindicator.CATEGORY_APPLICATION_STATUS)
        self.systray.set_status(appindicator.STATUS_ACTIVE)

        # construct menu
        menu = gtk.Menu()
        mitem = gtk.MenuItem("設定")
        menu.append(mitem)
        mitem.connect("activate", self.createConfigWindow)
        mitem.show()
        mitem = gtk.MenuItem("終了する")
        menu.append(mitem)
        mitem.connect("activate", self.exit_program)
        mitem.show()

        # attach menu to out system tray
        self.systray.set_menu(menu)

        # instantiate confcontroller
        self.myConf = ConfController()

    # def resetAllConfig(self, callback_data=None):
    #    self.myConf.resetAllDeviceConfig()

    def getActiveInput(self):
        a = self.window.ptDropdown.get_active_text()
        b = self.window.ptDropdown.get_active()
        if b > 0:
            return a

    def getSelectedMonitor(self, callback_data=None):
        a = self.window.monitorDropdown.get_active_text()
        b = self.window.monitorDropdown.get_active()
        if b > 0:
            return a

    def mapTabletToMonitor(self, callback_data=None):
        # find ids for the right input device
        pen = self.getActiveInput()
        # get the display width, screen_width and screen_offset for CTMGenerator function to calculate matrix
        monitor = self.getSelectedMonitor()
        # call API with these settings
        self.myConf.setPT2Monitor(pen, monitor)

    def exit_program(self, callback_data=None):
        # This function kills the program PTXConf.
        # Can be called from 2 places, 1 from the appindicator dropdown menu "Exit",
        # another from the config popup window "Exit" button.
        gtk.main_quit()

    def createConfigWindow(self, callback_data=None):
        # first refress all monitor and touch/pen information
        self.myConf.refresh()

        # This creats a popup window for more detailed configuration if user find necessary.
        # Still incomplete at the moment.
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_border_width(20)
        self.window.set_title("PTXConf")
        self.window.connect("destroy", self.destroyConfigWindow)

        button_apply = gtk.Button("適用")
        button_close = gtk.Button("閉じる")

        button_close.connect("clicked", self.destroyConfigWindow)
        vbox = gtk.VBox(spacing=20)
        hbox = gtk.HBox(spacing=20)
        vboxLeft = gtk.VBox(spacing=6)
        vboxRight = gtk.VBox(spacing=6)
        hboxForButtons = gtk.HBox()
        hboxForButtonsLeft = gtk.HBox(spacing=30)
        hboxForButtonsRight = gtk.HBox(spacing=10)
        labelEmptySpace01 = gtk.Label()
        labelEmptySpace02 = gtk.Label()

        label01 = gtk.Label("入力デバイス")
        label02 = gtk.Label("モニタ")
        # create monitor selector widget
        monSelector = MonitorSelector(self.myConf.monitorIds)
        # dropdown menus 1 and 2, users choose what input device map to what monitor.
        # creat and set up dopdownmenu 1: user select from a list of connected pen input deivces.
        ptDropdown = gtk.combo_box_new_text()
        ptDropdown.set_tooltip_text("choose an input device to configure")
        # getting the list of names of the input device
        # set up the dropdown selection for input devices
        ptDropdown.append_text('入力デバイスを選択してください。:')
        for i in self.myConf.penTouchIds:
            ptDropdown.append_text(i)
        ptDropdown.set_active(0)
        # ptDropdown.connect("changed", self.getActiveInput)
        # creat and set up dopdownmenu 2: user select from a list of connected display/output deivces.
        monitorDropdown = gtk.combo_box_new_text()
        monitorDropdown.set_tooltip_text("マッピングするデバイスを選択してください。")
        # getting the list of display names
        # set up the dropdown selection for monitors
        monitorDropdown.append_text('モニタを選択してください。:')
        monitorDropdown.mons = self.myConf.monitorIds.keys()
        for key in monitorDropdown.mons:
            monitorDropdown.append_text(key)
        monitorDropdown.set_active(0)
        monitorDropdown.handler_id_changed = monitorDropdown.connect("changed", self.monDropdownCallback)

        # connect apply button to function
        button_apply.connect("clicked", self.mapTabletToMonitor)

        # inserting all widgets in place
        vboxLeft.pack_start(label01)
        vboxLeft.pack_start(label02)

        vboxRight.pack_start(ptDropdown)
        vboxRight.pack_start(monitorDropdown)

        hboxForButtonsLeft.pack_start(button_apply)
        hboxForButtonsLeft.pack_start(labelEmptySpace01)
        hboxForButtonsRight.pack_start(labelEmptySpace02)
        hboxForButtonsRight.pack_start(button_close)
        hboxForButtons.pack_start(hboxForButtonsLeft)
        hboxForButtons.pack_start(hboxForButtonsRight)

        vbox.pack_start(monSelector, expand=False)
        hbox.pack_start(vboxLeft)
        hbox.pack_start(vboxRight)
        vbox.pack_start(hbox)
        vbox.pack_start(hboxForButtons)
        self.window.add(vbox)
        self.window.show_all()

        # store convenient handle to drop down boxes
        self.window.monitorSelector = monSelector
        self.window.monitorSelector.connect('button-press-event', self.monSelectorCallback)
        self.window.ptDropdown = ptDropdown
        self.window.monitorDropdown = monitorDropdown

    def monDropdownCallback(self, calback_data=None):
        # update MonitorSelector
        mon = self.window.monitorDropdown.get_active_text()
        if mon in self.window.monitorSelector.moninfo:
            self.window.monitorSelector.set_active_mon(mon)

    def monSelectorCallback(self, widget, event):
        # get mon selector selection
        monSelection = self.window.monitorSelector.get_active_mon()
        # if different than drop down, update drop down
        if monSelection != self.window.monitorDropdown.get_active_text():
            # lookup this monitor index in drop down and set it...
            idx = self.window.monitorDropdown.mons.index(monSelection)
            # careful to disable dropdown changed callback while doing this
            hid = self.window.monitorDropdown.handler_id_changed
            self.window.monitorDropdown.handler_block(hid)
            self.window.monitorDropdown.set_active(idx+1)
            self.window.monitorDropdown.handler_unblock(hid)

    def destroyConfigWindow(self, callback_data=None):
        # close the popup window, app will still be docked on top menu bar.
        self.window.destroy()

    def main(self):
        gtk.main()


p = PTXConfUI()
p.main()
