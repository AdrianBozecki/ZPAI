import React, { useState, useEffect } from 'react';
import styles from './AddMealModal.module.css';

function AddMealModal({ mealToAdd, onClose, categories, onMealsRefresh }) {
    const unitsOfMeasure = ['GRAM', 'KILOGRAM', 'MILLILITER', 'LITER', 'PIECE', 'OUNCE', 'POUND', 'PINT', 'QUART', 'GALLON', 'TEASPOON', 'TABLESPOON', 'CUP'];

    const [selectedCategories, setSelectedCategories] = useState([]);
    const [selectedProducts, setSelectedProducts] = useState(mealToAdd ? mealToAdd.products : [{ name: '', value: '', unit_of_measure: unitsOfMeasure[0] }]);
    const [mealName, setMealName] = useState(mealToAdd ? mealToAdd.name : '');
    const [mealDescription, setMealDescription] = useState(mealToAdd ? mealToAdd.description : '');
    const [mealPreparation, setMealPreparation] = useState(mealToAdd ? mealToAdd.preparation : '');
    const [mealImage, setMealImage] = useState(mealToAdd ? mealToAdd.image : null);

    useEffect(() => {
        if (mealToAdd && mealToAdd.image) {
            setMealImage(mealToAdd.image);
        }
    }, [mealToAdd]);

    const handleBackdropClick = (event) => {
        if (event.target === event.currentTarget) {
            onClose();
        }
    };

    const handleCategoryChange = (event) => {
        const selectedOptions = Array.from(event.target.selectedOptions).map(option => option.value);
        setSelectedCategories(selectedOptions);
    };

    const handleProductChange = (index, field, event) => {
        const newProducts = [...selectedProducts];
        newProducts[index][field] = event.target.value;
        setSelectedProducts(newProducts);
    };

    const addProduct = () => {
        setSelectedProducts([...selectedProducts, { name: '', value: '', unit_of_measure: '' }]);
    };

    function logRequestResponse(url, options, response) {
        console.log('Request URL:', url);
        console.log('Request Options:', options);
        console.log('Response Status:', response.status);
        response.clone().json().then(data => {
            console.log('Response Body:', data);
        }).catch(() => {
            response.clone().text().then(data => {
                console.log('Response Body:', data);
            });
        });
    }

    const handleAddMeal = async (e) => {
        e.preventDefault();

        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');

        const payload = new FormData();
        payload.append('name', mealName);
        payload.append('description', mealDescription);
        payload.append('preparation', mealPreparation);
        payload.append('user_id', user_id);
        payload.append('category_ids', JSON.stringify(selectedCategories.map(Number)));
        payload.append('products', JSON.stringify(selectedProducts));
        if (mealImage) {
            payload.append('image', mealImage);
        }

        console.log('meal.image:', mealImage); // Add this line to log meal.image

        const options = {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: payload,
        };

        try {
            const response = await fetch('http://localhost:8000/meals', options);
            logRequestResponse('http://localhost:8000/meals', options, response);

            if (response.ok) {
                alert('Meal added successfully!');
                onMealsRefresh();
                onClose();
            } else {
                throw new Error('Failed to add new meal');
            }
        } catch (error) {
            console.error('Error adding new meal:', error);
            alert('Failed to add new meal.');
        }
    };

    const removeProduct = (index) => {
        const newProducts = [...selectedProducts];
        newProducts.splice(index, 1);
        setSelectedProducts(newProducts);
    };

    return (
        <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
            <div className={styles.modalContent}>
                <h2>Add Meal</h2>
                <form onSubmit={handleAddMeal}>
                    <label>
                        Name:
                        <input type="text" value={mealName} onChange={(e) => setMealName(e.target.value)} required/>
                    </label>
                    <label>
                        Description:
                        <textarea value={mealDescription} onChange={(e) => setMealDescription(e.target.value)}
                                  required/>
                    </label>
                    <label>
                        Preparation:
                        <textarea value={mealPreparation} onChange={(e) => setMealPreparation(e.target.value)}
                                  required/>
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
                            <div key={index}>
                                <input type="text" value={product.name}
                                       onChange={(e) => handleProductChange(index, 'name', e)}
                                       placeholder="Product Name" required/>
                                <input type="number" value={product.value}
                                       onChange={(e) => handleProductChange(index, 'value', e)} placeholder="Value"
                                       required/>
                                <select value={product.unit_of_measure}
                                        onChange={(e) => handleProductChange(index, 'unit_of_measure', e)}>
                                    {unitsOfMeasure.map(unit => (
                                        <option key={unit} value={unit}>{unit}</option>
                                    ))}
                                </select>
                                <button type="button" onClick={() => removeProduct(index)}>Remove</button>
                            </div>
                        ))}
                        <button type="button" onClick={addProduct}>Add next product</button>
                    </label>
                    <label>
                        Image:
                        <input type="file" onChange={(e) => setMealImage(e.target.files[0])}/>
                        {mealImage && typeof mealImage === 'string' && (
                            <img src={mealImage} alt="Meal" style={{ width: '100px', height: '100px', marginTop: '10px' }} />
                        )}
                    </label>
                    <button type="submit">Add Meal</button>
                </form>
                <button className={styles.fullWidthNavyButton} onClick={onClose}>Close</button>
            </div>
        </div>
    );
}

export default AddMealModal;