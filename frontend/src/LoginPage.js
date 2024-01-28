import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Importujesz Link z react-router-dom
import styles from './LoginPage.module.css';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (event) => {
    event.preventDefault();
  
    const loginData = {
      email: email,
      password: password,
    };
  
    try {
      const response = await fetch('http://localhost:8000/users/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('token_type', data.token_type);
        localStorage.setItem('user_id', data.user_id);

        navigate('/dashboard');
      } else {
        alert('Login failed: Incorrect email or password.');
        console.error('Login failed:', data.error);
      }
    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>MealFuel</h1>
      <form onSubmit={handleLogin} className={styles.form}>
        <label className={styles.label}>
          email:
          <input
            type="text"
            value={email}
            onChange={handleEmailChange}
            className={styles.input}
            placeholder="email"
          />
        </label>
        <label className={styles.label}>
          password:
          <input
            type="password"
            value={password}
            onChange={handlePasswordChange}
            className={styles.input}
            placeholder="password"
          />
        </label>
        <button type="submit" className={styles.button}>Sign in</button>
        <Link to="/register" className={styles.linkContainer}>
        < button type="button" className={styles.linkButton}>SIGN UP</button>
        </Link>
      </form>
    </div>
  );
}

export default LoginPage;
