import React, { useState, useRef } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

export default function QuestionCard({ question, interviewId, onAnswerSubmit, isLoading }) {
  const [answer, setAnswer] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef(null);

  const startVoiceRecording = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      toast.error('Speech recognition not supported');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.onstart = () => setIsRecording(true);
    recognition.onend = () => setIsRecording(false);
    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(result => result[0].transcript)
        .join('');
      setAnswer(transcript);
    };

    recognition.start();
    recognitionRef.current = recognition;
  };

  const stopVoiceRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  const handleSubmit = async () => {
    if (!answer.trim()) {
      toast.error('Please provide an answer');
      return;
    }

    await onAnswerSubmit(answer);
    setAnswer('');
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl w-full">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        {question.question_text}
      </h2>

      <div className="mb-6">
        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type your answer or click the microphone to speak..."
          className="w-full h-32 p-4 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-600"
        />
      </div>

      <div className="flex gap-4">
        <button
          onClick={isRecording ? stopVoiceRecording : startVoiceRecording}
          className={`flex-1 py-3 rounded-lg font-bold text-white transition-all ${
            isRecording ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'
          }`}
        >
          {isRecording ? 'Stop Recording' : 'Start Recording'}
        </button>
        
        <button
          onClick={handleSubmit}
          disabled={isLoading}
          className={`flex-1 py-3 rounded-lg font-bold text-white transition-all ${
            isLoading ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {isLoading ? 'Evaluating...' : 'Submit Answer'}
        </button>
      </div>
    </div>
  );
}
