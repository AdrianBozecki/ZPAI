import React, { useState } from 'react';
import styles from './FindMealModal.module.css';
import MealResultModal from './MealResultModal';

function FindMealModal({ onClose , setAddMealModalOpen, setMealToAdd}) {
  const [products, setProducts] = useState([]);
  const [product, setProduct] = useState('');
  const [mealResult, setMealResult] = useState(null);

  const handleBackdropClick = (event) => {
    if (event.target === event.currentTarget) {
      onClose();
    }
  };

  const handleProductChange = (event) => {
    setProduct(event.target.value);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    setProducts([...products, product]);
    setProduct('');
  };

  const handleProductDelete = (index) => {
    const newProducts = [...products];
    newProducts.splice(index, 1);
    setProducts(newProducts);
  };

  const handleFindMeal = async () => {
    const ingredients = products.join(',');
    const response = await fetch(`http://localhost:8000/spooncular-meals/find-by-ingredients?ingredients=${ingredients}`);
    const data = await response.json();
    setMealResult(data);
  };

  const closeMealResultModal = () => {
    setMealResult(null);
  };

  const openAddMealModal = (meal) => {
  const mealToAdd = {
    name: meal.title,
    description: meal.summary.replace(/<[^>]*>/g, ''),
    preparation: meal.instructions.replace(/<[^>]*>/g, ''),
    products: [...meal.used_ingredients, ...meal.missed_ingredients].map(ingredient => ({
      name: ingredient.name,
      value: ingredient.amount,
      unit_of_measure: 'PIECE',
    })),
    image: meal.image,
  };
  setMealToAdd(mealToAdd);
  setAddMealModalOpen(true);
  onClose();
};

  return (
    <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        <h3>Enter the products you have</h3>
        <form onSubmit={handleFormSubmit}>
          <input
            type="text"
            placeholder="Product name"
            value={product}
            onChange={handleProductChange}
          />
          <button type="submit">Add</button>
        </form>
        <ul>
          {products.map((product, index) => (
            <li key={index}>
              {product}
              <button onClick={() => handleProductDelete(index)}>-</button>
            </li>
          ))}
        </ul>
        <button className={styles.findMealButton} onClick={handleFindMeal}>Find Meal</button>
      </div>
        {mealResult && (
          <MealResultModal meal={mealResult} onClose={closeMealResultModal} openAddMealModal={openAddMealModal} />
        )}
    </div>
  );
}

export default FindMealModal;