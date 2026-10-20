drop database sistema_gym;
create database if not exists sistema_gym;

use sistema_gym;

create table cadastro_prof(
	id_prof int not null unique primary key,
	CPF varchar(14) not null unique,
	nome varchar(100) not null,
	email varchar(150) not null unique,
	data_nascimento date not null,
	telefone varchar(18) not null,
	genero varchar(50),
    senha varchar(100) not null
);

create table cadastro_aluno(
	id_aluno int not null unique primary key,
    CPF varchar(14) not null unique,
	nome varchar(100) not null,
	email varchar(150) not null unique,
	data_nascimento date not null,
	telefone varchar(18) not null,
	genero varchar(50),
    senha varchar(100) not null
    );
    
create table exercicio(
	id int not null unique primary key,
	nome varchar(200) not null unique,
    maquinas_utensilios varchar(200),
	descricao text
    );
    

	
    