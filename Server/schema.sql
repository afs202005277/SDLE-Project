
DROP TABLE IF EXISTS user_list;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS shopping_lists;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE shopping_lists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE user_list (
    user_id INTEGER REFERENCES users(id),
    list_id INTEGER REFERENCES shopping_lists(id),
    PRIMARY KEY (user_id, list_id)
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bought BOOLEAN DEFAULT FALSE,
    quantity INTEGER,
    list_id INTEGER REFERENCES shopping_lists(id) NOT NULL
);

insert into users (name, email, password) values ('teste1', 'teste1@gmail.com', '$2b$12$FxwkbqOXyjELCWhnMdJeFeTjTkBywMh3q4QXrJWM4UgIvcddsDjiu');
insert into users (name, email, password) values ('teste2', 'teste2@gmail.com', '$2b$12$FxwkbqOXyjELCWhnMdJeFeTjTkBywMh3q4QXrJWM4UgIvcddsDjiu');

insert into shopping_lists (name) values ('Lista de Teste');

insert into user_list (user_id, list_id) values (1, 1);
insert into user_list (user_id, list_id) values (2, 1);

insert into items (name, bought, quantity ,list_id) values ('item1', FALSE, 3, 1);
insert into items (name, bought, quantity ,list_id) values ('item2', FALSE, 1, 1);
insert into items (name, bought, quantity ,list_id) values ('item3', FALSE, 2, 1);
insert into items (name, bought, quantity ,list_id) values ('item4', TRUE, 0, 1);