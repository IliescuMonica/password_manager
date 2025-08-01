from tkinter import *
from tkinter import messagebox
from random import *
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project

def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_list_letters = [choice(letters) for _ in range(nr_letters)]
    password_list_symbols = [choice(symbols) for _ in range(nr_symbols) ]
    password_list_numbers = [choice(numbers) for _ in range(nr_numbers) ]

    password_list = password_list_letters + password_list_symbols + password_list_numbers

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:{
            "email": email,
            "password": password,
    }}


    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title = "Error", message = "Please make sure you haven't left any fields empty.")
    else:

        try:
            with open('data.json','r') as file:
                #reading old data
                data=json.load(file)
        except FileNotFoundError:
            with open('data.json', 'w') as file:
                json.dump(new_data, file, indent=4)
        else:
            # updating old data with new data
            data.update(new_data)
            with open('data.json','w') as file:
                # saving updated data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            website_entry.focus()
            email_entry.delete(0, END)
            email_entry.insert(0, "user@gmail.com")
            password_entry.delete(0, END)
            messagebox.showinfo(title="Success", message=f"Details for {website} saved successfully!")

# ---------------------------- SEARCH FOR INFO ------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data found.")
        return
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No details for {website} found.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(window,width=200,height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(row=0,column=1)

website_label = Label(window,text="Website:")
website_label.grid(row=1,column=0)

website_entry = Entry(window,width=34)
website_entry.grid(row=1,column=1,sticky="w")
website_entry.focus()

search_button = Button(window,width=14,text="Search",command=search)
search_button.grid(row=1,column=2)


email_label = Label(window,text="Email/Username:")
email_label.grid(row=2,column=0)

email_entry = Entry(window,width=52)
email_entry.insert(0,"user@gmail.com")
email_entry.grid(row=2,column=1,columnspan=2,sticky="w")

password_label = Label(window,text="Password:")
password_label.grid(row=3,column=0)

password_entry = Entry(window,width=34)
password_entry.grid(row=3,column=1,sticky="w")

generate_button = Button(text="Generate Password",command=generate_password)
generate_button.grid(row=3,column=2)

add_button = Button(text="Add",width=44,command = save)
add_button.grid(row=4,column=1,columnspan=2)


window.mainloop()