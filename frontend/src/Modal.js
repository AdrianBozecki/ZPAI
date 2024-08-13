import React, { useState, useEffect } from 'react';
import styles from './Modal.module.css';
import UpdateMealModal from "./UpdateMealModal";

function Modal({ meal, onEdit, onClose, categories, onMealsRefresh }) {
    const localUserId = localStorage.getItem('user_id');
    const [unitSystem, setUnitSystem] = useState('METRIC');
    const [commentContent, setCommentContent] = useState('');
    const [comments, setComments] = useState([]);
    const [likesCount, setLikesCount] = useState(meal.likes_count);
    const [userLiked, setUserLiked] = useState(false);

    useEffect(() => {
        const fetchComments = async () => {
            try {
                const response = await fetch(`http://localhost:8000/comments?meal_id=${meal.id}`);
                if (response.ok) {
                    const data = await response.json();
                    setComments(data);
                } else {
                    console.error('Failed to fetch comments');
                }
            } catch (error) {
                console.error('Error fetching comments:', error);
            }
        };

        const checkUserLiked = () => {
            const likedBy = meal.liked_by || [];
            setUserLiked(likedBy.includes(Number(localUserId)));
        };

        fetchComments();
        checkUserLiked();
    }, [meal.id, localUserId, meal.liked_by]);

    const handleBackdropClick = (event) => {
        if (event.target === event.currentTarget) {
            onClose();
        }
    };

    const handleEdit = () => {
        onEdit(meal);
        onClose();
    };

    const handleDelete = async () => {
        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');

        if (meal.user_id.toString() === user_id) {
            try {
                const response = await fetch(`http://localhost:8000/meals/${meal.id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });

                if (response.ok) {
                    alert('Meal deleted successfully!');
                    onMealsRefresh();
                    onClose();
                } else {
                    throw new Error('Failed to delete meal');
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

    const handleAddComment = async () => {
        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');

        const payload = {
            content: commentContent,
            user_id: Number(user_id),
            meal_id: meal.id,
        };

        try {
            const response = await fetch('http://localhost:8000/comments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                const newComment = await response.json();
                setComments([...comments, newComment]);
                setCommentContent('');
            } else {
                throw new Error('Failed to add comment');
            }
        } catch (error) {
            console.error('Error adding comment:', error);
            alert('Failed to add comment.');
        }
    };

    const handleLike = async () => {
        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');

        try {
            const response = await fetch('http://localhost:8000/likes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ user_id: Number(user_id), meal_id: meal.id }),
            });

            if (response.ok) {
                setLikesCount(likesCount + 1);
                setUserLiked(true);
            } else {
                throw new Error('Failed to like meal');
            }
        } catch (error) {
            console.error('Error liking meal:', error);
            alert('Failed to like meal.');
        }
    };

    const handleUnlike = async () => {
        const token = localStorage.getItem('access_token');
        const user_id = localStorage.getItem('user_id');

        try {
            const response = await fetch(`http://localhost:8000/likes/${user_id}/${meal.id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                setLikesCount(likesCount - 1);
                setUserLiked(false);
            } else {
                throw new Error('Failed to unlike meal');
            }
        } catch (error) {
            console.error('Error unliking meal:', error);
            alert('Failed to unlike meal.');
        }
    };

    const categoryNames = getCategoryNames(meal.category_ids);

    return (
        <div className={styles.modalBackdrop} onClick={handleBackdropClick}>
            <div className={styles.modalContent}>
                <h2>{meal.name}</h2>
                <img src={meal.image_url || "/img/placeholder.png"} alt="Meal"/>
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
                {localUserId === meal.user_id.toString() && (
                    <button onClick={handleEdit}>Edit</button>
                )}
                <div className={styles.commentSection}>
                    <input
                        type="text"
                        placeholder="Add a comment"
                        value={commentContent}
                        onChange={(e) => setCommentContent(e.target.value)}
                    />
                    <button onClick={handleAddComment}>Add</button>
                </div>
                <div className={styles.commentsList}>
                    {comments.map(comment => (
                        <div key={comment.id} className={styles.comment}>
                            <p><b>{comment.user.name} {comment.user.lastname}:</b> {comment.content}</p>
                            <p><i>{new Date(comment.created_at).toLocaleString()}</i></p>
                        </div>
                    ))}
                </div>
                <div className={styles.likesSection}>
                    <p><b>Likes:</b> {likesCount}</p>
                    {userLiked ? (
                        <button onClick={handleUnlike}>Unlike</button>
                    ) : (
                        <button onClick={handleLike}>Like</button>
                    )}
                </div>
                <button onClick={onClose}>Close</button>
            </div>
        </div>
    );
}

export default Modal;