import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './DashboardPage.module.css';
import Modal from './Modal';
import AddMealModal from './AddMealModal';

function DashboardPage() {
    const navigate = useNavigate();
    const [categories, setCategories] = useState([]);
    const [meals, setMeals] = useState([]);
    const [selectedMeal, setSelectedMeal] = useState(null);
    const [isModalOpen, setModalOpen] = useState(false);
    const [isAddMealModalOpen, setAddMealModalOpen] = useState(false);
    const [products, setProducts] = useState([]);
  
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');
        if (!token) {
          alert('Unauthorized: No token provided');
          navigate('/');
        } else {
          fetch('http://localhost:8000/categories', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
              'User_Id': user_id,
            }
          })
          .then(response => response.json())
          .then(data => {
            setCategories(data);
          })
          .catch(error => {
            console.error('Error fetching categories', error);
          });
        
          fetch('http://localhost:8000/meals', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
              'User_Id': user_id,
            }
          })
          .then(response => response.json())
          .then(data => {
            setMeals(data);
          })
          .catch(error => {
            console.error('Error fetching meals', error);
          });
          fetch('http://localhost:8000/products', {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
              'User_Id': user_id,
            }
          })
          .then(response => response.json())
          .then(data => setProducts(data))
          .catch(error => console.error('Error fetching products', error));
        }
      }, [navigate]);

      const handleMealClick = (meal) => {
        setSelectedMeal(meal);
        setModalOpen(true);
      };
  
      const closeModal = () => {
        setModalOpen(false);
      };

      const openAddMealModal = () => {
        setAddMealModalOpen(true);
      };
  
      const closeAddMealModal = () => {
        setAddMealModalOpen(false);
      };

  return (
    <div className={styles.dashboard}>
      <header className={styles.header}>
        <h1>MealFuel</h1>
        <div className={styles.actions}>
          <button className={styles.addButton} onClick={openAddMealModal}>+ add</button>
          <input className={styles.search} placeholder="search meal" />
          <button className={styles.settingsButton}>logout</button>
          
        </div>
      </header>

      <aside className={styles.sidebar}>
        <nav className={styles.nav}>
          <button className={styles.navButton}>all</button>
          {categories.map((category) => (
            <button key={category.id} className={styles.navButton}>
            {category.name}
        </button>
          ))}
        </nav>
      </aside>

      <main className={styles.content}>
      <section className={styles.meals}>
          {meals.map((meal, index) => (
            <div key={index} className={styles.mealCard} onClick={() => handleMealClick(meal)}>
              {meal.name}
            </div>
          ))}
        </section>
      </main>
      {isModalOpen && selectedMeal && (
          <Modal meal={selectedMeal} onClose={closeModal} />
        )}

      {isAddMealModalOpen && (
        <AddMealModal onClose={closeAddMealModal}  categories={categories} products={products}/>
      )}
    </div>
  );
}

export default DashboardPage;
