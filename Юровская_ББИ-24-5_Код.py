from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import *
import sqlite3
import os
from math import pi, sin, cos

class Samsung:
    def __init__(self, Number, Type, Seria, Model, Color, Memory, Year, Price, Rate):
        self.Number = Number
        self.Type = Type
        self.Seria = Seria
        self.Model = Model
        self.Color = Color
        self.Memory = Memory
        self.Year = Year
        self.Price = Price
        self.Rate = Rate
        self.t = (self.Number, self.Type, self.Seria, self.Model, self.Color, 
                 self.Memory, self.Year, self.Price, self.Rate)
    
    def __str__(self):
        return f"{self.Number} {self.Type} {self.Seria} {self.Model} {self.Color} " \
               f"{self.Memory} {self.Year} {self.Price} {self.Rate}"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Техника Samsung")
        self.root.geometry("1400x750")
        self.root.configure(background="pink")
        
        # Подключение к БД
        self.db_path = os.path.join(os.path.dirname(__file__), 'Юровская_ББИ-24-5_база данных.db')
        self.con = sqlite3.connect(self.db_path)
        self.cur = self.con.cursor()
        
        # Проверяем структуру таблицы
        self.check_table_structure()
        
        # Загрузка данных
        self.products_list = []
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблиц
        self.update_tree(self.tree)
        self.update_tree(self.tree_sorted)
    
    def check_table_structure(self):
        """Проверяем структуру таблицы и создаем если ее нет"""
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Samsung (
            number TEXT,
            type TEXT,
            seria TEXT,
            model TEXT,
            color TEXT,
            memory TEXT,
            year INTEGER,
            price INTEGER,
            rate INTEGER
        )
        """)
        self.con.commit()
    
    def load_data(self):
        self.cur.execute("SELECT * FROM Samsung")
        records = self.cur.fetchall()
        for row in records:
            self.products_list.append(Samsung(*row))
        print(f"Загружено {len(self.products_list)} записей")
    
    def create_widgets(self):
        # Основная таблица
        self.label_table1 = Label(self.root, text="Техника Samsung", 
                                font=("Arial", 12, "bold"), bg="green", fg="white")
        self.label_table1.place(x=10, y=0)
        
        columns = ("number", "type", "seria", "model", "color", "memory", "year", "price", "rate")
        display_columns = ("№", "Вид", "Серия", "Модель", "Цвет", "Память", "Год выпуска", "Цена (руб)", "Рейтинг")
        
        # Основная таблица (верхняя)
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        col_widths = [50, 100, 100, 150, 100, 100, 100, 100, 100]
        for col, display_col, width in zip(columns, display_columns, col_widths):
            self.tree.heading(col, text=display_col)
            self.tree.column(col, width=width, anchor="center")
        self.tree.place(x=10, y=30, width=1000, height=300)
        
        # Таблица для сортировки (нижняя)
        self.label_table2 = Label(self.root, text="Отсортированная техника", 
                                font=("Arial", 12, "bold"), bg="green", fg="white")
        self.label_table2.place(x=10, y=340)
        
        self.tree_sorted = ttk.Treeview(self.root, columns=columns, show="headings")
        for col, display_col, width in zip(columns, display_columns, col_widths):
            self.tree_sorted.heading(col, text=display_col)
            self.tree_sorted.column(col, width=width, anchor="center")
        self.tree_sorted.place(x=10, y=370, width=1000, height=300)
        
        # Элементы управления справа
        languages = ["По модели", "По цвету", "По памяти"]
        self.languages_listbox = Listbox(self.root, selectmode=SINGLE, 
                                       font=("Arial", 10), bg="lightgray")
        for lang in languages:
            self.languages_listbox.insert(END, lang)
        self.languages_listbox.place(x=1200, y=180, width=150, height=90)
        self.languages_listbox.bind("<<ListboxSelect>>", self.selected)
        
        btn_style = {"font": ("Arial", 10), "width": 15, "height": 1}
        Button(self.root, text="Добавить запись", command=self.add_record,
              bg="lightblue", **btn_style).place(x=1200, y=50)
        Button(self.root, text="Удалить запись", command=self.delete_record,
              bg="lightcoral", **btn_style).place(x=1200, y=100)
        Button(self.root, text="Обновить", command=self.refresh_data,
              bg="lightgreen", **btn_style).place(x=1200, y=150)
        Button(self.root, text="Показать график", command=self.show_graph,
              bg="lightyellow", **btn_style).place(x=1200, y=300)
    
    def update_tree(self, tree, data=None):
        tree.delete(*tree.get_children())
        data_to_show = [obj.t for obj in self.products_list] if data is None else data
        for item in data_to_show:
            tree.insert("", "end", values=item)
    
    def selected(self, event):
        if not self.languages_listbox.curselection():
            return
            
        selected_index = self.languages_listbox.curselection()[0]
        sort_options = [
            lambda x: x[3],  # По модели
            lambda x: x[4],  # По цвету
            lambda x: x[5]   # По памяти
        ]
        sorted_data = sorted([obj.t for obj in self.products_list], key=sort_options[selected_index])
        self.update_tree(self.tree_sorted, sorted_data)
    
    def refresh_data(self):
        self.products_list = []
        self.load_data()
        self.update_tree(self.tree)
        self.update_tree(self.tree_sorted)
        messagebox.showinfo("Обновлено", "Данные успешно обновлены")
    
    def add_record(self):
        add_window = Toplevel(self.root)
        add_window.title("Добавление записи")
        add_window.geometry("400x500")
        
        fields = [
            ("Номер:", "number"),
            ("Тип:", "type"),
            ("Серия:", "seria"),
            ("Модель:", "model"),
            ("Цвет:", "color"),
            ("Память:", "memory"),
            ("Год выпуска:", "year"),
            ("Цена:", "price"),
            ("Рейтинг:", "rate")
        ]
        
        self.entries = {}
        for i, (label, field) in enumerate(fields):
            Label(add_window, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = Entry(add_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry
        
        Button(add_window, text="Сохранить", command=self.save_record).grid(row=len(fields), column=0, pady=10)
        Button(add_window, text="Отмена", command=add_window.destroy).grid(row=len(fields), column=1, pady=10)
    
    def save_record(self):
        try:
            data = (
                self.entries["number"].get(),
                self.entries["type"].get(),
                self.entries["seria"].get(),
                self.entries["model"].get(),
                self.entries["color"].get(),
                self.entries["memory"].get(),
                int(self.entries["year"].get()),
                int(self.entries["price"].get()),
                int(self.entries["rate"].get())
            )
            
            self.cur.execute("INSERT INTO Samsung VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
            self.con.commit()
            self.refresh_data()
            messagebox.showinfo("Успех", "Запись успешно добавлена")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность ввода числовых значений!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    
    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите запись для удаления")
            return
            
        item_data = self.tree.item(selected_item)['values']
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту запись?"):
            try:
                self.cur.execute("""
                    DELETE FROM Samsung 
                    WHERE number=? AND type=? AND seria=? AND model=? 
                    AND color=? AND memory=? AND year=? AND price=? AND rate=?
                """, item_data)
                self.con.commit()
                self.refresh_data()
                messagebox.showinfo("Успех", "Запись успешно удалена")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {str(e)}")
    
    def show_graph(self):
        # Считаем количество техники по памяти
        memory_stats = {
            "32 ГБ": 0,
            "64 ГБ": 0,
            "128 ГБ": 0,
            "256 ГБ": 0,
            "512 ГБ": 0,
            "1 ТБ": 0
        }
        
        for product in self.products_list:
            if product.Memory in memory_stats:
                memory_stats[product.Memory] += 1
        
        # Создаем окно для графика
        graph_window = Toplevel(self.root)
        graph_window.title("Распределение техники по памяти")
        graph_window.geometry("500x700")
        
        # Создаем canvas для круговой диаграммы
        canvas = Canvas(graph_window, width=400, height=400, bg='white')
        canvas.pack(pady=20)
        
        # Цвета для секторов
        colors = ["green", "blue", "lightblue", "red", "orange", "pink"]
        
        # Параметры диаграммы
        center_x, center_y = 200, 200
        radius = 150
        total = sum(memory_stats.values())
        start_angle = 0
        
        # Рисуем сектора
        for i, (memory, count) in enumerate(memory_stats.items()):
            if count == 0:
                continue
                
            # Вычисляем угол сектора
            angle = 360 * count / total
            
            # Рисуем сектор
            canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=angle,
                fill=colors[i], outline='black'
            )
            
            # Добавляем подписи
            mid_angle = start_angle + angle/2
            label_x = center_x + (radius + 30) * cos(mid_angle * pi / 180)
            label_y = center_y + (radius + 30) * sin(mid_angle * pi / 180)
            canvas.create_text(label_x, label_y, text=f"{count}", font=("Arial", 10, "bold"))
            
            start_angle += angle
        
        # Добавляем легенду
        legend_frame = Frame(graph_window)
        legend_frame.pack(pady=10)
        
        for i, (memory, color) in enumerate(zip(memory_stats.keys(), colors)):
            Label(legend_frame, text=memory, fg=color, font=("Arial", 10)).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            Label(legend_frame, text=f"{memory_stats[memory]} шт.", font=("Arial", 10)).grid(row=i, column=1, sticky="e", padx=5)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
