import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './LoginPage.module.css'; // Import custom CSS

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
        localStorage.setItem('refresh_token', data.refresh_token);
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

  return (
    <div className={`container ${styles.container}`}>
      <div className={`card ${styles.card}`}>
        <div className={`card-body ${styles.cardBody}`}>
          <h3 className="card-title text-center">Login</h3>
          <form onSubmit={handleLogin}>
            <div className={`form-group ${styles.formGroup}`}>
              <label htmlFor="email">Email address</label>
              <input
                  type="email"
                  className={`form-control ${styles.formControl}`}
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
              />
            </div>
            <div className={`form-group ${styles.formGroup}`}>
              <label htmlFor="password">Password</label>
              <input
                  type="password"
                  className={`form-control ${styles.formControl}`}
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
              />
            </div>
            <button type="submit" className={`btn btn-primary ${styles.btn}`}>
              Login
            </button>
          </form>
          <div className={`text-center mt-3 ${styles.textCenter}`}>
            <p>Don't have an account?</p>
            <Link to="/register" className={`btn btn-secondary ${styles.btn}`}>
              Register
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;