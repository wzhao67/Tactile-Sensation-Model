from Tkinter import *

class UI(Frame):
    
    def __init__(self, master):
        """initialize the frame"""
        Frame.__init__(self, master)
        
        #contains flags representing sets of unlabelled input data
        self.unlabelled_inputs = []
        #number of single point data, if included. Defaults to 0 if not
        self.num_SPs = 0    
        #contains flags representing sets of labelled input data
        self.labelled_inputs = []
        #input point sigma, defaults to 2.0
        self.unlabelled_sigma = 2.0
        self.labelled_sigma = 2.0
        #number of hidden units, defaults to 84
        self.num_hidden_units = 84
        #force pixelation, defaults to 0 if none
        self.pixelation_sigma = 0
        #training epochs, defaults to 100
        self.unlabelled_epochs = 100
        self.labelled_epochs = 100
        #regularization constants, default to 0.01
        self.unlabelled_lambda = 0.01
        self.labelled_lambda = 0.01
        #learning rates, default to 0.1
        self.unlabelled_LR = 0.1
        self.labelled_LR = 0.1
        
        self.grid()
        self.create_input_widgets()
        self.create_hidden_layer_widgets()
        self.create_macro_widgets()
        
    def create_input_widgets(self):
        """Create check buttons and text boxes for input data options"""
        
        #Options for labelled data used in Autoencoder training
        self.input_title = Label(self, text = "*** Unlabelled input data *** ")
        self.input_title.grid(row = 0, column = 0, columnspan = 2, sticky = W)
        
        #single point data
        self.single_points = BooleanVar()
        Checkbutton(self, text = "Single Points", variable = self.single_points).grid(row = 1, column = 0, sticky = W)
        self.single_point_title = Label(self, text = "Number: ")
        self.single_point_title.grid(row = 2, column = 0, sticky = W)
        self.num_single_points = Entry(self)
        self.num_single_points.grid(row = 2, column = 1, sticky = W)
        
        #single and double point data
        self.mixed_points = BooleanVar()
        Checkbutton(self, text = "30000 1&2 Points", variable = self.mixed_points).grid(row = 3, column = 0, sticky = W)
        
        #Helvetica alphabet data
        self.alphabet = BooleanVar()
        Checkbutton(self, text = "31200 alphabets", variable = self.alphabet).grid(row = 4, column = 0, sticky = W)
        
        #Braille alphabet data
        self.braille = BooleanVar()
        Checkbutton(self, text = "31200 Braille", variable = self.braille).grid(row = 5, column = 0, sticky = W)
        
        #Point data sigma
        self.l_data_sigma1 = Label(self, text = "Point input sigma: ")
        self.l_data_sigma1.grid(row = 6, column = 0, sticky = W)
        self.t_data_sigma1 = Entry(self)
        self.t_data_sigma1.grid(row = 6, column = 1, sticky = W) 
        
        #Options for labelled data used in Autoencoder training
        self.input_title_labelled = Label(self, text = "*** Labelled input data ***")
        self.input_title_labelled.grid(row = 0, column = 2, columnspan = 2, stick = W)
        
        #single and double point data, used for TPDT
        self.mixed_points_labelled = BooleanVar()
        Checkbutton(self, text = "30000 1&2 Points", variable = self.mixed_points_labelled).grid(row = 1, column = 2, sticky = W)
        
        #Helvetica alphabet data, used for letter classification
        self.alphabet_labelled = BooleanVar()
        Checkbutton(self, text = "31200 alphabets", variable = self.alphabet_labelled).grid(row = 2, column = 2, sticky = W)
        
        #Braille alphabet data, used for Braille letter classification
        self.braille_labelled = BooleanVar()
        Checkbutton(self, text = "31200 Braille", variable = self.braille_labelled).grid(row = 3, column = 2, sticky = W)   
        
        #Point data sigma
        self.l_data_sigma2 = Label(self, text = "Point input sigma: ")
        self.l_data_sigma2.grid(row = 4, column = 2, sticky = W)
        self.t_data_sigma2 = Entry(self)
        self.t_data_sigma2.grid(row = 4, column = 3, sticky = W)              

    def create_hidden_layer_widgets(self):
        """Create text and checkboxes for hidden layer options"""
        
        self.hidden_title = Label(self, text = "*** Hidden unit options ***")
        self.hidden_title.grid(row = 7, column = 0, columnspan = 4, sticky = W)
        
        #number of hidden units
        self.l_hidden_units = Label(self, text = "# Hid Units: ")
        self.l_hidden_units.grid(row = 8, column = 0, columnspan = 1, sticky = W)
        self.t_hidden_units = Entry(self)
        self.t_hidden_units.grid(row = 8, column = 1, sticky = W)
        
        #whether pixelation is enforced (if empty, no pixelation enforcement)
        self.l_pixelation = Label(self, text = "Pixelation Sigma: ")
        self.l_pixelation.grid(row = 9, column = 0, columnspan = 1, sticky = W)
        self.t_pixelation = Entry(self)
        self.t_pixelation.grid(row = 9, column = 1, sticky = W)
        
        #number of training epochs
        self.l_epochs1 = Label(self, text = "Unlabelled epochs: ")
        self.l_epochs1.grid(row = 10, column = 0, sticky = W)
        self.t_epochs1 = Entry(self)
        self.t_epochs1.grid(row = 10, column = 1, sticky = W)
        
        self.l_epochs2 = Label(self, text = "Labelled epochs: ")
        self.l_epochs2.grid(row = 10, column = 2, sticky = W)
        self.t_epochs2 = Entry(self)
        self.t_epochs2.grid(row = 10, column = 3, sticky = W)        
    
    def create_macro_widgets(self):
        """Create text for macro parameter options"""
        
        self.macro_title = Label(self, text = "*** Macro parameters options ***")
        self.macro_title.grid(row = 11, column = 0, columnspan = 4, sticky = W)
        
        #Regularization constant...set as 0.01
        self.l_lambda1 = Label(self, text = "Unlabelled lambda: ")
        self.l_lambda1.grid(row = 12, column = 0, sticky = W)
        self.t_lambda1 = Entry(self)
        self.t_lambda1.grid(row = 12, column = 1, sticky = W)
        
        self.l_lambda2 = Label(self, text = "Labelled lambda: ")
        self.l_lambda2.grid(row = 12, column = 2, sticky = W)
        self.t_lambda2 = Entry(self)
        self.t_lambda2.grid(row = 12, column = 3, sticky = W)        
        
        #Learning rates...set as 0.1
        self.l_lr1 = Label(self, text = "Unlabelled LR: ")
        self.l_lr1.grid(row = 13, column = 0, sticky = W)
        self.t_lr1 = Entry(self)
        self.t_lr1.grid(row = 13, column = 1, sticky = W)
        
        #Learning rates...set as 0.1
        self.l_lr2 = Label(self, text = "Labelled LR: ")
        self.l_lr2.grid(row = 13, column = 2, sticky = W)
        self.t_lr2 = Entry(self)
        self.t_lr2.grid(row = 13, column = 3, sticky = W)        
     
        self.submit_button = Button(self, text = "Run", command = self.retvals)
        self.submit_button.grid(row = 14, column = 0, columnspan = 4, sticky = W)
    
    def retvals(self):
        """Set the appropriate variables"""
        
        #instantiate flags for unlabelled training set
        if self.single_points.get():
            self.unlabelled_inputs.append(0) #0 flag means single point data
            self.num_SPs = int(self.num_single_points.get())
        if self.mixed_points.get():
            self.unlabelled_inputs.append(1) #1 flag means 1pt + 2pt data
        if self.alphabet.get():
            self.unlabelled_inputs.append(2) #2 flag means alphabet
        if self.braille.get():
            self.unlabelled_inputs.append(3) #3 flag means braille
        
        #instantiate flags for labelled training set
        if self.mixed_points_labelled.get():
            self.labelled_inputs.append(1) #1 flag means 1pt + 2pt data
        if self.alphabet_labelled.get():
            self.labelled_inputs.append(2) #2 flag means alphabet
        if self.braille_labelled.get():
            self.labelled_inputs.append(3) #3 flag means braille        
        
        #instantiate other fields
        if self.t_data_sigma1.get() != "":
            self.unlabelled_sigma = float(self.t_data_sigma1.get())
        if self.t_data_sigma2.get() != "":
            self.labelled_sigma = float(self.t_data_sigma2.get())
        if self.t_hidden_units.get() != "":
            self.num_hidden_units = int(self.t_hidden_units.get())
        if self.t_pixelation.get() != "":
            self.pixelation_sigma = float(self.t_pixelation.get())
        if self.t_epochs1.get() != "":
            self.unlabelled_epochs = int(self.t_epochs1.get())
        if self.t_epochs2.get() != "":
            self.labelled_epochs = int(self.t_epochs2.get())        
        if self.t_lambda1.get() != "":
            self.unlabelled_lambda = float(self.t_lambda1.get())
        if self.t_lambda2.get() != "":
            self.labelled_lambda = float(self.t_lambda2.get())
        if self.t_lr1.get() != "":
            self.unlabelled_LR = float(self.t_lr1.get())
        if self.t_lr2.get() != "":
            self.labelled_LR = float(self.t_lr2.get())
        
        self.quit()
                   


        
