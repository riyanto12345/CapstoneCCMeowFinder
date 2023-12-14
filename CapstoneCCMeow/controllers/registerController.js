const bcrypt = require('bcrypt');
const saltRounds = 10;
const gensalt = bcrypt.genSaltSync(saltRounds); 
const db = require('../middleware/dbConnection');

exports.registerUser = async (req,res) =>{
    const {email,username,password} = req.body;
    if(!email||!username||!password){
        return res.status(400).json({
          msg:"Please fill all the fields"
        });
    }

    const queryEmail = "SELECT * FROM tb_user WHERE email=?";
    db.query(queryEmail,[email],(err,result) =>{
        if(err) throw err;
        if(result.length> 0){
            return res.status(400).json({
              msg:"Email already exists"});
        }
  
        const query = "INSERT INTO tb_user(email,username,password) VALUES (?,?,?)";
        db.query(query,[email,username,bcrypt.hashSync(password,saltRounds)],(err,result) =>{
            if(err) throw err;
            return res.status(201).json({msg:"User registered successfully"});
        })
    })  
    
  }

  exports.getUser = async (req, res) => {
    const query = "SELECT * FROM tb_user";
    db.query(query, (err, result) => {
      if (err) throw err;
      return res.status(200).json({ result });
    });
  };
  