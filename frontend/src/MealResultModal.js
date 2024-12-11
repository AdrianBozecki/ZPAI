import React from 'react';
import styles from './MealResultModal.module.css';

function MealResultModal({ meal, onClose, openAddMealModal }) {
  const handleBackdropClick = (event) => {
    if (event.target === event.currentTarget) {
      onClose();
    }
  };

  return (
    <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
      <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
        <h3>{meal.title}</h3>
        <img src={meal.image} alt={meal.title}/>
        <p dangerouslySetInnerHTML={{__html: meal.summary}}></p>
        <h4>Used Ingredients</h4>
        <ul>
          {meal.used_ingredients.map((ingredient, index) => (
              <li key={index}>{ingredient.amount} {ingredient.unit} {ingredient.name}</li>
          ))}
        </ul>
        <h4>Missed Ingredients</h4>
        <ul>
          {meal.missed_ingredients.map((ingredient, index) => (
              <li key={index}>{ingredient.amount} {ingredient.unit} {ingredient.name}</li>
          ))}
        </ul>
        <p>{meal.instructions}</p>
        <button className={styles.paddedButton} onClick={() => {
          console.log(meal);
          openAddMealModal(meal);
          onClose();
        }}>Save
        </button>
        <button className={styles.paddedButton} onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default MealResultModal;