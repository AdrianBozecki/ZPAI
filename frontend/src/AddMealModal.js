import React, { useState } from 'react';
import styles from './AddMealModal.module.css';

function AddMealModal({ onClose, categories, onMealsRefresh}) {
    const unitsOfMeasure = ['GRAM', 'KILOGRAM', 'MILLILITER', 'LITER', 'PIECE', 'OUNCE', 'POUND', 'PINT', 'QUART', 'GALLON', 'TEASPOON', 'TABLESPOON', 'CUP'];

    const [selectedCategories, setSelectedCategories] = useState([]);
    const [selectedProducts, setSelectedProducts] = useState([{ name: '', value: '', unit_of_measure: unitsOfMeasure[0] }]);
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

    const handleProductChange = (index, field, event) => {
        const newProducts = [...selectedProducts];
        newProducts[index][field] = event.target.value;
        setSelectedProducts(newProducts);
    };

    const addProduct = () => {
        setSelectedProducts([...selectedProducts, { name: '', value: '', unit_of_measure: '' }]);
    };

    const handleAddMeal = async (e) => {
        e.preventDefault();

        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');

        const payload = {
            name: mealName,
            description: mealDescription,
            products: selectedProducts,
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
    const removeProduct = (index) => {
    const newProducts = [...selectedProducts];
    newProducts.splice(index, 1);
    setSelectedProducts(newProducts);
};

    return (
        <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
            <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
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
                    {selectedProducts.map((product, index) => (
    <div key={index} style={{ display: 'flex', alignItems: 'center' }}>
        <input
            type="text"
            placeholder="Product Name"
            value={product.name}
            onChange={(e) => handleProductChange(index, 'name', e)}
        />
        <input
            type="number"
            placeholder="Value"
            value={product.value}
            onChange={(e) => handleProductChange(index, 'value', e)}
        />
        <select
            value={product.unit_of_measure}
            onChange={(e) => handleProductChange(index, 'unit_of_measure', e)}
        >
            {unitsOfMeasure.map((unit) => (
                <option key={unit} value={unit}>
                    {unit}
                </option>
            ))}
        </select>
        <button type="button" onClick={() => removeProduct(index)} style={{ marginLeft: '10px' }}>-</button>
    </div>
))}
        <button type="button" onClick={addProduct}>Add next product</button>
                    <button type="submit">Submit</button>
                    <button onClick={onClose}>Close</button>
                </form>
            </div>
        </div>
    );
}

export default AddMealModal;