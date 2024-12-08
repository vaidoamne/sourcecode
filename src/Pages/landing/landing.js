import React , { useState }from 'react';
import { Link } from 'react-router-dom';
import './landing.css'; 

const Landing = () => {
  
    const [inputValue, setInputValue] = useState('');
    const [passwordValue, setpasswordValue] = useState('');

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
      };
      const handlePasswordChange = (e) => {
        setpasswordValue(e.target.value);
      };


  return (

    
    <div className="landing-container">
    <div className='logo'></div>
    <div className='company-name'>Railroad Lens</div>
      <div className="background-image"></div>
      <div className="gradient-overlay"></div>
      <div className="landing-content">
        <div className='login-container'>
            <h2>Login</h2>
            <p>Username</p>
            <input
            id="userInput"
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Type here..."
          />
          <p>Password</p>
          <input
          id="Password"
          type="text"
          value={passwordValue}
          onChange={handlePasswordChange}
          placeholder="Type here..."
        />
        </div>

        <Link to="/home">
          <button className='Login-Button'>Go to Home Page</button>
        </Link>
        <div className='signup-text'>Don't have an account? Sign Up</div>
      </div>


    </div>
  );
};

export default Landing;
