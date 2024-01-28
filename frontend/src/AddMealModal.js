import styles from './DashboardPage.module.css';
import React, { useState } from 'react';

function AddMealModal({ onClose, categories, products, onProductsUpdated }) {
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [selectedProducts, setSelectedProducts] = useState([]);
    const [newProductName, setNewProductName] = useState('');
const [newProductUnit, setNewProductUnit] = useState('');

  
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

      const handleAddProduct = async (e) => {
        e.preventDefault(); // Zapobieganie domyślnej akcji formularza
      
        const token = localStorage.getItem('access_token'); // Pobranie tokena
        const user_id = localStorage.getItem('user_id');
        const payload = {
          name: newProductName,
          unit_of_measure: newProductUnit,
        };
      
        try {
          const response = await fetch('http://localhost:8000/products', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
              'User_id': user_id,
            },
            body: JSON.stringify(payload),
          });
      
          if (response.ok) {
            alert('Product added successfully!');
            onProductsUpdated();
          } else {
            throw new Error('Failed to add new product');
          }
      
          setNewProductName('');
          setNewProductUnit('');
      
        } catch (error) {
          console.error('Error adding new product:', error);
          alert('Failed to add new product.');
        }
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
        <h3>Add new product</h3>
        <form onSubmit={handleAddProduct}>
  <input
    type="text"
    placeholder="Product Name"
    value={newProductName}
    onChange={(e) => setNewProductName(e.target.value)}
  />
  <select value={newProductUnit} onChange={(e) => setNewProductUnit(e.target.value)}>
    <option value="">Select Unit</option>
    <option value="GRAM">Gram</option>
    <option value="MILLILITER">Milliliter</option>
    <option value="CENTIMETER">Centimeter</option>
    <option value="PIECE">Piece</option>
  </select>
  <button type="submit">Add Product</button>
</form>
      </div>
    );
  }
  
  export default AddMealModal;
  