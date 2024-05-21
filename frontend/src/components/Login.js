import React, {useState} from 'react';
import login from '../services/authService';
import {useHistory} from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const history = useHistory();
    
    const HandleLogin = async (e) => {
        e.preventDefualt()
        try {
           await login(username, password);
            history.push('/')
        } catch (error) {
            console.error("failed to login", error);
        }

    };

    return (<>
        <div className='login-form'>
            <form onSubmit={HandleLogin}>
                <div>
                    <label>Username</label>
                    <input

                    type='email'
                    placeholder='Email'
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    
                    />

                </div>
                <div>
                    <label>Password</label>
                    <input
                
                    type='text'
                    placeholder='Password'
                    value={password}
                    onChange={(e)=> setPassword(e.target.value)}

                    />  

                </div>
                 <button type='submit'>Login</button>
                
               
            </form>
        </div>
    </>);

};

export default Login;