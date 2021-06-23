import tkinter
from tkinter import scrolledtext
from tkinter import INSERT
import segment
from fuzzywuzzy import fuzz
root = tkinter.Tk()
root.title("Text Segmentation")
root.geometry("800x700")
is_on = False

#calculates the match between two sentences
def match_calculate():
    if is_on:
        match1 = fuzz.ratio(result_unigram_textbox.get("1.0","end-1c").lower(), compare_textbox.get("1.0","end-1c").lower())
        match2 = fuzz.ratio(result_bigram_textbox.get("1.0","end-1c").lower(), compare_textbox.get("1.0","end-1c").lower())
        matched_unigram_label.config(text = "Matched Percent: "+f"{match1:.2f}")
        match_bigram_label.config(text = "Matched Percent: "+f"{match2:.2f}")
    else:
        matched_unigram_label.config(text = "Matched Percent: 0")
        match_bigram_label.config(text = "Matched Percent: 0")

#Called wen user press Run        
def retrieve_input():
    inputValue = textbox.get("1.0","end-1c")
    unigram_result, bigram_result, time1, time2 = segment.start_segmentation(inputValue)
    result_unigram_textbox.config(state="normal")
    result_unigram_textbox.delete('1.0', "end")
    result_unigram_textbox.insert("end", unigram_result)
    result_unigram_textbox.config(state="disabled")
    time_unigram_label.config(text = "Time: "+f"{time1:.5f}")
    
    result_bigram_textbox.config(state="normal")
    result_bigram_textbox.delete('1.0', "end")
    result_bigram_textbox.insert("end", bigram_result)
    result_bigram_textbox.config(state="disabled")
    time_bigram_label.config(text = "Time: "+f"{time2:.5f}")
    match_calculate()
    

#disable maximize&minimize button
root.resizable(0,0)

#adding the main canves
main_canvas = tkinter.Canvas(root, width = 800, height = 700)
main_canvas.pack()

#adding get result button
get_result_button = tkinter.Button( main_canvas, text = "Run", bg = 'white', width = 15, height = 1, font = 'sans 18 bold', activeforeground = "gray25", command=retrieve_input)
get_result_button.place(x = 400,y = 650, anchor = tkinter.CENTER)



#adding text to segment text box
text_label = tkinter.Label(root, 
                text = "Enter text to segment ", 
                font = ("Times New Roman", 18), 
                foreground = "black")
text_label.place(x = 200, y = 25, anchor = "center")
textbox = tkinter.scrolledtext.ScrolledText (root)
textbox.place(width = 300, height = 200, x = 200, y = 150, anchor = "center")

#adding text to be compared 
compare_text_label = tkinter.Label(root, 
                text = "Enter text to compare with ", 
                font = ("Times New Roman", 18), 
                foreground = "black")
compare_text_label.place(x = 600, y = 25, anchor = "center")
compare_textbox = tkinter.scrolledtext.ScrolledText (root)
compare_textbox.place(width = 300, height = 200, x = 600, y = 150, anchor = "center")


#adding unigram result text box
result_unigram_label = tkinter.Label(root, 
                text = "Using unigrams ", 
                font = ("Times New Roman", 18), 
                foreground = "black")
time_unigram_label = tkinter.Label(root, 
                text = "Time: 0", 
                font = ("Times New Roman", 18), 
                foreground = "black")
matched_unigram_label = tkinter.Label(root, 
                text = "Matched Percent: 0", 
                font = ("Times New Roman", 18), 
                foreground = "black")
result_unigram_label.place(x = 200, y = 275, anchor = "center")
time_unigram_label.place(x = 200, y = 520, anchor = "center")
matched_unigram_label.place(x = 200, y = 560, anchor = "center")
result_unigram_textbox = tkinter.scrolledtext.ScrolledText (root )
result_unigram_textbox.pack()
result_unigram_textbox.place(width = 300, height = 200, x = 200, y = 400, anchor = "center")
result_unigram_textbox.config(state="disabled")

#adding bigram result text box
result_bigram_label = tkinter.Label(root, 
                text = "Using bigrams ", 
                font = ("Times New Roman", 18), 
                foreground = "black")
time_bigram_label = tkinter.Label(root, 
                text = "Time: 0", 
                font = ("Times New Roman", 18), 
                foreground = "black")
match_bigram_label = tkinter.Label(root, 
                text = "Matched Percent: 0", 
                font = ("Times New Roman", 18), 
                foreground = "black")
result_bigram_label.place(x = 600, y = 275, anchor = "center")
time_bigram_label.place(x = 600, y = 520, anchor = "center")
match_bigram_label.place(x = 600, y = 560, anchor = "center")
result_bigram_textbox = tkinter.scrolledtext.ScrolledText (root)
result_bigram_textbox.place(width = 300, height = 200, x = 600, y = 400, anchor = "center")
result_bigram_textbox.config(state="disabled")

# Sqitch the match Button
def switch():
    global is_on
      
    # Determin is on or off
    if is_on:
        on_button.config(image = off)
        is_on = False
    else:
        
        on_button.config(image = on)
        is_on = True
  
# Define Our Images for match Button
on = tkinter.PhotoImage(file = "on.png")
off = tkinter.PhotoImage(file = "off.png")
  
# Create A Button for match 
on_button = tkinter.Button(root, image = off, bd = 0,
                   command = switch)
on_button.place(x = 770, y = 30, anchor = "center")

                   


root.mainloop()