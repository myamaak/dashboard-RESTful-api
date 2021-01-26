create table if not exists users(
	 id int not null auto_increment,
	 username varchar(64) not null,
	 email varchar(64) not null,
	 password text not null,
	 primary key (id)
);
create table if not exists board(
    id int not null AUTO_INCREMENT,
    boardname varchar(64) not null,
    create_date timestamp default NOW(),
    user_id int not null,
    primary key (id),
    foreign key (user_id) references users(id)
);

create table if not exists boardArticle(
    id int not null AUTO_INCREMENT,
    title varchar(64) not null,
    content text,
    board_id int not null,
    user_id int not null,
    create_date timestamp default NOW(),
    primary key (id),
    foreign key (board_id) references board(id),
    foreign key (user_id) references users(id)
);

