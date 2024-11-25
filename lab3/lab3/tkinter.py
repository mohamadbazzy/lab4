import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog, simpledialog
import sqlite3
import csv
from tkinter import Toplevel, Label, Button

class DatabaseApp(tk.Tk):
    """
    A class representing the School Management System application, 
    built using Tkinter and SQLite3 for database handling.

    Attributes
    ----------
    tabs : ttk.Notebook
        Tabbed interface for managing students, instructors, courses, and registration.
    db_connection : sqlite3.Connection
        The SQLite connection object.
    cursor : sqlite3.Cursor
        The SQLite cursor object.
    """
    def __init__(self):
        """
        Initializes the main window of the School Management System.
        Sets up the UI tabs and database connection.
        """
        super().__init__()
        self.title('School Management System')
        self.geometry('600x400')
        self.db_connection = None
        self.cursor = None
        self.initialize_database()
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=1, fill='both')
    
        self.add_student_tab = ttk.Frame(self.tabs)
        self.add_instructor_tab = ttk.Frame(self.tabs)
        self.add_course_tab = ttk.Frame(self.tabs)
        self.register_course_tab = ttk.Frame(self.tabs)
        self.view_all_tab = ttk.Frame(self.tabs)
        
        self.tabs.add(self.add_student_tab, text='Add stdnt')
        self.tabs.add(self.add_instructor_tab, text='Add instrctr')
        self.tabs.add(self.add_course_tab, text='Add Course')
        self.tabs.add(self.register_course_tab, text='Register for Course')
        self.tabs.add(self.view_all_tab, text='View All')

        self.create_add_student_widgets()
        self.create_add_instructor_widgets()
        self.create_add_course_widgets()
        self.create_register_course_widgets()
        self.create_view_all_widgets()

    def get_db_connection(self):
        """
        Gets or creates a database connection.

        Returns
        -------
        sqlite3.Connection
            The connection object to the SQLite database.
        """
        if not self.db_connection:
            self.db_connection = sqlite3.connect('school.db')
            self.cursor = self.db_connection.cursor()
        return self.db_connection

    def initialize_database(self):
        """
        Initializes the database with the necessary tables if they do not already exist.
        Creates tables for students, instructors, courses, and registrations.
        """
        conn = self.get_db_connection()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL,
                student_id TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS instructors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT NOT NULL,
                instructor_id TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                course_id TEXT NOT NULL,
                instructor_id TEXT NOT NULL,
                FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                course_id TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES students(student_id),
                FOREIGN KEY(course_id) REFERENCES courses(course_id)
            )
        """)
        conn.commit()

    def create_add_student_widgets(self):
        """
        Creates and packs the widgets for the 'Add Student' tab, 
        including input fields for name, age, email, and student ID.
        """
        tk.Label(self.add_student_tab, text="Name:").pack()
        self.student_name = tk.Entry(self.add_student_tab)
        self.student_name.pack()

        tk.Label(self.add_student_tab, text="Age:").pack()
        self.student_age = tk.Entry(self.add_student_tab)
        self.student_age.pack()

        tk.Label(self.add_student_tab, text="Email:").pack()
        self.student_email = tk.Entry(self.add_student_tab)
        self.student_email.pack()

        tk.Label(self.add_student_tab, text="Student ID:").pack()
        self.student_id = tk.Entry(self.add_student_tab)
        self.student_id.pack()

        tk.Button(self.add_student_tab, text='Add Student', command=self.add_student).pack()

    def create_add_instructor_widgets(self):
        """
        Creates and packs the widgets for the 'Add Instructor' tab, 
        including input fields for name, age, email, and instructor ID.
        """
        tk.Label(self.add_instructor_tab, text='Name:').pack()
        self.instructor_name = tk.Entry(self.add_instructor_tab)
        self.instructor_name.pack()

        tk.Label(self.add_instructor_tab, text='Age:').pack()
        self.instructor_age = tk.Entry(self.add_instructor_tab)
        self.instructor_age.pack()

        tk.Label(self.add_instructor_tab, text='Email:').pack()
        self.instructor_email = tk.Entry(self.add_instructor_tab)
        self.instructor_email.pack()

        tk.Label(self.add_instructor_tab, text='Instructor ID:').pack()
        self.instructor_id = tk.Entry(self.add_instructor_tab)
        self.instructor_id.pack()

        tk.Button(self.add_instructor_tab, text='Add Instructor', command=self.add_instructor).pack()

    def create_add_course_widgets(self):
        """
        Creates and packs the widgets for the 'Add Course' tab, 
        including input fields for course ID, course name, and instructor ID.
        """
        tk.Label(self.add_course_tab, text='Course ID:').pack()
        self.course_id = tk.Entry(self.add_course_tab)
        self.course_id.pack()

        tk.Label(self.add_course_tab, text='Course Name:').pack()
        self.course_name = tk.Entry(self.add_course_tab)
        self.course_name.pack()

        tk.Label(self.add_course_tab, text='Instructor ID:').pack()
        self.instructor_id_course = tk.Entry(self.add_course_tab)
        self.instructor_id_course.pack()

        tk.Button(self.add_course_tab, text='Add Course', command=self.add_course).pack()

    def create_register_course_widgets(self):
        """
        Creates and packs the widgets for the 'Register for Course' tab, 
        including dropdowns for selecting a student and a course.
        """
        tk.Label(self.register_course_tab, text='Select Student:').pack()
        self.student_dropdown = ttk.Combobox(self.register_course_tab)
        self.student_dropdown.pack()

        tk.Label(self.register_course_tab, text='Select Course:').pack()
        self.course_dropdown = ttk.Combobox(self.register_course_tab)
        self.course_dropdown.pack()

        tk.Button(self.register_course_tab, text='Register', command=self.register_course).pack()
        self.refresh_dropdowns()

    def create_view_all_widgets(self):
        """
        Creates and packs the widgets for the 'View All' tab, 
        including a table to display all students, instructors, and courses.
        """
        self.view_all_table = ttk.Treeview(self.view_all_tab, columns=('ID', 'Name', 'Type'), show='headings')
        self.view_all_table.heading('ID', text='ID')
        self.view_all_table.heading('Name', text='Name')
        self.view_all_table.heading('Type', text='Type')
        self.view_all_table.pack(expand=1, fill='both')

        # Bind double-click event to the edit function
        self.view_all_table.bind('<Double-1>', self.edit)

        tk.Button(self.view_all_tab, text='Refresh', command=self.refresh_view_all).pack()
        tk.Button(self.view_all_tab, text='Export to CSV', command=self.export_to_csv).pack()
        tk.Button(self.view_all_tab, text='Load', command=self.load).pack()
        self.search_entry = tk.Entry(self.view_all_tab)
        self.search_entry.pack(pady=5)
        tk.Button(self.view_all_tab, text='Search', command=self.search).pack()
        tk.Button(self.view_all_tab, text='Delete', command=self.delete).pack(pady=5)

    def refresh_dropdowns(self):
        """
        Refreshes the student and course dropdown lists in the 'Register for Course' tab.
        """
        conn = self.get_db_connection()
        self.cursor.execute('SELECT name FROM students')
        students = [row[0] for row in self.cursor.fetchall()]
        self.student_dropdown['values'] = students

        self.cursor.execute('SELECT course_name FROM courses')
        courses = [row[0] for row in self.cursor.fetchall()]
        self.course_dropdown['values'] = courses

    def add_student(self):
        """
        Adds a new student to the database.

        Retrieves the student's name, age, email, and student ID from the input fields,
        inserts them into the `students` table, and refreshes the dropdowns. Displays
        a success popup upon completion or an error message if the insertion fails.

        Raises:
            Exception: If there's an error while adding the student to the database.
        """
        name=self.student_name.get()
        age=int(self.student_age.get())
        email=self.student_email.get()
        student_id=self.student_id.get()
        try:
            conn=self.get_db_connection()
            self.cursor.execute("""
                INSERT INTO students (name, age, email,student_id) 
                VALUES (?, ?, ?, ?)
            """, (name, age,email, student_id))
            conn.commit()
            self.refresh_dropdowns()
            custom_popup = Toplevel()
            custom_popup.title("Success")
            
            # Create a label with the centered message
            message = Label(custom_popup, text="Success! Student added successfully", font=('Arial', 12), padx=50, pady=20)
            message.pack()

            # Add a button to close the popup
            close_button = Button(custom_popup, text="OK", command=custom_popup.destroy)
            close_button.pack(pady=10)
            self.clear_student_inputs()
        except Exception as e:
            messagebox.showinfo('Error adding student', e)
    
    def add_instructor(self):
        """
        Adds a new instructor to the database.

        Retrieves the instructor's name, age, email, and instructor ID from the input fields,
        inserts them into the `instructors` table, and refreshes the dropdowns. Displays
        a success popup upon completion or an error message if the insertion fails.

        Raises:
            Exception: If there's an error while adding the instructor to the database.
        """
        name=self.instructor_name.get()
        age=int(self.instructor_age.get())
        email=self.instructor_email.get()
        instructor_id=self.instructor_id.get()
        try:
            conn=self.get_db_connection()
            self.cursor.execute("""
                INSERT INTO instructors (name, age, email,instructor_id) 
                VALUES (?, ?, ?, ?)
            """, (name, age,email, instructor_id))
            conn.commit()
            self.refresh_dropdowns()
            custom_popup = Toplevel()
            custom_popup.title("Success")
            
            # Create a label with the centered message
            message = Label(custom_popup, text="Success! Instructor added successfully", font=('Arial', 12), padx=50, pady=20)
            message.pack()

            # Add a button to close the popup
            close_button = Button(custom_popup, text="OK", command=custom_popup.destroy)
            close_button.pack(pady=10)
            self.clear_instructor_inputs()
        except Exception as e:
            messagebox.showinfo('Error adding instructor', e)

    def add_course(self):
        """
        Adds a new course to the database.

        Retrieves the course ID, course name, and instructor ID from the input fields,
        inserts them into the `courses` table, and refreshes the dropdowns. Displays
        a success popup upon completion or an error message if the insertion fails.

        Raises:
            Exception: If there's an error while adding the course to the database.
        """
        course_id=self.course_id.get()
        course_name=self.course_name.get()
        instructor_id=self.instructor_id_course.get()
        try:
            conn=self.get_db_connection()
            self.cursor.execute("""
                INSERT INTO courses (course_id,course_name, instructor_id) 
                VALUES (?, ?, ?)
            """, (course_id,course_name,instructor_id))
            conn.commit()
            self.refresh_dropdowns()
            custom_popup = Toplevel()
            custom_popup.title("Success")
            
            # Create a label with the centered message
            message = Label(custom_popup, text="Success! Course added successfully", font=('Arial', 12), padx=50, pady=20)
            message.pack()

            # Add a button to close the popup
            close_button = Button(custom_popup, text="OK", command=custom_popup.destroy)
            close_button.pack(pady=10)
            self.clear_course_inputs()
        except Exception as e:
            messagebox.showinfo('Error adding course', e)
    
    def register_course(self):
        """
        Registers a student for a course.

        Retrieves the selected student and course, fetches the corresponding student ID
        and course ID from the database, and inserts the registration into the `registrations`
        table. Displays a success popup upon completion or an error message if the registration fails.

        Raises:
            Exception: If there's an error while registering the course in the database.
        """
        student_name=self.student_dropdown.get()
        course_name=self.course_dropdown.get()
        try:
            conn=self.get_db_connection()
            self.cursor.execute("SELECT student_id FROM students WHERE name=?" ,(student_name,))
            student_id= self.cursor.fetchone()[0]
            self.cursor.execute("SELECT course_id FROM courses WHERE course_name=?" ,(course_name,))
            course_id= self.cursor.fetchone()[0]
            self.cursor.execute("""
                INSERT INTO registrations (student_id, course_id)
                VALUES(?,?)
            """, (student_id, course_id))
            conn.commit()
            custom_popup = Toplevel()
            custom_popup.title("Success")
            
            # Create a label with the centered message
            message = Label(custom_popup, text="Success! Course registered successfully", font=('Arial', 12), padx=50, pady=20)
            message.pack()

            # Add a button to close the popup
            close_button = Button(custom_popup, text="OK", command=custom_popup.destroy)
            close_button.pack(pady=10)
        except Exception as e:
            messagebox.showinfo('Error registering course', e)
    
    def refresh_view_all(self):
        """
        Refreshes the displayed list of students, instructors, and courses.

        Clears the current view, fetches all records from the `students`, `instructors`, and
        `courses` tables, and inserts them into the table view. Displays a success popup upon completion
        or an error message if the operation fails.

        Raises:
            Exception: If there's an error while refreshing the data from the database.
        """
        self.view_all_table.delete(*self.view_all_table.get_children())
        try:
            conn= self.get_db_connection()
            self.cursor.execute('SELECT student_id, name FROM students')
            students= self.cursor.fetchall()
            self.cursor.execute('SELECT instructor_id, name FROM instructors')
            instructors= self.cursor.fetchall()
            self.cursor.execute("SELECT course_id, course_name FROM courses")
            courses= self.cursor.fetchall()

            for record in students:
                self.view_all_table.insert("","end", values=(*record,"Student"))

            for record in instructors:
                self.view_all_table.insert("","end", values=(*record,"Instructor"))
            
            for record in courses:
                self.view_all_table.insert("","end", values=(*record,"Course"))
            custom_popup = Toplevel()
            custom_popup.title("Success")
            
            # Create a label with the centered message
            message = Label(custom_popup, text="Success! Data refreshed successfully", font=('Arial', 12), padx=50, pady=20)
            message.pack()

            # Add a button to close the popup
            close_button = Button(custom_popup, text="OK", command=custom_popup.destroy)
            close_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror('Error refreshing data', e)
    
    def export_to_csv(self):
        """
        Exports the currently displayed data to a CSV file.

        Opens a file dialog to choose the location to save the CSV file, writes the contents
        of the table to the file, and displays a success popup. If the export fails, an error
        message is displayed.

        Raises:
            Exception: If there's an error while exporting the data to the CSV file.
        """
        try:
            filename= filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV Files","*.csv")])
            if filename:
                with open(filename,'w', newline='') as file:
                    writer=csv.writer(file)
                    writer.writerow(["ID","Name","Type"])
                    for row in self.view_all_table.get_children():
                        row_data= self.view_all_table.item(row,'values')
                        writer.writerow(row_data)
                custom_popup = Toplevel()
            custom_popup.title("Success")
            
            # Create a label with the centered message
            message = Label(custom_popup, text="Success! Course added successfully", font=('Arial', 12), padx=50, pady=20)
            message.pack()

            # Add a button to close the popup
            close_button = Button(custom_popup, text="OK", command=custom_popup.destroy)
            close_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error exporting data", e)

    def load(self):
        """
        Loads data from a CSV file into the application.

        Opens a file dialog to select a CSV file, reads the file, and populates the table view
        with the data from the file. Displays a success popup upon completion or an error message
        if the operation fails.

        Raises:
            Exception: If there's an error while loading data from the CSV file.
        """
        try:
            # Open a file dialog to select the CSV file
            filename = filedialog.askopenfilename(defaultextension='.csv', filetypes=[("CSV Files", "*.csv")])
            if filename:
                # Clear existing data in the table
                for item in self.view_all_table.get_children():
                    self.view_all_table.delete(item)
                
                with open(filename, 'r') as file:
                    reader = csv.reader(file)
                    header = next(reader)  # Skip the header row
                    
                    for row in reader:
                        if len(row) == 3:  # Ensure that each row has 3 columns
                            self.view_all_table.insert("", "end", values=row)
                
                # Show success popup
                custom_popup = Toplevel()
                custom_popup.title("Success")
                
                # Create a label with the centered message
                message = Label(custom_popup, text="Data loaded successfully", font=('Arial', 12), padx=50, pady=20)
                message.pack()
                
                # Add a button to close the popup
                close_button = Button(custom_popup, text="OK", command=custom_popup.destroy)
                close_button.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error loading data", e)
    
    def search(self):
        """
        Searches for students, instructors, or courses by name or course name.

        Retrieves the search term from the input field, searches in the `students`, `instructors`,
        and `courses` tables for matches, and displays the results in the table view. If the search
        fails, an error message is displayed.

        Raises:
            Exception: If there's an error while searching the database.
        """
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return
        
        # Clear existing data in the table
        for item in self.view_all_table.get_children():
            self.view_all_table.delete(item)

        conn = self.get_db_connection()
        
        try:
            # Search in students table
            self.cursor.execute("SELECT student_id, name, 'Student' FROM students WHERE name LIKE ?", (f"%{search_term}%",))
            students = self.cursor.fetchall()
            
            # Search in instructors table
            self.cursor.execute("SELECT instructor_id, name, 'Instructor' FROM instructors WHERE name LIKE ?", (f"%{search_term}%",))
            instructors = self.cursor.fetchall()
            
            # Search in courses table
            self.cursor.execute("SELECT course_id, course_name, 'Course' FROM courses WHERE course_name LIKE ?", (f"%{search_term}%",))
            courses = self.cursor.fetchall()
            
            # Insert results into the table
            for record in students + instructors + courses:
                self.view_all_table.insert("", "end", values=record)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def edit(self,event):
        """
        Allows editing a selected record in the table view.

        Retrieves the selected record, shows an input dialog to enter the new value, and updates
        the record both in the database and the table view. If the update fails, an error message
        is displayed.

        Args:
            event (Event): The event triggered by selecting a record in the table.

        Raises:
            Exception: If there's an error while editing the record.
        """
        item = self.view_all_table.selection()
        if not item:
            return
        
        column = self.view_all_table.identify_column(event.x)
        column_id = column.split('#')[1]
        column_index = int(column_id) - 1
        
        # Get the current value of the cell
        current_value = self.view_all_table.item(item[0], 'values')[column_index]
        
        # Show an input dialog to get the new value
        new_value = simpledialog.askstring("Edit Value", f"Edit value for '{self.view_all_table.heading(column_id, 'text')}'", initialvalue=current_value)
        
        if new_value is not None:
            self.update_record(item[0], column_index, new_value)
    
    def update_record(self, item_id, column_index, new_value):
        """
        Updates a record in the database and table view.

        Identifies the table (students, instructors, or courses) based on the type of record,
        updates the corresponding record in the database, and reflects the change in the table view.
        Displays an error message if the update fails.

        Args:
            item_id (str): The ID of the item to be updated.
            column_index (int): The index of the column to be updated.
            new_value (str): The new value to be set.

        Raises:
            Exception: If there's an error while updating the record.
        """
        values = self.view_all_table.item(item_id, 'values')
        id_value, name_value, type_value = values
        
        # Determine which table to update
        if type_value == "Student":
            table = "students"
            id_field = "student_id"
            name_field = "name"
        elif type_value == "Instructor":
            table = "instructors"
            id_field = "instructor_id"
            name_field = "name"
        elif type_value == "Course":
            table = "courses"
            id_field = "course_id"
            name_field = "course_name"
        else:
            messagebox.showerror("Error", "Unknown type")
            return
        
        # Update the database
        conn = self.get_db_connection()
        try:
            self.cursor.execute(f"UPDATE {table} SET {name_field} = ? WHERE {id_field} = ?", (new_value, id_value))
            conn.commit()
            
            # Update the Treeview
            updated_values = list(values)
            updated_values[column_index] = new_value
            self.view_all_table.item(item_id, values=updated_values)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()
    
    def delete(self):
        """
        Deletes a selected record from the database and table view.

        Confirms the deletion with the user, identifies the type of record (student, instructor, or course),
        deletes it from the corresponding table in the database, and removes it from the table view.
        Displays an error message if the deletion fails.

        Raises:
            Exception: If there's an error while deleting the record from the database.
        """
        selected_item = self.view_all_table.selection()
    
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return
        
        item_id = selected_item[0]
        item_values = self.view_all_table.item(item_id, 'values')
        id_value, name_value, type_value = item_values
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the {type_value} '{name_value}'?")
        if not confirm:
            return
        
        # Determine which table to delete from
        if type_value == "Student":
            table = "students"
            id_field = "student_id"
        elif type_value == "Instructor":
            table = "instructors"
            id_field = "instructor_id"
        elif type_value == "Course":
            table = "courses"
            id_field = "course_id"
        else:
            messagebox.showerror("Error", "Unknown type")
            return
        
        # Delete from the database
        conn = self.get_db_connection()
        try:
            self.cursor.execute(f"DELETE FROM {table} WHERE {id_field} = ?", (id_value,))
            conn.commit()
            
            # Remove from the Treeview
            self.view_all_table.delete(item_id)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def clear_instructor_inputs(self):
        """
        Clears the input fields for adding a new instructor.
        """
        self.instructor_name.delete(0, tk.END)
        self.instructor_email.delete(0, tk.END)
        self.instructor_age.delete(0, tk.END)
        self.instructor_id.delete(0, tk.END)
    
    def clear_student_inputs(self):
        """
        Clears the input fields for adding a new student.
        """
        self.student_name.delete(0, tk.END)
        self.student_email.delete(0, tk.END)
        self.student_age.delete(0, tk.END)
        self.student_id.delete(0, tk.END)

    def clear_course_inputs(self):
        """
        Clears the input fields for adding a new course.
        """
        self.course_id.delete(0, tk.END)
        self.course_name.delete(0, tk.END)
        self.instructor_id_course.delete(0, tk.END)

if __name__=="__main__":
    app=DatabaseApp()
    app.mainloop()



        

    






        



