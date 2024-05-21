import axios from 'axios';
import jwt_decode from 'jwt_decode';

const API_URL = 'http://127.0.0.1:8000/api/token/';
const REFRESH_API_TOKEN = 'http://127.0.0.1:8000/api/token/refresh/';
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
    return user?.access;
}

const isAuthenticated = ()=> {
    const token = getToken();
    if (token) {
        const  decodedToken = jwt_decode(token);
        return decodedToken.exp > Date.now() / 1000;

    }
    return false;
}

// Refresh the token if expired 
const refreshToken = () => {
    const user = getCurrentUser();
    if (user && user.refresh) {
        return axios.post(REFRESH_API_TOKEN, {refresh: user.refresh})
        .then(res => {
            if (res.data.access) {
                localStorage.setItem('user', JSON.stringify({...user, access: res.data.access

                }));
                return res.data.access
            } else {
                logout();
                return null
            }
        }).catch(() => {
            logout();
            return null
        })
    } else {
        logout();
        return null
    }

    }
// function to refresh the token if expired and the user is authenticated 
const checkToken = async () => {
    if (!isAuthenticated()){
        const refresh = await refreshToken();
        if (!refresh) {

            return false
        }
    }
    return true;
}

export default {
    login,
    logout,
    getCurrentUser,
    getToken,
    isAuthenticated,
    checkToken
}
