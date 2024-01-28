import React, { useState } from 'react';
import styles from './AddMealModal.module.css';

function AddMealModal({ onClose, categories, products, onProductsUpdated, onMealsRefresh}) {
    const [selectedCategories, setSelectedCategories] = useState([]);
    const [selectedProducts, setSelectedProducts] = useState([]);
    const [newProductName, setNewProductName] = useState('');
    const [newProductUnit, setNewProductUnit] = useState('');
    const [mealName, setMealName] = useState('');
    const [mealDescription, setMealDescription] = useState('');
    const [mealPreparation, setMealPreparation] = useState('');

    const handleBackdropClick = (event) => {
        if (event.target === event.currentTarget) {
            onClose();
        }
    };

    const handleCategoryChange = (event) => {
        const selectedOptions = Array.from(event.target.selectedOptions).map(option => option.value);
        setSelectedCategories(selectedOptions);
    };

    const handleProductChange = (event) => {
        const selectedOptions = Array.from(event.target.selectedOptions).map(option => option.value);
        setSelectedProducts(selectedOptions);
    };

    const handleAddProduct = async (e) => {
        e.preventDefault();

        const token = localStorage.getItem('access_token');
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
                    'User_id': user_id
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                alert('Product added successfully!');
                setNewProductName('');
                setNewProductUnit('');
                onProductsUpdated(); // Odśwież listę produktów
            } else {
                throw new Error('Failed to add new product');
            }
        } catch (error) {
            console.error('Error adding new product:', error);
            alert('Failed to add new product.');
        }
    };

    const handleAddMeal = async (e) => {
        e.preventDefault();

        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');

        const payload = {
            name: mealName,
            description: mealDescription,
            product_ids: selectedProducts.map(Number),
            category_ids: selectedCategories.map(Number),
            preparation: mealPreparation,
            user_id: Number(user_id),
        };

        try {
            const response = await fetch('http://localhost:8000/meals', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                    'User_id': user_id
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                alert('Meal added successfully!');
                onMealsRefresh();
                onClose(); // Zamknij modal
            } else {
                throw new Error('Failed to add new meal');
            }
        } catch (error) {
            console.error('Error adding new meal:', error);
            alert('Failed to add new meal.');
        }
    };

    return (
        <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
            <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
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
                <h3>Add New Meal</h3>
                <form onSubmit={handleAddMeal}>
                    <input
                        type="text"
                        placeholder="Name"
                        value={mealName}
                        onChange={(e) => setMealName(e.target.value)}
                    />
                    <textarea
                        placeholder="Description"
                        value={mealDescription}
                        onChange={(e) => setMealDescription(e.target.value)}
                    />
                    <textarea
                        placeholder="Preparation"
                        value={mealPreparation}
                        onChange={(e) => setMealPreparation(e.target.value)}
                    />
                    <select multiple value={selectedCategories} onChange={handleCategoryChange}>
                        {categories.map((category) => (
                            <option key={category.id} value={category.id}>
                                {category.name}
                            </option>
                        ))}
                    </select>
                    <select multiple value={selectedProducts} onChange={handleProductChange}>
                        {products.map((product) => (
                            <option key={product.id} value={product.id}>
                                {product.name}
                            </option>
                        ))}
                    </select>
                    <button type="submit">Submit</button>
                    <button onClick={onClose}>Close</button>
                </form>
                
            </div>
        </div>
    );
}

export default AddMealModal;
