import React, { useState } from 'react';
import styles from './Modal.module.css';

function Modal({ meal, onClose, categories, onMealsRefresh}) {
    const localUserId = localStorage.getItem('user_id');
    const [unitSystem, setUnitSystem] = useState('METRIC');

    const handleBackdropClick = (event) => {
        if (event.target === event.currentTarget) {
          onClose();
        }
    };


const handleDelete = async () => {
  const token = localStorage.getItem('access_token'); // Pobierz token z localStorage
  const user_id = localStorage.getItem('user_id'); // Pobierz user_id z localStorage


  if (meal.user_id.toString() === user_id) {
    try {
      const response = await fetch(`http://localhost:8000/meals/${meal.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`, // Wstaw token do nagłówka autoryzacji
          'Content-Type': 'application/json',
          'User_id': user_id,
        }
      });

      if (response.ok) {
        console.log(`Meal with id: ${meal.id} was deleted.`);
        onMealsRefresh();
        onClose();
      } else {
        console.error('Failed to delete the meal.');
        alert('Failed to delete the meal.');
      }
    } catch (error) {
      console.error('There was an error deleting the meal:', error);
      alert('There was an error deleting the meal.');
    }
  } else {
    alert('You do not have permission to delete this meal.');
  }
};

    const handleExport = () => {
        const token = localStorage.getItem('access_token');
        const url = `http://localhost:8000/meals/${meal.id}/shopping-list?unit_system=${unitSystem}`;
        window.open(url, '_blank');
    };

    const getCategoryNames = (categoryIds) => {
        return categoryIds
            .map(id => categories.find(category => category.id === id))
            .filter(category => category != null)
            .map(category => category.name);
    };

    const categoryNames = getCategoryNames(meal.category_ids);

    return (
        <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
            <div className={styles.modalContent}>
                <h2>{meal.name}</h2>
                <img src="/img/placeholder.png" alt="Meal"/>
                <p><b>description:</b> {meal.description}</p>
                <p><b>categories:</b> {categoryNames.join(', ')}</p>
                <p><b>products:</b></p>
               {meal.products.map(product => {
              const unit = product.value > 1 ? `${product.unit_of_measure.toLowerCase()}s` : product.unit_of_measure.toLowerCase();
              return (
                <p key={product.name}> {product.name} {product.value} {unit}</p>
              );
            })}
                <p><b>preparation:</b> <div style={{ whiteSpace: 'pre-wrap' }}>{meal.preparation}</div></p>
                <p><b>created by user:</b> {meal.user_id}</p>
                <div className={styles.exportSection}>
                    <div>
                        <label>
                            <input type="radio" value="METRIC" checked={unitSystem === 'METRIC'} onChange={() => setUnitSystem('METRIC')} />
                            Metric
                        </label>
                        <label>
                            <input type="radio" value="IMPERIAL" checked={unitSystem === 'IMPERIAL'} onChange={() => setUnitSystem('IMPERIAL')} />
                            Imperial
                        </label>
                    </div>
                    <button onClick={handleExport}>Export Shopping List</button>
                </div>
                    {localUserId === meal.user_id.toString() && (
                    <button onClick={handleDelete}>Delete</button>
                )}
                <button onClick={onClose}>Close</button>
            </div>
        </div>
    );
}

export default Modal;