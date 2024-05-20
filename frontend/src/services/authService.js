import axios from 'axios';
import jwt_decode from 'jwt_decode';

API_URL = 'http://127.0.0.1:8000/api/token/'

// create a service for handling the authentication 

const login = (username, password) => {
    // post the recieved data to the backend
    return axios.post(API_URL, {username, password})
    .then(res => {
        if (res.data.access) {
            // Convert the token into JSON string and store it in the local storage
            console.log(res.data)
            localStorage.setItem('user', JSON.stringify(res.data)) 
        }
        return res.data
    });

};
const logout = ()=> {
    localStorage.removeItem('user');
};


const getCurrentUser = ()=> {
   let user = localStorage.getItem('user')
   console.log(user)
   return JSON.parse(user);
}

const getToken = ()=> {
    const user = getCurrentUser();
    // what is this statement ?
    return user?.access;
}

const isAuthenticated = ()=> {
    const token = getToken();
    if (token) {
        // what does the jwt_decode do to the token
        const  decodedToken = jwt_decode(token);
        return decodedToken.exp > Date.now() / 1000;

    }
    return false;
}

export default {
    login,
    logout,
    getCurrentUser,
    getToken,
    isAuthenticated,
}
