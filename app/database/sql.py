import sqlite3


class DB:

    def __init__(self, db_file):
        """Инициализирует соединение с БД."""
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяет, есть ли user в БД."""
        query = self.cur.execute('SELECT id FROM users WHERE user_id = ?', (user_id,))
        return bool(len(query.fetchall()))

    def get_user_id(self, user_id):
        """Получаем id пользователя в базе по его user_id."""
        query = self.cur.execute('SELECT id FORM users WHERE user_id = ?', (user_id,))
        return query.fetchall()[0]

    def add_user(self, user_id):
        """Добавляем пользователя в БД."""
        self.cur.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
        return self.conn.commit()

    def add_record(self, user_id, operation, value):
        """Добавляет новую запись о доходе/расходе в БД."""
        self.cur.execute('INSERT INTO records (user_id, operation, value) VALUES (?, ?, ?)', (
            self.get_user_id(user_id),
            operation == '+',
            value
        ))
        return self.conn.commit()

    def get_records(self, user_id, within='*'):
        """Получаем историю операций за определенный период."""
        if within == 'day':
            # За последний день.
            result = self.cur.execute(
                'SELECT * FROM records WHERE user_id = ? AND date BETWEEN datetime("now", "start of day") AND datetime("now", "localtime") ORDER BY date',
                (self.get_user_id(user_id),)
            )
        elif within == 'month':
            # За последний месяц.
            result = self.cur.execute(
                'SELECT * FROM records WHERE user_id = ? AND date BETWEEN datetime("now", "-6 days") AND datetime("now", "localtime") ORDER BY date',
                (self.get_user_id(user_id),)
            )
        elif within == 'year':
            # За последний год.
            result = self.cur.execute(
                'SELECT * FROM records WHERE user_id = ? AND date BETWEEN datetime("now", "start of month") AND datetime("now", "localtime") ORDER BY date',
                (self.get_user_id(user_id),)
            )
        else:
            # За все время.
            result = self.cur.execute(
                'SELECT * FROM records WHERE user_id = ? ORDER BY date',
                (self.get_user_id(user_id),)
            )

        return result.fetchall()

    def close(self):
        """Закрытия соединения с БД."""
        self.conn.close()
