#/usr/bin/kivy
import time, sys, kivy
from functools import partial

from kivy.app import App
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.properties import BooleanProperty, \
							StringProperty, \
							NumericProperty, \
							ObjectProperty


Config.set( 'graphics', 'width', '360' )
Config.set( 'graphics', 'height', '640' )


class BreakWidget( FloatLayout ):
	'''Kivy app that maintains a timer for breaks/work.
	Options for alarm sound and ability to set custom times.
	It can be paused and reset to null. A popup is created
	upon timer completion that prompts to continue to next
	mode or exit.
	'''
	
	#kivy properties
	
	#sound stuff
	sound 	    = BooleanProperty( False ) #Play alarm sound
	alarmSound  = SoundLoader.load( 'squish1.ogg' ) #sound for alarm
	
	#display strings
	timer 	    = StringProperty( '00:00' ) #String that represents time remaining
	message     = StringProperty( 'Set time(s)' ) #message to the user about the current state
	units	    = StringProperty( ' ' ) #minutes/seconds/etc
	pauseResume = StringProperty( 'Pause' ) #text on the pause/resume button
	progress = None
	
	#user input for work/break times
	workTime    = ObjectProperty()
	breakTime   = ObjectProperty()
	
	#variable
	total_pause_time = 0
	running = False

	def pauseTimer( self ):
		if self.running:
			self.running = not self.running
			self.pauseResume = 'Resume'
			
			Clock.unschedule( self.tick )
			self.pause_time = time.time()
			
		elif self.pauseResume == 'Resume':
			Clock.schedule_interval( self.tick, 1 )
			self.pauseResume = 'Pause'
			self.start_time += 1 #too account for delay between button release and graphic change
			self.resume_time = time.time()
			self.total_pause_time += ( self.resume_time - self.pause_time )
	
	def startBreak( self ):
	
		if not self.running:	
			try:
				self.timerSecs = int( self.breakTime.text ) * 60

				
				if self.breakTime.text < 10 :
					self.timer = '0' + self.breakTime.text + ':00'
				else:
					self.timer = self.breakTime.text + ':00'
				
				self.determineUnits( self.timerSecs )
					
				self.message = 'Don\'t do anything!'
				Clock.schedule_interval( self.tick, 1 )
				self.start_time = time.time()
				self.progress = 0
				
			except ValueError:
				self.popupMode = 'break'
				self.popupMessage()

				
	def startWork( self ):
	
		if not self.running:	
			try:
				self.timerSecs = int( self.workTime.text ) * 60

				
				if self.workTime.text < 10 :
					self.timer = '0' + self.workTime.text + ':00'
				else:
					self.timer = self.workTime.text + ':00'
				
				self.determineUnits( self.timerSecs )
					
				self.message = 'Accomplish much!'
				Clock.schedule_interval( self.tick, 1 )
				self.start_time = time.time()
				self.progress = 0
				
			except ValueError:
				self.popupMode = 'work'
				self.popupMessage()
				
				
	def tick( self, *largs ):
		'''Updates the timer based on a start time.time() and updates
		GUI appropriately. Also calls the function to end the timer/clock
		when necessary'''

		def checkFinished( timer_secs ):
		#simple test to determine if the timer is done
			if timer_secs <= 0:
				return True
			else:
				return False

				
		self.running = True
		
		#determine how long it's been since we started
		passedTime = ( time.time() - self.start_time ) - self.total_pause_time
		
		#figure out how much longer the timer has
		timerSecRemain = int ( self.timerSecs - passedTime )

		#make the strings for the timer to display, adding lead zeros
		dispMin = self.addLeadZero( timerSecRemain / 60 )
		dispSec = self.addLeadZero( timerSecRemain % 60 )
		
		#reflect changes in the gui; units, timer, progress bar
		self.determineUnits( timerSecRemain )
		self.timer = '{0}:{1}'.format( dispMin, dispSec )
		self.set_progress( passedTime )
		
		#if the timer runs out, end the timer (play sound, unschedule tick, popup)
		if checkFinished( timerSecRemain ):
			self.end_timer()
	
	def end_timer( self ):
		'''checks for sounds on/off.
		Unschedules the tick function, calls the popup
		and stops the timer from running '''

		if self.sound:
			self.alarmSound.play()
			
		Clock.unschedule( self.tick )
		self.running = False
		self.message = 'Set time(s)'
		self.popupMessage()
		
	def build_popup( self, wd_text ):

		start_button = Button( text = wd_text[2], 
							size_hint_y = None,
							height = '50sp' )
							
		close_button = Button( text = 'Exit',
							size_hint_y = None,
							height = '50sp' )
		
		content = BoxLayout( orientation = 'vertical' )
		content.add_widget( Label( text = wd_text[1] ) )
		
		if wd_text[0][0] == 'E':
			textbox = BoxLayout( size_hint = ( 0.75, 0.5 ), spacing = 10 )
			self.new_time = TextInput(font_size = 30)
			textbox.add_widget( Label() )
			textbox.add_widget( self.new_time )
			textbox.add_widget( Label( text = 'minutes' ) )
			content.add_widget( textbox )
			
		button_layout = BoxLayout( orientation = 'horizontal' )
		button_layout.add_widget( start_button )
		button_layout.add_widget( close_button )

			
		content.add_widget( button_layout )

		self.p = Popup( title = wd_text[0],
					size_hint = ( 0.85, 0.5 ),
					content = content,
					auto_dismiss = False )

		start_button.bind( on_release = partial( self.close_popup, wd_text[0][0] ) )
		close_button.bind( on_release = partial( self.close_popup, None ) )
	
		self.p.open()
			
	def popupMessage( self ):
	  
		if self.message[0] == 'D': #break
			self.build_popup( [ 'Breaktime Over!', 
								'Nice job slacker.\nNow get ready to work!',
								'Start working' ] )
			
		elif self.message[0] == 'A': #work
			self.build_popup( [ 'Worktime Over!', 
								'Good work! (I hope...)', 
								 'Start break'] )
								 
		elif self.message[0] == 'S':
			self.build_popup([ 'Enter a time', 
			'You\'re missing a time for your {}!'.format( self.popupMode ), 
			'Enter'] )
								 
					
	def close_popup( self, ending_mode, *largs ):
	
		if ending_mode == 'B': #break just ended
			self.startWork()
			
		if ending_mode == 'W': #work just ended
			self.startBreak()
			
		if ending_mode == 'E':
			if self.new_time.text.isdigit():		
				if self.popupMode == 'break':
						self.breakTime.text = self.new_time.text
						self.startBreak()
					
				elif self.popupMode == 'work':

						self.workTime.text = self.new_time.text
						self.startWork()
			else:
				return 0
		self.p.dismiss()			

#these are set	####			
	def set_progress(self, completedSecs ):
		self.progress = 1 + int( ( completedSecs / self.timerSecs ) * 100 )
	
	def reset( self ):
		'''Sets everything back to default when reset button is released'''
		Clock.unschedule( self.tick )
		self.running = False
		self.progress = 0
		self.timer = '00:00'
		self.units = ' '
		self.message = 'Set time(s)'

	def determineUnits( self, time_remaining ):
		'''given the seconds, determine the correct units/grammar'''
		if time_remaining > 60:
			self.units == 'Minutes'
		elif time_remaining == 60:
			self.units = 'Minute'
		elif time_remaining < 60:
			self.units = 'Seconds'
		elif time_remaining == 1:
			self.units = 'Second'
		
	def addLeadZero( self, number ):
		if number % 10 != 0 and number < 10 or number == 0:
			number = '0' + str( number )
		return number	

class BreakApp( App ):
	def build( self ):
		return BreakWidget()
	



do_this = BreakApp()
do_this.run()
