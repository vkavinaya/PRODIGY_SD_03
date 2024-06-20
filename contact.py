import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Define the file path for storing contacts
CONTACTS_FILE = 'contacts.json'

def load_contacts():
    """Load contacts from the file."""
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_contacts(contacts):
    """Save contacts to the file."""
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

class ContactManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Contact Manager")
        self.geometry("600x400")

        self.contacts = load_contacts()
        self.create_widgets()
        self.populate_contacts()

    def create_widgets(self):
        """Create the GUI widgets."""
        self.contact_listbox = tk.Listbox(self, height=15, width=70)
        self.contact_listbox.pack(pady=20, padx=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        self.add_button = tk.Button(button_frame, text="Add Contact", width=15, command=self.add_contact)
        self.add_button.grid(row=0, column=0, padx=10)

        self.edit_button = tk.Button(button_frame, text="Edit Contact", width=15, command=self.edit_contact)
        self.edit_button.grid(row=0, column=1, padx=10)

        self.delete_button = tk.Button(button_frame, text="Delete Contact", width=15, command=self.delete_contact)
        self.delete_button.grid(row=0, column=2, padx=10)

    def populate_contacts(self):
        """Populate the listbox with contacts."""
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_listbox.insert(tk.END, f"Name: {contact['name']} | Phone: {contact['phone']}")

    def add_contact(self):
        """Add a new contact."""
        dialog = tk.Toplevel(self)
        dialog.title("Add Contact")

        tk.Label(dialog, text="Name:").pack()
        name_entry = tk.Entry(dialog)
        name_entry.pack()

        tk.Label(dialog, text="Phone number:").pack()
        phone_entry = tk.Entry(dialog)
        phone_entry.pack()

        def save_contact():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()

            if name and phone:
                self.contacts.append({"name": name, "phone": phone})
                save_contacts(self.contacts)
                self.populate_contacts()
                dialog.destroy()
            else:
                messagebox.showwarning("Input Error", "All fields are required!")

        tk.Button(dialog, text="Save", command=save_contact).pack()

    def edit_contact(self):
        """Edit an existing contact."""
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            contact = self.contacts[index]

            dialog = tk.Toplevel(self)
            dialog.title("Edit Contact")

            tk.Label(dialog, text="Name:").pack()
            name_entry = tk.Entry(dialog)
            name_entry.insert(tk.END, contact['name'])
            name_entry.pack()

            tk.Label(dialog, text="Phone number:").pack()
            phone_entry = tk.Entry(dialog)
            phone_entry.insert(tk.END, contact['phone'])
            phone_entry.pack()

            def save_contact():
                name = name_entry.get().strip()
                phone = phone_entry.get().strip()

                if name and phone:
                    self.contacts[index] = {"name": name, "phone": phone}
                    save_contacts(self.contacts)
                    self.populate_contacts()
                    dialog.destroy()
                else:
                    messagebox.showwarning("Input Error", "All fields are required!")

            tk.Button(dialog, text="Save", command=save_contact).pack()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to edit.")

    def delete_contact(self):
        """Delete a contact."""
        selected_index = self.contact_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.contacts.pop(index)
            save_contacts(self.contacts)
            self.populate_contacts()
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

if __name__ == "__main__":
    app = ContactManager()
    app.mainloop()
