const express = require('express');
const mysql = require('mysql2');

const app = express();
const port = 5000;

// Configurar a conexão com o banco de dados MySQL
const db_config = {
    host: 'localhost',
    user: 'root', 
    password: '', 
    database: 'aniversario'
};

const pool = mysql.createPool(db_config); // Criar um pool de conexões

app.use(express.json()); // Middleware para analisar o corpo da requisição como JSON

app.post('/aniversariantes', (req, res) => {
    const nome = req.body.nome;

    if (!nome) {
        return res.status(400).json({ message: 'Nome é obrigatório' });
    }

    pool.getConnection((err, connection) => {
        if (err) {
            console.error('Erro ao conectar ao banco de dados:', err);
            return res.status(500).json({ message: 'Erro interno do servidor' });
        }

        const query = 'INSERT INTO aniversariante (nome) VALUES (?)';
        connection.query(query, [nome], (err, results) => {
            connection.release(); // Liberar a conexão de volta para o pool

            if (err) {
                console.error('Erro ao inserir no banco de dados:', err);
                return res.status(500).json({ message: 'Erro interno do servidor' });
            }

            res.status(201).json({ message: 'Aniversariante criado com sucesso', nome });
        });
    });
});

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});