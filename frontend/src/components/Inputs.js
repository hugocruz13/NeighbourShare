import "../styles/Inputs.css"

function InputLogin ({ name, value, onChange}){
    return (
        <div className="container-email">
        <label>Email</label>
        <br></br>
        <input type="email" name={name} className="input" value={value}  onChange={onChange}  required />
      </div>
    );
}   

function InputPassword({ name, value, onChange}){
    return(
        <div className="container-pass">
        <label>Password</label>
        <br></br>
        <input type="password" name={name} className="input" value={value}  onChange={onChange} required/>
      </div>
    );
}

export { InputLogin, InputPassword };