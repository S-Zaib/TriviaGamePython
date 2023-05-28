# Python program to create a simple GUI
# Simple Quiz using Tkinter

#import everything from tkinter
import random
from tkinter import *

# and import messagebox as mb from tkinter
from tkinter import messagebox as mb

#import json to use json file for data
import json

class MainMenu:
    def __init__(self):
        self.main_menu = Tk()
        self.main_menu.geometry("300x250")
        self.main_menu.title("Trivia Game")
        self.main_menu.configure(background="cyan")
        self.main_menu.resizable(0,0)


        # Create a frame to contain the buttons
        button_frame = Frame(self.main_menu)
        button_frame.pack(pady=20)
		# match the background colour of the frame to the main menu
        button_frame.configure(background="cyan")

        # Configure button styles in colour yellow
        button_style = {"background": "yellow", "font": ("ariel", 16, "bold")}
        # Play button
        self.play_button = Button(button_frame, text="Play", command=self.play, **button_style)
        self.play_button.pack(pady=10)

		# Quit button
        self.quit_button = Button(button_frame, text="Controls", command=self.controls, **button_style)
        self.quit_button.pack(pady=10)

        # Quit button
        self.quit_button = Button(button_frame, text="Quit", command=self.main_menu.destroy, **button_style)
        self.quit_button.pack(pady=10)

        self.quiz = None

    def play(self):
        self.quiz = Quiz()
        self.main_menu.withdraw()


    def controls(self):
        mb.showinfo("Controls", "Player 1 - Space Bar \nPlayer 2 - Enter Key")


