#!/usr/bin/python
# coding:utf-8

from uiautomatorplug.android import device as d    
import commands
import re
import subprocess
import os
import string
import time
import sys
import util 
import unittest


u=util.Util()
#Written by Piao chengguo
#commands.getoutput('adb shell am start -n com.android.videoeditor/.ProjectsActivity')
# PATH
# key



#################################
PACKAGE_NAME = 'com.intel.android.gallery3d'
ACTIVITY_NAME = PACKAGE_NAME + '.app.Gallery'

class GalleryTest(unittest.TestCase):
    def setUp(self):
        super(GalleryTest,self).setUp()
        #Add on May 26th due to device always reboot by itself
        if d(text = 'Charged').wait.exists(timeout = 2000):
            commands.getoutput('adb root')
            time.sleep(5)
            commands.getoutput('adb remount')
            d.swipe(530,1300,1000,1300)



   

    def tearDown(self):
        super(GalleryTest,self).tearDown()
        self._pressBack(4)
        time.sleep(1)
########################################################

# Test case 1
    def testLaunchGalleryFromMS(self):
        commands.getoutput('adb shell am start -n com.android.videoeditor/.ProjectsActivity')
        #self._creatMovieStudioProject()
        time.sleep(2)
        d.swipe(550,550,551,551) #Hold on the first item in media list
        if d(text = 'Delete project').wait.exists(timeout = 2000):
            while d(text = 'Delete project').wait.exists(timeout = 2000):
                d(text = 'Delete project').click.wait()
                if d(text = 'Yes').wait.exists(timeout = 2000):
                    d(text = 'Yes').click.wait()
                time.sleep(2)
                d.swipe(550,550,551,551)
                if d(text = 'Cancel').wait.exists():
                    d(text = 'Cancel').click.wait()
        else:
            d(text = 'Cancel').click.wait()
        self.createMovie()
        for i in range(0,100):
            time.sleep(2)
            d(resourceId = 'com.android.videoeditor:id/add_new_media_item_menu').click.wait()        
            assert d(text = 'Import image').wait.exists(timeout = 1000),'enter import image menu fail'
            d(text = 'Import image').click.wait()
            time.sleep(1)
            self._selectIntelGallery()
            self._pressBack(1)

# Test case 2
    def testLaunchGalleryFromMMS(self):
        self._launchMMS()
        d(description ='Attach').click.wait()
        assert d(text = 'Attach').wait.exists(timeout =1000),'enter attach mode fail'
        d(text = 'Pictures').click.wait()
        if d(text ='Open from').wait.exists(timeout =2000):
            pass
        else:
            d(resourceId = 'android:id/up').click.wait()
            assert d(text ='Open from').wait.exists(timeout =2000)
        for i in range(0,100):
            time.sleep(2)
            d(index = 6).click.wait()
            assert d(packageName = 'com.intel.android.gallery3d').wait.exists(timeout =2000),'enter gallery fail'
            self._pressBack(1)
            time.sleep(1)    

# test case 3
    def testLaunchGalleryFromEmail(self):
        self._launchemail()
        d(resourceId = 'com.android.email:id/compose').click.wait()
        time.sleep(1)
        assert d(className = 'android.widget.ImageButton').wait.exists(timeout=1000),'enter new email fail'   
        d(className = 'android.widget.ImageButton').click.wait()
        assert d(text = 'Attach picture').wait.exists(timeout=1000),'enter menu fail'  
        d(text = 'Attach picture').click.wait()
        if not d(text = 'Gallery').wait.exists(timeout = 2000):
            d(resourceId = 'android:id/up').click.wait()
        for i in range(0,100):
            d(index = 6).click.wait()
            assert d(packageName = 'com.intel.android.gallery3d').wait.exists(timeout =2000),'enter gallery fail'
            self._pressBack(1)
            time.sleep(1)          

    def testLaunchGalleryFromContact(self):
        self._launchContact()
        assert d(resourceId = 'com.android.contacts:id/menu_add_contact').wait.exists(timeout=1000),'unable to add new contacts'
        d(resourceId = 'com.android.contacts:id/menu_add_contact').click.wait()
        if d(text ='Add account').wait.exists(timeout =1000):
            d(text ='Keep local').click.wait()
        time.sleep(1)
        if d(text ='OK').wait.exists(timeout =1000):
            d(text ='OK').click.wait()
        assert d(text = 'Done').wait.exists(timeout=1000),'create new contact fail' 
        d(resourceId = 'com.android.contacts:id/frame').click.wait()
        time.sleep(1)
        assert d(text = 'Choose photo from Gallery').wait.exists(timeout=1000),'enter select photo menu fail'
        d(text = 'Choose photo from Gallery').click.wait()
        time.sleep(2)
        assert d(text = 'Open from').wait.exists(timeout=2000),'enter choose photo from gallery menu fail'
        for i in range(0,100):
            d(index = 6).click.wait()
            assert d(packageName = 'com.intel.android.gallery3d').wait.exists(timeout =2000),'enter gallery fail'
            self._pressBack(1)
            time.sleep(1)









