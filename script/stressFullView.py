#!/usr/bin/python
# coding:utf-8

from uiautomatorplug.android import device as d
import unittest
import commands
import string
import time
import sys
import util
import os

u = util.Util()

PACKAGE_NAME = 'com.intel.android.gallery3d'
ACTIVITY_NAME = PACKAGE_NAME + '/.app.Gallery'

class GalleryTest(unittest.TestCase):
    def setUp(self):
        super(GalleryTest,self).setUp()
        #Add on May 26th due to device always reboot by itself
        if d(text = 'Charged').wait.exists(timeout = 2000):
            commands.getoutput('adb root')
            time.sleep(5)
            commands.getoutput('adb remount')
            d.swipe(530,1300,1000,1300)
        u._clearAllResource()
        


    def tearDown(self):
        super(GalleryTest,self).tearDown()
        u.pressBack(4)

    def testCropPicture(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            u.setMenuOptions('Crop')
            assert d(text = 'Crop picture').wait.exists(timeout = 3000)
            d(text = 'Crop').click.wait()
            assert d(text = 'Crop').wait.gone(timeout = 2000)

    def testCropPictureCancel(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            u.setMenuOptions('Crop')
            assert d(text = 'Crop picture').wait.exists(timeout = 3000)
            d(text = 'Cancel').click.wait()
            assert d(text = 'Crop').wait.gone(timeout = 2000)

    def testAddEvent(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        u.setMenuOptions('Details')
        for i in range(100):
            d(resourceId = 'com.intel.android.gallery3d:id/event_edit').click.wait()
            d(text = 'Enter new event').click.wait() #Make sure keyboard has been invoked
            d(text = 'Enter new event').set_text('NewEvent')
            self._tapOnDoneButton()
            assert d(text = 'NewEvent',resourceId = 'com.intel.android.gallery3d:id/event_text').wait.exists(timeout = 2000)
            #Delete the added event
            d(resourceId = 'com.intel.android.gallery3d:id/event_edit').click.wait()
            d(resourceId = 'com.intel.android.gallery3d:id/search_text_clear').click.wait() #Tap on X button to clear event
            self._tapOnDoneButton()
            assert d(text = 'Add an event').wait.exists(timeout = 2000)

    def testAddPlace(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        u.setMenuOptions('Details')
        for i in range(100):
            d(resourceId = 'com.intel.android.gallery3d:id/venue_edit').click.wait()
            d(text = 'Enter new venue').click.wait() #Make sure keyboard has been invoked
            d(text = 'Enter new venue').set_text('NewVenue')
            self._tapOnDoneButton()
            assert d(text = 'NewVenue',resourceId = 'com.intel.android.gallery3d:id/venue_text').wait.exists(timeout = 2000)
            #Delete the added place
            d(resourceId = 'com.intel.android.gallery3d:id/venue_edit').click.wait()
            d(resourceId = 'com.intel.android.gallery3d:id/search_text_clear').click.wait() #Tap on X button to clear venue
            self._tapOnDoneButton()
            assert d(text = 'Add a venue').wait.exists(timeout = 2000)

    def testTagOnePicture(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        u.setMenuOptions('Details')
        for i in range(100):
            d.swipe(1000,1600,1000,200) #Swipe detail list up
            d(resourceId = 'com.intel.android.gallery3d:id/addKeywordButton').click.wait()
            d(text = 'Enter new keyword').click.wait() #Make sure keyboard has been invoked
            d(text = 'Enter new keyword').set_text('NewKeyword')
            self._tapOnDoneButton()
            assert d(text = 'NewKeyword',className = 'android.widget.TextView').wait.exists(timeout = 2000)

    def testSetAsContact(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            self._setPicAs('contact')
            u.tapOnCenter() #Select the contact in the center of the list
            if d(text = 'Complete action using').wait.exists(timeout = 2000):
                try:
                    assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
                except:
                    d(text = 'com.intel.android.gallery3d').click.wait()
                finally:
                    d(text = 'Always').click.wait()
            time.sleep(2)
            d(text = 'Crop').click.wait()
            assert d(description = 'Share').wait.exists(timeout = 2000)

    def testSetAsWallpaper(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            self._setPicAs('wallpaper')
            if d(text = 'Complete action using').wait.exists(timeout = 2000):
                try:
                    assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
                except:
                    d(text = 'com.intel.android.gallery3d').click.wait()
                finally:
                    d(text = 'Always').click.wait()
            d(text = 'Crop').click.wait()
            assert d(description = 'Share').wait.exists(timeout = 2000)

    def testViewPicture(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            d.press('back') #If it goes to fullview suc, it shall back to the grid view after pressing back key
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)
            u.pressBack(4)
            u.launchGallery()
            u.enterXView('fullview')

    def testUPIcon(self):
        u._confirmResourceExists()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            d(resourceId = 'android:id/home').click.wait()
            assert d(description = 'Switch to camera').wait.exists(timeout = 2000)
            u.pressBack(4)
            u.launchGallery()
            u.enterXView('fullview')
            u.showPopCard()

    def testSlidePicture(self):
        self._clearAndPush500Pic()
        u.launchGallery()
        u.enterXView('fullview')
        d.click(550,150)
        d.click(550,150)
        time.sleep(10)
        assert d(description = 'Share').wait.exists(timeout = 5000), 'Pop card does not display after tapping on the top bar twice'       
        for i in range(10):
            for j in range(10):
                self._slideImageRtoL()
            for k in range(10):
                self._slideImageLtoR()

    def testDeleteOneByOne(self):
        self._clearAndPush500Pic()
        u.launchGallery()
        u.enterXView('fullview')
        u.showPopCard()
        for i in range(100):
            d(description = 'Delete').click.wait()
            d(text = 'Delete').click.wait() #Confirm it

    def testPlayPauseVideo(self):
        self._clearAndPushVideo()
        u.launchGallery()
        u.enterXView('fullview')
        for i in range(100):
            u.showPopCard()
            u.tapOnCenter() #Press playback icon
            if d(text = 'Complete action using').wait.exists(timeout = 2000):
                try:
                    assert d(text = 'Always', enabled = 'true').wait.exists(timeout = 2000)
                except:
                    d(text = 'com.intel.android.gallery3d').click.wait()
                finally:
                    d(text = 'Always').click.wait()
            time.sleep(10) #Play video file 10 s
            d.click(550,150)
            d.click(550,150) #Invoke pop card
            u.tapOnCenter() #Pause the video playback
            assert d(resourceId = 'com.intel.android.gallery3d:id/background_play_action_provider_button').wait.exists(timeout = 2000)
            #d(resourceId = 'android:id/up').click.wait() #Back to the fullview
            u.pressBack(1)





    def _clearAndPushVideo(self):
        commands.getoutput('adb shell rm -r /mnt/sdcard/testalbum/')
        #commands.getoutput('adb push ' + os.getcwd() + '/resource/testvideo/ ' + '/sdcard/testvideo')
        commands.getoutput('adb push ' + PATH + '/script/resource/testvideo/ ' + '/sdcard/testvideo')
        #Refresh media
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')

    def _clearAndPush500Pic(self):
        commands.getoutput('adb shell rm -r /mnt/sdcard/testalbum/')
        #commands.getoutput('adb push ' + os.getcwd() + '/resource/testStress500pic/ /sdcard/testStress500pic')
        commands.getoutput('adb push ' + PATH + '/script/resource/testStress500pic/ ' + '/sdcard/testStress500pic')
        #Refresh media
        commands.getoutput('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')

    def _setPicAs(self,setact):
        d.press('menu')
        d(text = 'Set picture as').click.wait()
        setmode = {'contact':'Contact photo', 'wallpaper':'com.intel.android.gallery3d'}
        d(text = setmode[setact]).click.wait()

    def _tapOnDoneButton(self):
        #Touch on Done button on the soft keyboard
        d.click(1100,1660)

    def _slideImageRtoL(self):
        #Swipe screen from right to left
        d.swipe(1000,1000,1,1000,2)
        time.sleep(2)

    def _slideImageLtoR(self):
        #Swipe screen from left to right
        d.swipe(1,1000,1000,1000,2)
        time.sleep(2)
