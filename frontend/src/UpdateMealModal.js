import React, { useState, useEffect } from 'react';
import styles from './AddMealModal.module.css';
import { makeRequest } from './utils'; // Adjust the import path as needed

function UpdateMealModal({ mealToUpdate, onClose, categories, onMealsRefresh }) {
    const unitsOfMeasure = ['GRAM', 'KILOGRAM', 'MILLILITER', 'LITER', 'PIECE', 'OUNCE', 'POUND', 'PINT', 'QUART', 'GALLON', 'TEASPOON', 'TABLESPOON', 'CUP'];

    const [mealName, setMealName] = useState(mealToUpdate ? mealToUpdate.name : '');
    const [mealDescription, setMealDescription] = useState(mealToUpdate ? mealToUpdate.description : '');
    const [mealPreparation, setMealPreparation] = useState(mealToUpdate ? mealToUpdate.preparation : '');
    const [selectedProducts, setSelectedProducts] = useState(mealToUpdate ? JSON.parse(JSON.stringify(mealToUpdate.products)) : []);
    const [selectedCategories, setSelectedCategories] = useState(mealToUpdate ? mealToUpdate.categories : []);

    useEffect(() => {
        if (mealToUpdate) {
            setSelectedCategories(mealToUpdate.category_ids);
            setSelectedProducts(mealToUpdate.products);
            setMealName(mealToUpdate.name);
            setMealDescription(mealToUpdate.description);
            setMealPreparation(mealToUpdate.preparation);
        }
    }, [mealToUpdate]);

    const handleBackdropClick = (event) => {
        if (event.target === event.currentTarget) {
            onClose();
        }
    };

    const handleCategoryChange = (event) => {
        const categoryId = parseInt(event.target.value);
        if (selectedCategories.includes(categoryId)) {
            setSelectedCategories(selectedCategories.filter(id => id !== categoryId));
        } else {
            setSelectedCategories([...selectedCategories, categoryId]);
        }
    };

    const handleProductChange = (index, field, event) => {
        const newProducts = [...selectedProducts];
        const product = { ...newProducts[index] }; // Create a new object
        product[field] = event.target.value; // Update the value in the new object
        newProducts[index] = product; // Replace the old product with the new one
        setSelectedProducts(newProducts);
    };

    const addProduct = () => {
        setSelectedProducts([...selectedProducts, { name: '', value: '', unit_of_measure: unitsOfMeasure[0] }]);
    };

    const removeProduct = (index) => {
        const newProducts = [...selectedProducts];
        newProducts.splice(index, 1);
        setSelectedProducts(newProducts);
    };

    const handleUpdateMeal = async (e) => {
        e.preventDefault();

        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');

        const payload = {};

        if (mealName !== mealToUpdate.name) payload.name = mealName;
        if (mealDescription !== mealToUpdate.description) payload.description = mealDescription;
        if (mealPreparation !== mealToUpdate.preparation) payload.preparation = mealPreparation;
        if (JSON.stringify(selectedProducts) !== JSON.stringify(mealToUpdate.products)) payload.products = selectedProducts;
        if (JSON.stringify(selectedCategories) !== JSON.stringify(mealToUpdate.category_ids)) payload.category_ids = selectedCategories;

        if (Object.keys(payload).length === 0) {
            alert('No changes were made.');
            return;
        }

        try {
            const response = await makeRequest(`http://localhost:8000/meals/${mealToUpdate.id}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                alert('Meal updated successfully!');
                onMealsRefresh();
                onClose();
            } else {
                throw new Error('Failed to update meal');
            }
        } catch (error) {
            console.error('There was an error updating the meal:', error);
            alert('There was an error updating the meal.');
        }
    };

    return (
        <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
            <div className={styles.modalContent}>
                <h2>Update Meal</h2>
                <form onSubmit={handleUpdateMeal}>
                    <label>
                        Name:
                        <input type="text" value={mealName} onChange={(e) => setMealName(e.target.value)} required/>
                    </label>
                    <label>
                        Description:
                        <textarea value={mealDescription} onChange={(e) => setMealDescription(e.target.value)} required/>
                    </label>
                    <label>
                        Preparation:
                        <textarea value={mealPreparation} onChange={(e) => setMealPreparation(e.target.value)} required/>
                    </label>
                    <label>
                        Categories:
                        <select multiple value={selectedCategories} onChange={handleCategoryChange}>
                            {categories.map(category => (
                                <option key={category.id} value={category.id}>{category.name}</option>
                            ))}
                        </select>
                    </label>
                    <label>
                        Products:
                        {selectedProducts.map((product, index) => (
                            <div key={index} style={{ display: 'flex', alignItems: 'center' }}>
                                <input type="text" value={product.name} onChange={(e) => handleProductChange(index, 'name', e)} placeholder="Product Name" required/>
                                <input type="number" value={product.value} onChange={(e) => handleProductChange(index, 'value', e)} placeholder="Value" required/>
                                <select value={product.unit_of_measure} onChange={(e) => handleProductChange(index, 'unit_of_measure', e)}>
                                    {unitsOfMeasure.map(unit => (
                                        <option key={unit} value={unit}>{unit}</option>
                                    ))}
                                </select>
                                <button type="button" onClick={() => removeProduct(index)}>Remove</button>
                            </div>
                        ))}
                        <button type="button" onClick={addProduct}>Add next product</button>
                    </label>
                    <button type="submit">Update Meal</button>
                </form>
                <button className={styles.fullWidthNavyButton} onClick={onClose}>Close</button>
            </div>
        </div>
    );
}

export default UpdateMealModal;