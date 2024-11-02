import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [transcription, setTranscription] = useState('');
  const [translation, setTranslation] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTranscription = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5001/transcribe');
      setTranscription(response.data.transcription);
    } catch (error) {
      console.error('Error during transcription:', error);
      alert('Transcription failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleTranslation = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5001/translate', {
        text: transcription,
      });
      setTranslation(response.data.translation);
    } catch (error) {
      console.error('Error during translation:', error);
      alert('Translation failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleSummary = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5001/summarize', {
        text: translation,
      });
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error during summarization:', error);
      alert('Summarization failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Hello, LinguaText!</h1>
      <button onClick={handleTranscription} disabled={loading}>
        {loading ? 'Processing...' : '文字起こし'}
      </button>
      <button onClick={handleTranslation} disabled={!transcription || loading}>
        {loading ? 'Processing...' : '翻訳'}
      </button>
      <button onClick={handleSummary} disabled={!translation || loading}>
        {loading ? 'Processing...' : '要約'}
      </button>

      <div>
        <h2>文字起こし:</h2>
        <p>{transcription}</p>
      </div>
      <div>
        <h2>翻訳:</h2>
        <p>{translation}</p>
      </div>
      <div>
        <h2>要約:</h2>
        <p>{summary}</p>
      </div>
    </div>
  );
}

export default App;
