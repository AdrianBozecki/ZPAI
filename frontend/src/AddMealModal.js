import styles from './DashboardPage.module.css';
import React, { useState } from 'react';

function AddMealModal({ onClose, categories, products}) {
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [selectedProducts, setSelectedProducts] = useState([]);

  
    const handleCategoryChange = (event) => {
      const options = event.target.options;
      const value = [];
      for (let i = 0, l = options.length; i < l; i++) {
        if (options[i].selected) {
          value.push(options[i].value);
        }
      }
      setSelectedCategories(value);
    };

      
    const handleProductChange = (event) => {
        const options = event.target.options;
        const value = [];
        for (let i = 0, l = options.length; i < l; i++) {
          if (options[i].selected) {
            value.push(options[i].value);
          }
        }
        setSelectedProducts(value);
      };


    
  
    return (
      <div className={styles.modalBackdrop}>
        <div className={styles.modalContent}>
            
          <h2>Add New Meal</h2>
          <form>
            <input type="text" placeholder="Name" /* reszta atrybutów */ />
            <select name="categories" multiple value={selectedCategories} onChange={handleCategoryChange}>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
          <select name="products" multiple value={selectedProducts} onChange={handleProductChange}>
            {products.map((product) => (
              <option key={product.id} value={product.id}>
                {product.name}
              </option>
            ))}
          </select>
            <textarea placeholder="Description" /* reszta atrybutów */></textarea>
            <textarea placeholder="Preparation" /* reszta atrybutów */></textarea>
            <button type="submit">Submit</button>
            <button onClick={onClose}>Close</button>
          </form>
        </div>
      </div>
    );
  }
  
  export default AddMealModal;
  