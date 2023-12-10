from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import sys
from CustomModules import CustomGraphics
import csv
import os

class ContactManager(App):
    def __init__(self, **kwargs):
        super(ContactManager, self).__init__(**kwargs)
        self.contacts_file = 'contacts.csv'
        self.contacts = []
        self.load_contacts()

    def build(self):
        # UI components
        self.name_input = TextInput(hint_text='Name')
        self.name_input.size = (200,50)
        self.phone_input = TextInput(hint_text='Phone Number')
        self.email_input = TextInput(hint_text='Email')
        self.address_input = TextInput(hint_text='Address')

        self.add_button = Button(text='Add Contact')
        self.add_button.bind(on_press=self.add_contact)
        self.add_button.background_color = (0,0,0)

        self.view_button = Button(text='View Contacts')
        self.view_button.bind(on_press=self.view_contacts)
        self.view_button.background_color = (0,0,0)

        self.search_input = TextInput(hint_text='Search')
        self.search_button = Button(text='Search')
        self.search_button.bind(on_press=self.search_contacts)
        self.search_button.background_color = (0,0,0)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        label = Label(text='Contact Manager', font_size=24)
        label.color = "black"
        layout.add_widget(label)
        layout.add_widget(self.name_input)
        layout.add_widget(self.phone_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.address_input)
        CustomGraphics.SetBG(layout, bg_color=[0.4,0.5,0.5,1])

        layout2 = BoxLayout(orientation='horizontal', spacing=10, padding=10)
        layout2.add_widget(self.add_button)
        layout2.add_widget(self.view_button)
        
        layout.add_widget(layout2)
        
        layout3 = BoxLayout(orientation='horizontal', spacing=10, padding=10)
        layout3.add_widget(self.search_input)
        layout3.add_widget(self.search_button)
        layout.add_widget(layout3)

        return layout

    def add_contact(self, instance):
        name = self.name_input.text
        phone = self.phone_input.text
        email = self.email_input.text
        address = self.address_input.text

        if name and phone:
            contact = {'Name': name, 'Phone': phone, 'Email': email, 'Address': address}
            self.contacts.append(contact)
            self.save_contacts()
            self.show_popup(f"Contact '{name}' added successfully!")
            self.clear_inputs()
        else:
            self.show_popup("Name and Phone are required fields!")

    def view_contacts(self, instance):
        if self.contacts:
            contact_list = [f"{contact['Name']}: {contact['Phone']}" for contact in self.contacts]
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            for contact_str in contact_list:
                contact_label = Label(text=contact_str, font_size=18, halign='left', valign='top')
                delete_button = Button(text='Delete')
                delete_button.bind(on_press=lambda instance, contact=contact_str: self.delete_contact(contact))
                update_button = Button(text='Update')
                update_button.bind(on_press=lambda instance, contact=contact_str: self.update_contact_popup(contact))
                contact_layout = BoxLayout(orientation='horizontal', spacing=10)
                contact_layout.add_widget(contact_label)
                contact_layout.add_widget(delete_button)
                contact_layout.add_widget(update_button)
                content.add_widget(contact_layout)

            scroll_view = ScrollView()
            scroll_view.add_widget(content)

            popup = Popup(title='Contact List', content=scroll_view, size_hint=(None, None), size=(700, 800))
            popup.open()
        else:
            self.show_popup("No contacts available.")

    def search_contacts(self, instance):
        search_term = self.search_input.text.lower()
        search_results = [contact for contact in self.contacts if
                          search_term in contact['Name'].lower() or search_term in contact['Phone'].lower()]

        if search_results:
            contact_list = [f"{contact['Name']}: {contact['Phone']}" for contact in search_results]
            content = BoxLayout(orientation='vertical', spacing=10, padding=10)
            for contact_str in contact_list:
                contact_label = Label(text=contact_str, font_size=18, halign='left', valign='top')
                delete_button = Button(text='Delete')
                delete_button.bind(on_press=lambda instance, contact=contact_str: self.delete_contact(contact))
                update_button = Button(text='Update')
                update_button.bind(on_press=lambda instance, contact=contact_str: self.update_contact_popup(contact))
                contact_layout = BoxLayout(orientation='horizontal', spacing=10)
                contact_layout.add_widget(contact_label)
                contact_layout.add_widget(delete_button)
                contact_layout.add_widget(update_button)
                content.add_widget(contact_layout)

            scroll_view = ScrollView()
            scroll_view.add_widget(content)

            popup = Popup(title='Search Results', content=scroll_view, size_hint=(None, None), size=(700, 800))
            popup.open()
        else:
            self.show_popup("No matching contacts found.")

    def update_contact_popup(self, contact_str):
        name, _ = contact_str.split(":")
        for contact in self.contacts:
            if contact['Name'] == name:
                self.show_update_popup(contact)

    def show_update_popup(self, contact):
        update_popup = Popup(title='Update Contact', size_hint=(None, None), size=(700, 800))

        update_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        update_name_input = TextInput(hint_text='Name', text=contact['Name'])
        update_phone_input = TextInput(hint_text='Phone Number', text=contact['Phone'])
        update_email_input = TextInput(hint_text='Email', text=contact['Email'])
        update_address_input = TextInput(hint_text='Address', text=contact['Address'])

        update_button = Button(text='Update')
        update_button.bind(on_press=lambda instance: self.update_contact(contact,
                                                                        update_name_input.text,
                                                                        update_phone_input.text,
                                                                        update_email_input.text,
                                                                        update_address_input.text,
                                                                        update_popup))

        update_layout.add_widget(update_name_input)
        update_layout.add_widget(update_phone_input)
        update_layout.add_widget(update_email_input)
        update_layout.add_widget(update_address_input)
        update_layout.add_widget(update_button)

        update_popup.content = update_layout
        update_popup.open()

    def update_contact(self, contact, new_name, new_phone, new_email, new_address, update_popup):
        if new_name and new_phone:
            contact['Name'] = new_name
            contact['Phone'] = new_phone
            contact['Email'] = new_email
            contact['Address'] = new_address
            self.save_contacts()
            update_popup.dismiss()
            self.show_popup(f"Contact '{new_name}' updated successfully!")
        else:
            self.show_popup("Name and Phone are required fields!")

    def delete_contact(self, contact_str):
        name, _ = contact_str.split(":")
        for contact in self.contacts:
            if contact['Name'] == name:
                self.contacts.remove(contact)
                self.save_contacts()
                self.show_popup(f"Contact '{name}' deleted successfully!")
                return

    def show_popup(self, message):
        popup = Popup(title='Message', content=Label(text=message), size_hint=(None, None), size=(700, 800))
        popup.open()

    def clear_inputs(self):
        self.name_input.text = ''
        self.phone_input.text = ''
        self.email_input.text = ''
        self.address_input.text = ''

    def load_contacts(self):
        if os.path.exists(self.contacts_file):
            with open(self.contacts_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.contacts = list(reader)

    def save_contacts(self):
        with open(self.contacts_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['Name', 'Phone', 'Email', 'Address']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.contacts)


if __name__ == '__main__':
    ContactManager().run()
