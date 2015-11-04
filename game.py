from kivy.app import App

from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from random import randint

import button
import time
import threading

#import RPi.GPIO as GPIO
#import button

class GameUI(BoxLayout):
    
    # keep states of button for each player
    # [0] [1] [2] : buttons for each bit
    # [3] : confirm button
    player1_answer = [False, False, False, False]
    player2_answer = [False, False, False, False]
    #is player submit check
    is_one_submit = False
    is_two_submit = False
    # variables to store whether each player has pressed
    # submit button or not
    submited_one = False
    submited_two = False
    submited_array = []
    
    # variable to store number of match count left
    #match_count = 3
    
    # variable to store if key is being pressed
    is_key_down = False
    
    # To simulate GPIO ports
    player1_btn_states = [False, False, False, False]
    player2_btn_states = [False, False, False, False]
    
    
    def __init__(self, **kwargs):
        super(GameUI, self).__init__(**kwargs)          
        
        # Initialize keyboard
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)  
        
        # Generate random number
        self.random()
        self.ids['top_layout'].markup = True
        # Start game loop on another thread
        threading.Thread(target=self.super_loop, args=()).start()
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        
        print keycode
        
        if not self.is_key_down:

            #for player one hit
            if keycode[1] == 'z':
                self.player1_btn_states[0] = True
            elif keycode[1] == 'x':
                self.player1_btn_states[1] = True
            elif keycode[1] == 'c':
                self.player1_btn_states[2] = True

            #for player 2 hit
            elif keycode[1] == 'm':
                self.player2_btn_states[0] = True
            elif keycode[1] == ',':
                self.player2_btn_states[1] = True
            elif keycode[1] == '.':
                self.player2_btn_states[2] = True

            #for both player submit hit
            elif keycode[1] == 'v':
                self.player1_btn_states[3] = True
            elif keycode[1] == '/':
                self.player2_btn_states[3] = True
                
            # update keydown flag
            self.is_key_down = True
            
    def _on_keyboard_up(self, keyboard, keycode):

        #for player 1 release
        if keycode[1] == 'z':
            self.player1_btn_states[0] = False
        elif keycode[1] == 'x':
            self.player1_btn_states[1] = False
        elif keycode[1] == 'c':
            self.player1_btn_states[2] = False

        #for player 2 release
        elif keycode[1] == 'm':
            self.player2_btn_states[0] = False
        elif keycode[1] == ',':
            self.player2_btn_states[1] = False
        elif keycode[1] == '.':
            self.player2_btn_states[2] = False

        #for player 1 ans 2 release submit
        elif keycode[1] == 'v':
            self.player1_btn_states[3] = False
        elif keycode[1] == '/':
            self.player2_btn_states[3] = False
                
        # reset key_down flag
        self.is_key_down = False

    def super_loop(self):
        
        previous_states = [False for i in range(8)]

        player1_prev_states = previous_states[:4]
        player2_prev_states = previous_states[4:]
        
        while True:
            
            # Handle state updates for each button
            
            #states = button.button_stage()
            #time.sleep(0.3)
            
            # Current states
            states = self.player1_btn_states + self.player2_btn_states

            print states
            print "for second round check p1 prev",player1_prev_states
            print "for second round check p2 prew",player2_prev_states

            player1_current_states = states[:4]
            print "player 1 current state", player1_current_states
            player2_current_states = states[4:]
            print "player 2 current state", player2_current_states
            
            #check state change for bot player and their new state must also be HIGH
	        #it is showing that state of buttons changed from unpressed to pressed
            if not self.is_one_submit:
                for i in range(len(player1_current_states)):
                    if (player1_current_states[i] != player1_prev_states[i]) and (player1_current_states[i] == True):
                        self.player1_answer[i] = not self.player1_answer[i]

            if not self.is_two_submit:
                for i in range(len(player2_current_states)):
                    if (player2_current_states[i] != player2_prev_states[i]) and (player2_current_states[i] == True):
                        self.player2_answer[i] = not self.player2_answer[i]
                    
            player1_prev_states = player1_current_states
            player2_prev_states = player2_current_states
            
            
            # Handle submission buttons
            # We check if we have winner here
            # we use 3 and 7 becase they are the last button of both players
            self.handle_submit_btn(states[3], states[7])
            
            # Update label for each player to match current players' answer
            self.update_labels()
            
            # If both players has submit their result, check for winner
            print "this is the submitted array", self.submited_array
            if len(self.submited_array) == 2:
                #self.match_count -= 1
                self.check_winner()
            
            '''
            
            time.sleep(3)
            self.player1_btn_states = (True, False, False, True)
            self.player2_btn_states = (False, True, False, False)
            '''

    # Update binary text on screen to reflect current answer of each player
    def update_labels(self):
        # Convert True/False values into 0 or 1 ( O for false and 1 for true )
        player1_bits = self.player1_answer[0:3]
        player2_bits = self.player2_answer[0:3]
        p1_values = ["1" if state else "0" for state in player1_bits]
        p2_values = ["1" if state else "0" for state in player2_bits]
        # Update label representing answer for each player

        # ROBROO DEBUG
        # self.ids['player_one_number'].text = ' '.join(p1_values)
        # self.ids['player_two_number'].text = ' '.join(p2_values)


        if not self.is_one_submit and not self.is_two_submit:
            self.ids['player_one_number'].text = ' '.join(p1_values)
            self.ids['player_one_number'].markup = True
            self.ids['player_two_number'].text = ' '.join(p2_values)
            self.ids['player_two_number'].markup = True
        elif self.is_one_submit and not self.is_two_submit:
            self.ids['player_one_number'].text = '[color=868686]' + ' '.join(p1_values) + '[/color]'
            self.ids['player_one_number'].markup = True
            self.ids['player_two_number'].text = ' '.join(p2_values)
            self.ids['player_two_number'].markup = True
        elif not self.is_one_submit and self.is_two_submit:
            self.ids['player_one_number'].text = ' '.join(p1_values)
            self.ids['player_one_number'].markup = True
            self.ids['player_two_number'].text = '[color=868686]' + ' '.join(p2_values) + '[/color]'
            self.ids['player_two_number'].markup = True
        else:
            self.ids['player_one_number'].text = '[color=868686]' + ' '.join(p1_values) + '[/color]'
            self.ids['player_one_number'].markup = True
            self.ids['player_two_number'].text = '[color=868686]' + ' '.join(p2_values) + '[/color]'
            self.ids['player_two_number'].markup = True

    # Handle submit button_stage
    # When button state is HIGH, append player to submited_array
    # according to player number
    def handle_submit_btn(self, submit1, submit2):
        # Append into submited_array in order depending on which player submit first
        # we append if and only if it was not append before
        if (submit1) and ("Player 1" not in self.submited_array):
            self.submited_array.append("Player 1")
            self.is_one_submit = True
            self.ids['player_one_stat'].text = '[color=3399ff]SUBMITTED[/color]'
            self.ids['player_one_stat'].markup = True

        elif (submit2) and ("Player 2" not in self.submited_array):
            self.submited_array.append("Player 2")
            self.is_two_submit = True
            self.ids['player_two_stat'].text = '[color=3399ff]SUBMITTED[/color]'
            self.ids['player_two_stat'].markup = True


    # This function show winner by checking each player's answer
    # with self.rand_number
    def check_winner(self):
        # Variable to keep correct answer
        correct_answer = self.rand_number
        print "correct ans", correct_answer

        # Calculate answer in decimal number
        player1_final_answer = (self.player1_answer[0] * 4) + (self.player1_answer[1] * 2) + (self.player1_answer[2] * 1)
        player2_final_answer = (self.player2_answer[0] * 4) + (self.player2_answer[1] * 2) + (self.player2_answer[2] * 1)

        print "player one ans ",player1_final_answer
        print "player two ans ",player2_final_answer
        # Both players give correct answer
        if player1_final_answer == correct_answer and player2_final_answer == correct_answer:
            # Break tie with index of submited_array
            self.ids['top_layout'].text  = '[color=99ff33]' + str(self.submited_array[0]) + " WON!!" + '[/color]'
        # Only player 1 gives correct answer
        elif correct_answer == player1_final_answer:
            self.ids['top_layout'].text  = '[color=99ff33]Player 1 Won[/color]'
        # Only player 2 gives correct answer            
        elif correct_answer == player2_final_answer:
            self.ids['top_layout'].text  = '[color=99ff33]Player 2 Won[/color]'
        # None of them gives correct answer
        else:
            self.ids['top_layout'].text = '[color=ff3333]DRAW[/color]'
        
        # Let player feels the pain for 5 seconds
        time.sleep(5)
        # Reset everything except match_count
        self.reset()
        
    def reset(self):
        self.player1_answer = [False, False, False, False]
        self.player2_answer = [False, False, False, False]
    
        self.submited_one = False
        self.submited_two = False
        self.submited_array = []
        self.is_one_submit = False
        self.is_two_submit = False
        self.random()

        self.ids['player_one_stat'].text = ''
        self.ids['player_two_stat'].text = ''

    # Generate random number and set to Layout
    # we can access random number via selxz.rand_number
    def random(self):
        self.rand_number = randint(1,7)
        self.ids['top_layout'].text  = str(self.rand_number)
    

class TutorialApp(App):
    def build(self):
        return GameUI()

if __name__ == "__main__":
    TutorialApp().run()
