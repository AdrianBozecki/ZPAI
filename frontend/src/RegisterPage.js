import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './RegisterPage.module.css';

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
      setError('Hasła nie są identyczne.');
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
    <div className={styles.container}>
      <h1 className={styles.title}>MealFuel</h1>
      {error && <p className={styles.error}>{error}</p>}
      <form onSubmit={handleRegister} className={styles.form}>
        <label className={styles.label}>
          email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={styles.input}
          />
        </label>
        <label className={styles.label}>
          name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className={styles.input}
          />
        </label>
        <label className={styles.label}>
          lastname:
          <input
            type="text"
            value={lastname}
            onChange={(e) => setLastname(e.target.value)}
            className={styles.input}
          />
        </label>
        <label className={styles.label}>
          phone number:
          <input
            type="tel"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            className={styles.input}
          />
        </label>
        <label className={styles.label}>
          password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={styles.input}
          />
        </label>
        <label className={styles.label}>
          confirm password:
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className={styles.input}
          />
        </label>
        <button type="submit" className={styles.button}>sign up</button>
      </form>
    </div>
  );
}

export default RegisterPage;
