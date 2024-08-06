import React, { useState, useEffect } from 'react';
import styles from './AddMealModal.module.css';

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
    const product = { ...newProducts[index] }; // Tworzymy nowy obiekt
    product[field] = event.target.value; // Aktualizujemy wartość w nowym obiekcie
    newProducts[index] = product; // Zastępujemy stary produkt nowym
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
    console.log(JSON.stringify(selectedProducts), JSON.stringify(mealToUpdate.products));
    if (JSON.stringify(selectedProducts) !== JSON.stringify(mealToUpdate.products)) payload.products = selectedProducts;
    if (JSON.stringify(selectedCategories) !== JSON.stringify(mealToUpdate.category_ids)) payload.category_ids = selectedCategories;

    if (Object.keys(payload).length === 0) {
        alert('No changes were made.');
        return;
    }

    try {
        console.log('Updating meal:', payload);
        const response = await fetch(`http://localhost:8000/meals/${mealToUpdate.id}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
                'User_id': user_id,
            },
            body: JSON.stringify(payload),
        });

        if (response.ok) {
            console.log(`Meal with id: ${mealToUpdate.id} was updated.`);
            onMealsRefresh();
            onClose();
        } else {
            console.error('Failed to update the meal.');
            console.log(response);
            alert('Failed to update the meal.');
        }
    } catch (error) {
        console.error('There was an error updating the meal:', error);
        alert('There was an error updating the meal.');
    }
};

    return (
        <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
            <div className={styles.modalContent} onClick={e => e.stopPropagation()}>
                <h3>Update Meal</h3>
                <form onSubmit={handleUpdateMeal}>
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

export default UpdateMealModal;