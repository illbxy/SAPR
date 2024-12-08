import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow

if __name__ == "__main__":
    try:
        # Создаем объект приложения
        app = QApplication(sys.argv)

        # Создаем главное окно
        window = MainWindow()

        # Показываем главное окно
        window.show()

        # Запускаем главный цикл приложения
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
