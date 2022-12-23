import sqlite3

class Database:
    """Обертка для работы с БД"""

    def __init__(self):#self- ссылка на сам объект этого класса, init - инициализация экземпляров класса после их создания
        """Инициализация базы данных"""
        self.conn = sqlite3.connect('db/project.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.check_if_table_exists()
    
    def check_if_table_exists(self):
        ''' Проверяем, есть ли таблица reviews в базе данных. Если нет, то создаем ее. '''
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="reviews"')
        if self.cursor.fetchone() is None:
            self.cursor.execute('CREATE TABLE reviews (id_review INTEGER, review TEXT)')
            self.conn.commit()

    def add_review(self, message):
        ''' Добавляем отзыв в базу данных '''
        self.cursor.execute('INSERT INTO reviews (id_review, review) VALUES (?, ?)',
                   (message.from_user.id, message.text))
        self.conn.commit()

    def get_reviews(self):
        ''' Получаем все отзывы из базы данных'''
        self.cursor.execute('SELECT review FROM reviews')
        reviews = [x[0] for x in self.cursor.fetchall()]
        return reviews
