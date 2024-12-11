// frontend/src/utils.js

// Function to refresh the token
async function refreshToken() {
  const refresh_token = localStorage.getItem('refresh_token');
  const response = await fetch('http://localhost:8000/users/refresh-token/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token }),
  });

  if (!response.ok) {
    throw new Error('Failed to refresh token');
  }

  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  return data.access_token;
}

// General function to make requests with retry logic
export async function makeRequest(url, options = {}) {
  const token = localStorage.getItem('access_token');
  options.headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  let response = await fetch(url, options);

  if (response.status === 401) {
    try {
      const newToken = await refreshToken();
      options.headers['Authorization'] = `Bearer ${newToken}`;
      response = await fetch(url, options);
    } catch (error) {
      console.error('Failed to refresh token', error);
      throw error;
    }
  }

  return response;
}