#class to define the components of the GUI
class Quiz:
	# This is the first method which is called when a
	# new object of the class is initialized. This method
	# sets the question count to 0. and initialize all the
	# other methoods to display the content and make all the
	# functionalities available
	def __init__(self):

		self.gui = Toplevel()
		self.gui.geometry("800x450")
		self.gui.title("Trivia Game")
		self.gui.configure(background="cyan")
		self.gui.resizable(0,0)
		self.gui.focus_force()

		# This is the variable to store the current player
		self.player_chosen = IntVar()

		# opt_selected holds an integer value which is used for
		# selected option in a question.
		self.opt_selected=IntVar()
		
		# displaying radio button for the current question and used to
		# display options for the current question
		
		# no of questions
		self.data_size=len(questions)
		
		# keep a counter of correct answers
		self.correct=[0,0]

		# set question number to 0
		self.q_no=0
		self.opts = []
		# assigns ques to the display_question function to update later.
		self.display_title()
		self.display_player()
		self.display_question()	
		self.gui.bind("<KeyPress>", self.choosePlayer)

	# This method is used to choose player based on who reacts faster by pressing the space bar for p1 and enter for p2
	def choosePlayer(self, event):
		# cover the options with a white rectangle
		while(self.player_chosen.get() == 0):

			if event.keysym == "space":
				self.player_chosen.set(1)
				print("Player 1", self.player_chosen.get())
				self.show_rest()


			elif event.keysym == "Return":
				self.player_chosen.set(2)
				print("Player 2", self.player_chosen.get())
				self.show_rest()




	def show_rest(self):
		self.display_player()

		self.opts=self.radio_buttons()
		
		# display options for the current question
		self.display_options()
		
		# displays the button for next and exit.
		self.buttons()



	# This method is used to display the result
	# It counts the number of correct and wrong answers
	# and then display them at the end as a message Box
	def display_result(self):
		
		# calculates the wrong count
		wrong_count1 = self.data_size - self.correct[0]
		correct1 = f"Correct: {self.correct[0]}"
		wrong1 = f"Wrong: {wrong_count1}"

		wrong_count2 = self.data_size - self.correct[1]
		correct2 = f"Correct: {self.correct[1]}"
		wrong2 = f"Missed/Wrong: {wrong_count2}"
		
		# calcultaes the percentage of correct answers
		score1 = int(self.correct[0] / self.data_size * 100)
		score2 = int(self.correct[1] / self.data_size * 100)
		result1 = f"Score: {score1}%"
		result2 = f"Score: {score2}%"
		
		# Shows a message box to display the result
		mb.showinfo("Player 1", f"{result1}\n{correct1}\n{wrong1}")
		mb.showinfo("Player 2", f"{result2}\n{correct2}\n{wrong2}")

		# store in log
		self.store_log(self.correct[0], self.correct[1])

	def store_log(self, score1, score2):
		# open file
		f = open("log.txt", "a")
		# write to file
		f.write(f"Player 1: {score1}%\nPlayer 2: {score2}%\n\n")
		# close file
		f.close()


	# This method checks the Answer after we click on Next.
	def check_ans(self, q_no):
		
		# checks for if the selected option is correct
		if self.opt_selected.get() == answers[q_no]:
			# if the option is correct it return true
			return True

	# This method is used to check the answer of the
	# current question by calling the check_ans and question no.
	# if the question is correct it increases the count by 1
	# and then increase the question number by 1. If it is last
	# question then it calls display result to show the message box.
	# otherwise shows next question.
	def next_btn(self):
		# Check if the answer is correct
		if self.check_ans(self.q_no):
			
			# if the answer is correct it increments the correct by 1
			self.correct[self.player_chosen.get()-1] += 1
		
		# Moves to next Question by incrementing the q_no counter
		self.q_no += 1
		
		# checks if the q_no size is equal to the data size
		if self.q_no==self.data_size:
			
			# if it is correct then it displays the score
			self.display_result()
			
			# destroys the GUI
			self.gui.destroy()
		else:
			# shows the next question
			self.display_question()
			self.gui.bind("<KeyPress>", self.choosePlayer)

	# This method shows the two buttons on the screen.
	# The first one is the next_button which moves to next question
	# It has properties like what text it shows the functionality,
	# size, color, and property of text displayed on button. Then it
	# mentions where to place the button on the screen. The second
	# button is the exit button which is used to close the GUI without
	# completing the quiz.
	def buttons(self):
		
		# The first button is the Next button to move to the
		# next Question
		next_button = Button(self.gui, text="Next",command=self.next_btn,
		width=10,bg="blue",fg="white",font=("ariel",16,"bold"))
		
		# placing the button on the screen
		next_button.place(x=350,y=380)
		
		# This is the second button which is used to Quit the GUI
		quit_button = Button(self.gui, text="Quit", command=self.gui.destroy,
		width=5,bg="black", fg="white",font=("ariel",16," bold"))
		
		# placing the Quit button on the screen
		quit_button.place(x=700,y=50)


	# This method deselect the radio button on the screen
	# Then it is used to display the options available for the current
	# question which we obtain through the question number and Updates
	# each of the options for the current question of the radio button.
	def display_options(self):
		val=0
		
		# deselecting the options
		self.opt_selected.set(0)

		# looping over the options to be displayed for the
		# text of the radio buttons.
		for option in options[self.q_no]:
			self.opts[val]['text']=option
			val+=1

	def destroy_options(self):
		for opt in self.opts:
			opt.destroy()


	# This method shows the current Question on the screen
	def display_question(self):
		self.opt_selected.set(0)
		self.player_chosen.set(0)
		self.destroy_options()


		
		# setting the Question properties
		q_no = Label(self.gui, text=questions[self.q_no], width=60,
		font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		
		#placing the option on the screen
		q_no.place(x=70, y=100)


	# This method is used to Display Title
	def display_title(self):
		
		# The title to be shown
		title = Label(self.gui, text="React Quick!",
		width=50, bg="blue",fg="white", font=("ariel", 20, "bold"))
		
		# place of the title
		title.place(x=0, y=2)

	def display_player(self):

		# The title to be shown
		title = Label(self.gui, text="Player: " + self.getPlayer(),
		width=50, bg="cyan",fg="blue", font=("ariel", 18, "bold"))
		
		# place of the title
		title.place(x=0, y=52)


	def getPlayer(self):
		if(self.player_chosen.get() == 0):
			return "-"
		else:
			return str(self.player_chosen.get()) + " Score: " + str(self.correct[self.player_chosen.get()-1])

	# This method shows the radio buttons to select the Question
	# on the screen at the specified position. It also returns a
	# list of radio button which are later used to add the options to
	# them.
	def radio_buttons(self):
		
		# initialize the list with an empty list of options
		q_list = []
		
		# position of the first option
		y_pos = 150
		# adding the options to the list
		for val, opt in enumerate(options[self.q_no]):
			val += 1
			print(opt, val)
			# setting the radio button properties
			radio_btn = Radiobutton(self.gui,text=" ",value = val, font = ("ariel",14))
			radio_btn.configure(command=lambda btn=radio_btn: self.clicked(btn))

			
			# adding the button to the list
			q_list.append(radio_btn)
			
			# placing the button
			radio_btn.place(x = 100, y = y_pos)
			
			# incrementing the y-axis position by 40
			y_pos += 40

			# incrementing the value of radio button by 1
		
		# return the radio buttons
		return q_list

	def clicked(self, val):
		print("clicked", val['value'])
		self.opt_selected.set(val['value'])

def divide_content(file_name):
    questions = []
    options = []
    answers = []

    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            question = lines[i].strip()
            options_arr = []

            i += 1
            while not lines[i].startswith('Správna odpoveď:'):
                options_arr.append(lines[i].strip())
                i += 1

            temp = lines[i].split(':')[1].strip()
            answer = ord(temp[0]) - ord('a') + 1

            questions.append(question)
            options.append(options_arr)
            answers.append(answer)

            i += 2

    return questions, options, answers

def format_content(file_name):
	questions = []
	answers = []
	options = []

	with open(file_name, 'r', encoding='utf-8') as file:
		lines = file.readlines()
		for line in lines:
			if(line == '\n'):
				continue
			options.append(['Áno', 'Nie'])
			line = line.strip()
			question_end_index = line.find('?')
			if question_end_index != -1:
				question = line[:question_end_index + 1]
				questions.append(question)
				if(line[question_end_index + 1:].strip().startswith('Áno')):
					answers.append(1)
				else:
					answers.append(2)

	return questions, options, answers

# get the question, options, and answer
question_abcd, options_abcd, answer_abcd = divide_content('otazky-abcd.txt')
question_yn, options_yn, answer_yn = format_content('otazky-slovo.txt')
question_solve, options_solve, answer_solve= format_content('otazky-slovo.txt')

# now fill the qrray questions, options, and answer with 3 random questions from each type
questions = []
options = []
answers = []

# get 3 random questions from each type
for i in range(3):
	randIDX = random.randint(0, len(question_abcd) - 1)
	questions.append(question_abcd[randIDX])
	options.append(options_abcd[randIDX])
	answers.append(answer_abcd[randIDX])

	randIDX = random.randint(0, len(question_yn) - 1)

	questions.append(question_yn[randIDX])
	options.append(options_yn[randIDX])
	answers.append(answer_yn[randIDX])

	randIDX = random.randint(0, len(question_solve) - 1)

	questions.append(question_solve[randIDX])
	options.append(options_solve[randIDX])
	answers.append(answer_solve[randIDX])







#display questions, options, and answer
print(questions)
print(options)
print(answers)



# Create a GUI window for the main menu
main_menu = MainMenu()

# Start the GUI
main_menu.main_menu.mainloop()


