import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './DashboardPage.module.css';
import Modal from './Modal';
import AddMealModal from './AddMealModal';
import FindMealModal from './FindMealModal';
import UpdateMealModal from "./UpdateMealModal";
import 'bootstrap/dist/css/bootstrap.min.css';
import { FaBars } from 'react-icons/fa'; // Importing icons for hamburger menu
import { makeRequest } from './utils';

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
  const [isEditModalOpen, setEditModalOpen] = useState(false);
  const [mealToEdit, setMealToEdit] = useState(null);
  const [isSidebarOpen, setSidebarOpen] = useState(false); // State for sidebar visibility

  const handleEditClick = (meal) => {
    setMealToEdit(meal);
    setEditModalOpen(true);
  };

  const fetchProducts = async () => {
    const user_id = localStorage.getItem('user_id');
    const response = await makeRequest('http://localhost:8000/products', {
      headers: {
        'User_Id': user_id,
      },
    });

    if (response.ok) {
      const data = await response.json();
      setProducts(data);
    } else {
      console.error('Error fetching products', response.statusText);
    }
  };

  const fetchMeals = async (categoryId = null, searchQuery = '') => {
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

    const response = await makeRequest(url, {
      headers: {
        'User_Id': user_id,
      },
    });

    if (response.ok) {
      const data = await response.json();
      setMeals(data);
      setSidebarOpen(false); // Hide sidebar after selecting a category
    } else {
      console.error('Error fetching meals', response.statusText);
    }
};

  const refreshMeals = () => {
    fetchMeals();
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
      setIsLoading(true);
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
        setIsLoading(false);
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
    localStorage.clear();
    navigate('/');
  };

  if (!isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className={`container-fluid ${styles.dashboard}`}>
      <header className={`${styles.header}`}>
        <button className={styles.hamburger} onClick={() => setSidebarOpen(!isSidebarOpen)}>
          <FaBars />
        </button>
        <h1 className={styles.title}>MealFuel</h1>
        <div className={styles.actions}>
          <button className={`btn btn-primary ${styles.findButton}`} onClick={openFindMealModal}>find meal</button>
          <button className={`btn btn-primary ${styles.addButton}`} onClick={openAddMealModal}>+ add meal</button>
          <input
              className={`form-control ${styles.search}`}
              placeholder="search meal"
              value={searchQuery}
              onChange={handleSearchChange}
          />
          <button className={`btn btn-danger ${styles.settingsButton}`} onClick={handleLogout}>logout</button>
        </div>
      </header>

      <div className="row">
        <aside className={`${styles.sidebar} ${isSidebarOpen ? styles.open : ''}`}>
          <nav className={styles.nav}>
            <button className={`btn btn-light ${styles.navButton}`} onClick={() => fetchMeals()}>all</button>
            {categories.map((category) => (
              <button key={category.id} className={`btn btn-light ${styles.navButton}`} onClick={() => fetchMeals(category.id)}>
                {category.name}
              </button>
            ))}
          </nav>
        </aside>

        <main className={`${styles.content}`}>
          <section className={styles.meals}>
            {meals.map((meal, index) => (
                <div key={index} className={styles.mealCard} onClick={() => handleMealClick(meal)}>
                  <div className={styles.imageContainer}>
                    <img src={meal.image_url || "/img/placeholder.png"} alt="Meal" className={styles.mealImage}/>
                  </div>
                  <div className={styles.mealName}>
                    {meal.name}
                  </div>
                </div>
            ))}
          </section>
        </main>
      </div>

      {isModalOpen && selectedMeal && (
          <Modal meal={selectedMeal} onEdit={handleEditClick} onClose={closeModal} categories={categories}
                 products={products} onMealsRefresh={refreshMeals}/>
      )}

      {isEditModalOpen && mealToEdit && (
        <UpdateMealModal mealToUpdate={mealToEdit} onClose={() => setEditModalOpen(false)} categories={categories} onMealsRefresh={refreshMeals}/>
      )}

      {isAddMealModalOpen && (
        <AddMealModal mealToAdd={mealToAdd} onClose={closeAddMealModal} categories={categories} products={products} onProductsUpdated={fetchProducts} onMealsRefresh={refreshMeals}/>
      )}

      {isFindMealModalOpen && (
        <FindMealModal onClose={closeFindMealModal} setAddMealModalOpen={setAddMealModalOpen} setMealToAdd={setMealToAdd} />
      )}
    </div>
  );
}

export default DashboardPage;