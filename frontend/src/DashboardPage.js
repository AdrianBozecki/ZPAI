import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './DashboardPage.module.css'; // Załóżmy, że masz już odpowiednie style

function DashboardPage() {
    const navigate = useNavigate();
  
    useEffect(() => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        // Jeśli nie ma tokena, wyświetl komunikat i przekieruj do strony logowania
        alert('Unauthorized: No token provided');
        navigate('/');
      }
    }, [navigate]);

  return (
    <div className={styles.dashboard}>
      <header className={styles.header}>
        <h1>MealFuel</h1>
        <div className={styles.actions}>
          <button className={styles.addButton}>+ add</button>
          <input className={styles.search} placeholder="search meal" />
          <button className={styles.settingsButton}>logout</button>
        </div>
      </header>

      <aside className={styles.sidebar}>
        <nav className={styles.nav}>
          <button className={styles.navButton}>all</button>
          <button className={styles.navButton}>breakfast</button>
          <button className={styles.navButton}>lunch</button>
          <button className={styles.navButton}>soup</button>
          <button className={styles.navButton}>dinner</button>
          <button className={styles.navButton}>drinks</button>
        </nav>
      </aside>

      <main className={styles.content}>
        <section className={styles.meals}>
          {/* Placeholder dla poszczególnych posiłków */}
          <div className={styles.mealCard}>lasagne</div>
          <div className={styles.mealCard}>lasagne</div>
          <div className={styles.mealCard}>lasagne</div>
          {/* Powtórz dla każdego posiłku */}
        </section>
      </main>
    </div>
  );
}

export default DashboardPage;
