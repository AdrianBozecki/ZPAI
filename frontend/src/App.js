import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Odpowiedź z backendu zostanie zapisana w stanie 'data'
    axios.get('http://localhost:8000/test_router/')
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Błąd podczas pobierania danych:", error);
      });
  }, []); // Pusty tablicę zależności oznacza, że żądanie będzie wykonane tylko raz, gdy komponent zostanie zamontowany

  return (
    <div className="App">
      <header className="App-header">
        {data ? (
          <div>
            <p>Dane z backendu:</p>
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </div>
        ) : (
          <p>Ładowanie danych...</p>
        )}
      </header>
    </div>
  );
}

export default App;
