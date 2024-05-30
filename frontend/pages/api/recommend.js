export default async (req, res) => {
    const response = await fetch('http://localhost:8000/recommend', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: req.body.user_id,
      }),
    });
  
    const data = await response.json();
    res.status(200).json(data);
  };
  