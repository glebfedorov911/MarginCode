# MarginCode

## Как составить .env файл

***
*.env* содержит в себе следующие переменные

```
POSTGRES_USER= Указываем имя пользователя postgresql, например postgres
POSTGRES_PASSWORD= Указываем пароль, который прикреплен к пользователю
POSTGRES_DB= Название нашей базы в postgresql
DATABASE_URL=postgresql+asyncpg://POSTGRES_USER:POSTGRES_PASSWORD@CONTAINER_NAME/HOST:PORT/POSTGRES_DB
// В DATABASE_URL указать все в ручную, а не переменными (то что заглавными буквами)
DATABASE_ECHO=Указываем хотим ли мы видеть сообщения о запросах (true/false)

SECRET_KEY=Секретный ключ будет описан ниже
TOKEN_ALGORITHM=Алгоритм шифрования
TOKEN_EXPIRES=Время истечения токена (ОБЯЗАТЕЛЬНО ЧИСЛО)
TOKEN_TYPE=Тип токена (Bearer)

PASSWORD_TO_CREATE_USER=Поле которое хранит пароля для создания юзера
```

***
Для того чтобы сгенерировать *secret key* необходимо воспользоваться OpenSSL, 
ключ генерируется следующей командной:

```
openssl rand -hex 32 // Необходимо перейти в директрою с openssl (на Windows: openssl.exe)
```

***
