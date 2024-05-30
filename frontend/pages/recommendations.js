import { useState } from 'react';

const Recommendations = () => {
  const [userId, setUserId] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const fetchRecommendations = async () => {
    const response = await fetch('/api/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: userId }),
    });

    const data = await response.json();
    setRecommendations(data.recommendations);
  };

  return (
    <div>
      <h1>Your Beer Recommendations</h1>
      <input 
        type="text" 
        placeholder="Enter your user ID" 
        value={userId} 
        onChange={(e) => setUserId(e.target.value)} 
      />
      <button onClick={fetchRecommendations}>Get Recommendations</button>
      <ul>
        {recommendations.map(beer => (
          <li key={beer.beer_id}>
            <h2>{beer.name}</h2>
            <p>{beer.description}</p>
            <p><strong>Why this beer?</strong> {beer.recommendation_reason}</p>
            <p><strong>Feature1:</strong> {beer.feature1}</p>
            <p><strong>Feature2:</strong> {beer.feature2}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Recommendations;
