const jwt = require('jsonwebtoken');

exports.isAuthorized = (req,res,next) =>{
    const token = req.headers['authorization'];
    const splittoken = token.split(' ')[1];
    if(!token == null){
      return res.status(401).json({msg:"Unauthorized"});
    }
    jwt.verify(splittoken,'secret',(err,result) =>{
      if(err){
        return res.status(401).json({
          msg:"Unauthorized"
        });
      }
      req.user = result;
      next();
    })
  }