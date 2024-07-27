import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './DashboardPage.module.css';
import Modal from './Modal';
import AddMealModal from './AddMealModal';
import FindMealModal from './FindMealModal';

function DashboardPage() {
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [meals, setMeals] = useState([]);
  const [selectedMeal, setSelectedMeal] = useState(null);
  const [isModalOpen, setModalOpen] = useState(false);
  const [isAddMealModalOpen, setAddMealModalOpen] = useState(false);
  const [products, setProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isFindMealModalOpen, setFindMealModalOpen] = useState(false);
  const [mealToAdd, setMealToAdd] = useState(null);

  const fetchProducts = () => {
    const token = localStorage.getItem('access_token');
    const user_id = localStorage.getItem('user_id');
    
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
  };

  const fetchMeals = (categoryId = null, searchQuery = '') => {
    const token = localStorage.getItem('access_token');
    const user_id = localStorage.getItem('user_id');
    let url = 'http://localhost:8000/meals';
  
    const params = new URLSearchParams();
    if (categoryId) {
      params.append('category_id', categoryId);
    }
    if (searchQuery) {
      params.append('name', searchQuery);
    }
    url += `?${params.toString()}`;
  
    fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'User_Id': user_id,
      }
    })
    .then(response => response.json())
    .then(data => setMeals(data))
    .catch(error => console.error('Error fetching meals', error));
  };
  const refreshMeals = () => {
    fetchMeals(); // funkcja, którą już masz zdefiniowaną do pobierania posiłków
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const user_id = localStorage.getItem('user_id');
    if (!token) {
      alert('Unauthorized: No token provided');
      navigate('/');
    } else {
      setIsLoading(true); // Aktualizacja stanu, nawet jeśli brakuje tokena
      Promise.all([
        fetch('http://localhost:8000/categories', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'User_Id': user_id,
          }
        }).then(response => response.json()),
        fetchMeals(),
        fetchProducts()
      ]).then(([categoriesData]) => {
        setCategories(categoriesData)
      }).catch(error => {
        console.error('Error fetching data', error);
        setIsLoading(false); // Aktualizacja stanu również w przypadku błędu
      });
    }
  }, [navigate]);

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      fetchMeals(null, searchQuery);
    }, 500);
  
    return () => clearTimeout(delayDebounce);
  }, [searchQuery]);

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

  const openFindMealModal = () => {
  setFindMealModalOpen(true);
};

  const closeFindMealModal = () => {
  setFindMealModalOpen(false);
};

  const handleLogout = () => {
    localStorage.clear(); // Czyści cały localStorage
    navigate('/'); // Przekierowuje na stronę główną
  };


  if (!isLoading) {
    return <div>Loading...</div>; // Wyświetlenie informacji o ładowaniu, gdy dane są jeszcze pobierane
  }

  return (
    <div className={styles.dashboard}>
        
      <header className={styles.header}>
        <h1>MealFuel</h1>
        <div className={styles.actions}>
          <button className={styles.findButton} onClick={openFindMealModal}>Find Meal</button>
          <button className={styles.addButton} onClick={openAddMealModal}>+ add meal</button>
          <input
              className={styles.search}
              placeholder="search meal"
              value={searchQuery}
              onChange={handleSearchChange}
          />
          <button className={styles.settingsButton} onClick={handleLogout}>logout</button>

        </div>
      </header>

      <aside className={styles.sidebar}>
        <nav className={styles.nav}>
          <button className={styles.navButton} onClick={() => fetchMeals()}>all</button>
          {categories.map((category) => (
            <button key={category.id} className={styles.navButton} onClick={() => fetchMeals(category.id)}>
              {category.name}
            </button>
          ))}
        </nav>
      </aside>

      <main className={styles.content}>
      <section className={styles.meals}>
  {meals.map((meal, index) => (
    <div key={index} className={styles.mealCard} onClick={() => handleMealClick(meal)}>
      <img
        src="/img/placeholder.png"
        alt="Meal"
        className={styles.mealImage} // Dodaj klasę dla stylizacji obrazka
      />
      {meal.name}
    </div>
  ))}
</section>
      </main>

      {isModalOpen && selectedMeal && (
        <Modal meal={selectedMeal} onClose={closeModal} categories={categories} products={products} onMealsRefresh={refreshMeals}/>
      )}

{isAddMealModalOpen && (
  <AddMealModal mealToAdd={mealToAdd} onClose={closeAddMealModal} categories={categories} products={products} onProductsUpdated={fetchProducts} onMealsRefresh={refreshMeals}/>
)}

      {isFindMealModalOpen && (
<FindMealModal onClose={closeFindMealModal} setAddMealModalOpen={setAddMealModalOpen} setMealToAdd={setMealToAdd} />)}
    </div>
  );
}

export default DashboardPage;
