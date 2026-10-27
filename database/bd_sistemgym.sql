CREATE DATABASE IF NOT EXISTS sistema_gym;

USE sistema_gym;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(18) NOT NULL,
    genero VARCHAR(50),
    senha VARCHAR(255) NOT NULL
);

CREATE TABLE alunos (
    id_usuario INT PRIMARY KEY,
    FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
);

CREATE TABLE professores (
    id_usuario INT PRIMARY KEY,
    FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
);

CREATE TABLE funcionarios (
    id_usuario INT PRIMARY KEY,
    FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
);

CREATE TABLE exercicio (
    id_exercicio INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(200) NOT NULL UNIQUE,
    maquinas_utensilios VARCHAR(200),
    descricao TEXT
);

CREATE TABLE treinos (
    id_treino INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    objetivo VARCHAR(100)
);

CREATE TABLE treino_exercicios (
    id_treino INT NOT NULL,
    id_exercicio INT NOT NULL,
    ordem INT NOT NULL,
    series INT NOT NULL,
    repeticoes INT NOT NULL,
    PRIMARY KEY (id_treino, id_exercicio),
    FOREIGN KEY (id_treino)
        REFERENCES treinos(id_treino),
    FOREIGN KEY (id_exercicio)
        REFERENCES exercicio(id_exercicio)
);
