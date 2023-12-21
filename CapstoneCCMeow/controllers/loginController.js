const bcrypt = require('bcrypt');
const saltRounds = 10;
const salt = bcrypt.genSaltSync(saltRounds); 
const jwt = require('jsonwebtoken'); 
const db = require('../middleware/dbConnection');

exports.loginUser = async (req, res) => {
    const { email, password } = req.body;

    const checkEmailQuery = "SELECT * FROM tb_user WHERE email=?";
    db.query(checkEmailQuery, [email], (err, result) => {
        if (err) throw err;
        if (result.length === 0) {
            return res.status(400).json({
                message: "Email not found"
            });
        }
        const checkPassword = bcrypt.compareSync(password, result[0].password);
        if (!checkPassword) {
            return res.status(400).json({
                message: "Incorrect password"
            });
        }
        const token = jwt.sign({
            id: result[0].id, 
            email: result[0].email
        }, 'secret', { expiresIn: '1d' });

        return res.status(200).json({
            message: "Login successful",
            token
        });
    });
}

exports.profile = async (req, res) => {
    return res.status(200).json({
        user: req.user
    });
}

exports.editUser = async (req, res) => {
    try {
        const { username, email } = req.body;
        if (!username || !email) {
            return res.status(400).json({
                message: "Please provide both username and email"
            });
        }
        const updateQuery = "UPDATE tb_user SET username=? WHERE email=?";
        db.query(updateQuery, [username, email], (err, result) => {
            if (err) throw err;
            return res.status(201).json({ message: "User updated successfully" });
        });
    } catch (error) {
        console.log(error.message);
    }
}
