const bcrypt = require('bcrypt');
const saltRounds = 10;
const salt = bcrypt.genSaltSync(saltRounds); 
const db = require('../middleware/dbConnection');

exports.registerUser = async (req, res) => {
    const { email, username, password } = req.body;
    if (!email || !username || !password) {
        return res.status(400).json({
            message: "Please complete all the required fields"
        });
    }

    const checkEmailQuery = "SELECT * FROM tb_user WHERE email=?";
    db.query(checkEmailQuery, [email], (err, result) => {
        if (err) throw err;
        if (result.length > 0) {
            return res.status(400).json({
                message: "Email already in use. Please choose another one."
            });
        }

        const insertQuery = "INSERT INTO tb_user(email, username, password) VALUES (?,?,?)";
        db.query(insertQuery, [email, username, bcrypt.hashSync(password, saltRounds)], (err, result) => {
            if (err) throw err;
            return res.status(201).json({ message: "User successfully registered" });
        });
    });
}

exports.getUser = async (req, res) => {
    const query = "SELECT * FROM tb_user";
    db.query(query, (err, result) => {
        if (err) throw err;
        return res.status(200).json({ users: result });
    });
};
