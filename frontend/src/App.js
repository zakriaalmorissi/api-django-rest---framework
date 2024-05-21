
import Api from './api'
import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import Login  from './components/Login';


function App() {
  return <>
  <BrowserRouter>
    <Routes>
        <Route 
        path="/" 
        element= {<Api/>}/>
        <Route path="/login" 
        element = {<Login/>}/>
    </Routes>
  </BrowserRouter>
  
  </>
}

export default App;
