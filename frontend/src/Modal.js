import styles from './DashboardPage.module.css';
function Modal({ meal, onClose }) {
    return (
      <div className={styles.modalBackdrop}>
        <div className={styles.modalContent}>
          <h2>name: {meal.name}</h2>
          <p>description: {meal.description}</p>
          <p>preparation:{meal.preparation}</p>
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    );
  }
  
  export default Modal;
  