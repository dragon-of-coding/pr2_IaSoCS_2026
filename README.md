# Book Catalog

Учебное консольное приложение на Python для работы с каталогом книг.

## Запуск

Для вывода книг:

```bash
python books.py list
```

Рабочие данные хранятся в файле `books.json`.

Пример структуры данных находится в `books.json.example`.

## Добавление книги

```bash
python books.py add "Dune" "Frank Herbert"
```

## Поиск по автору

```bash
python books.py author "Herbert"
```

## Экспорт каталога

```bash
python books.py export
```

По умолчанию результат записывается в файл `books_export.txt`.

## Ограничение каталога

Каталог поддерживает не более 500 книг.
