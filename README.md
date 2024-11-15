# Picture chat

A chat from the old days.

![demo](demo.gif)

## Installation

### Database

The application uses a `postgres` database.

The database uri should be placed in the `picture_chat/yoyo.ini`
file. You can get more informations about the database uri string in the [yoyo documentation](https://ollycope.com/software/yoyo/latest/#connecting-to-a-database).

example :

```ini
[DEFAULT]
sources = migrations
database = postgres://postgres:example@localhost:5432/picture_chat
batch_mode = off
verbosity = 0
```

#### Environment

You need to copy `picture_chat/.env.example` and `front./env.example` to `.env`

```shell
cp picture_chat/.env.example picture_chat/.env
cp front/.env.example front/.env
```

Note that you will have to change all the values for a production deployement.

### Commands to launch

When the database and `.env` are configured correctly you can launch those commands

```shell
poetry install

cd picture_chat
poetry run yoyo apply # you may have to respond with 'a' when prompted

cd ../front
npm install
cd ..
sh ./run.sh
```

you can then access to the application here: [http://localhost:3000](http://localhost:3000)

For a prodution deployement you may change what's inside `run.sh`

## Stack

The frontend has been made with `Svelte`.
There are no dependencies. The editor is just a plain text area with a canvas.

The backend uses `FastAPI` with a sort of "thin layered" three-tier architecture.

Images are stored as an array of bytes directly in the database,
and the chat uses `websockets` to handle connections and data transfer.