###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

#    def _creatMovieStudioProject(self):
#        commands.getoutput('adb shell am start -n com.android.videoeditor/.ProjectsActivity')
#        time.sleep(2)
#        assert d(resourceId = 'com.android.videoeditor:id/thumbnail').wait.exists(timeout=1000) 
#        d(resourceId = 'com.android.videoeditor:id/thumbnail').click.wait()        
#        if d(resourceId = 'com.android.videoeditor:id/add_new_media_item_menu').wait.exists(timeout = 3000):
#            #print 'created new project'
#            pass      
#        else:
#            assert d(text = 'Project name').wait.exists(timeout=1000),'fail'
#            time.sleep(1)
#            d(text = 'Project name').click()
#            time.sleep(1)
#            d(text = "Project name").set_text("newproject")
#            time.sleep(1)
#            d(text = 'OK').click.wait()
#            time.sleep(1)
#            assert d(resourceId = 'com.android.videoeditor:id/add_new_media_item_menu').wait.exists(timeout = 3000),'fail'
#        time.sleep(1)
#        self._pressBack(1)

    def createMovie(self):
        d(resourceId = 'com.android.videoeditor:id/thumbnail').click.wait()
        d(text = 'Project name').click.wait()
        d(text = 'Project name').set_text('newproject')
        d(text = 'OK').click.wait()
        #u.pressBack(1)

    def _selectIntelGallery(self):
        if d(resourceId = 'android:id/home').wait.exists(timeout=1000):
            assert d(packageName = 'com.intel.android.gallery3d').wait.exists(timeout =2000),'enter gallery fail'      
        else:
            d(text = 'com.intel.android.gallery3d').click.wait()
            time.sleep(1)
            d(text = 'Always').click.wait()
            time.sleep(1)             
            assert d(packageName = 'com.intel.android.gallery3d').wait.exists(timeout =2000),'enter gallery fail'
            


    def _launchMMS(self):
        commands.getoutput('adb shell am start -n com.android.mms/.ui.ConversationList')
        time.sleep(1)
        d(resourceId = 'com.android.mms:id/action_compose_new').click.wait()
        assert d(resourceId = 'com.android.mms:id/send_button_sms').wait.exists(timeout = 3000),'enter MMS send screen fail'

    def _launchemail(self):
        commands.getoutput('adb shell am start -n com.android.email/.activity.Welcome')
        time.sleep(2)
        if d(text ='Account setup').wait.exists(timeout=1000):
            #print 'login the email account'
            pass          
        else:
            assert d(resourceId = 'com.android.email:id/compose').wait.exists(timeout=2000),'enter email fail'
        time.sleep(1)                


    def _launchContact(self):
        commands.getoutput('adb shell am start -n com.android.contacts/.activities.PeopleActivity')
        time.sleep(2)
        if d(resourceId = 'com.android.contacts:id/menu_add_contact').wait.exists(timeout=1000):
            pass
        else:
            if d(text ='Make it Google').wait.exists(timeout=2000):
                d(text ='Not now').click.wait()
            if d(text ='Create a new contact').wait.exists(timeout=2000):
                print 'pls login the account'
            else:
                d().swipe.right()
                
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#



    def _pressBack(self,touchtimes):
        for i in range(0,touchtimes):
            d.press('back')

if __name__ =='__main__':  
    unittest.main()             
