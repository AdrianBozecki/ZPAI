import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import styles from './RegisterPage.module.css'; // Import custom CSS

function RegisterPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [lastname, setLastname] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async (event) => {
    event.preventDefault();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
      setError('Proszę wprowadzić poprawny adres e-mail.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords are not matching.');
      return;
    }

    setError('');

    const userData = {
      email,
      name,
      lastname,
      phone_number: phoneNumber,
      password
    };

    try {
      const response = await fetch('http://localhost:8000/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });

      if (response.status === 201) {
        navigate('/');
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Error occured.');
      }
    } catch (error) {
      setError('Error occured.');
      console.error('There was an error!', error);
    }
  };


  return (
    <div className={`container ${styles.container}`}>
      <div className={`card ${styles.card}`}>
        <div className="card-body">
          <h1 className={`card-title ${styles.cardTitle}`}>Registration</h1>
          {error && <p className={`error-message ${styles.errorMessage}`}>{error}</p>}
          <form onSubmit={handleRegister}>
            <div className="mb-3">
              <label htmlFor="email" className={`form-label ${styles.formLabel}`}>Email</label>
              <input
                type="email"
                className={`form-control ${styles.formControl}`}
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="name" className={`form-label ${styles.formLabel}`}>Name</label>
              <input
                type="text"
                className={`form-control ${styles.formControl}`}
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="lastname" className={`form-label ${styles.formLabel}`}>Lastname</label>
              <input
                type="text"
                className={`form-control ${styles.formControl}`}
                id="lastname"
                value={lastname}
                onChange={(e) => setLastname(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="phoneNumber" className={`form-label ${styles.formLabel}`}>Phone Number</label>
              <input
                type="tel"
                className={`form-control ${styles.formControl}`}
                id="phoneNumber"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="password" className={`form-label ${styles.formLabel}`}>Password</label>
              <input
                type="password"
                className={`form-control ${styles.formControl}`}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="confirmPassword" className={`form-label ${styles.formLabel}`}>Confirm Password</label>
              <input
                type="password"
                className={`form-control ${styles.formControl}`}
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className={`btn btn-primary ${styles.btnPrimary}`}>Sign Up</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
