DROP database sistema_gym;
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
