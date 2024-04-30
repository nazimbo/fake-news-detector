const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

app.post('/scrape', async (req, res) => {
  const url = req.body.url;
  try {
    const response = await axios.get(url);
    const $ = cheerio.load(response.data);
    const bodyContent = $('body').html();
    res.json({ body: bodyContent });
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
