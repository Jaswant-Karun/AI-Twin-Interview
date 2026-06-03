import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import toast from 'react-hot-toast';

export default function Results() {
  const router = useRouter();
  const { interviewId } = router.query;
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (interviewId) {
      fetchResults();
    }
  }, [interviewId]);

  const fetchResults = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/evaluations/${interviewId}/summary`
      );
      setResult(response.data);
    } catch (error) {
      toast.error('Failed to load results');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <p className="text-xl text-gray-700">Loading results...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-purple-700 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white text-center mb-8">
          Interview Complete! 🎉
        </h1>

        {result && (
          <div className="space-y-6">
            {/* Overall Score */}
            <div className="bg-white rounded-lg shadow-xl p-8 text-center">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">Overall Score</h2>
              <p className="text-6xl font-bold text-blue-600 mb-2">
                {result.overall_score.toFixed(1)}
              </p>
              <p className="text-gray-600">out of 100</p>
            </div>

            {/* Strengths */}
            <div className="bg-white rounded-lg shadow-xl p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">💪 Strengths</h2>
              <ul className="space-y-2 text-gray-700">
                {JSON.parse(result.strengths).map((strength, i) => (
                  <li key={i} className="flex items-center">
                    <span className="text-green-600 mr-3">✓</span> {strength}
                  </li>
                ))}
              </ul>
            </div>

            {/* Weaknesses */}
            <div className="bg-white rounded-lg shadow-xl p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">📍 Areas to Improve</h2>
              <ul className="space-y-2 text-gray-700">
                {JSON.parse(result.weaknesses).map((weakness, i) => (
                  <li key={i} className="flex items-center">
                    <span className="text-yellow-600 mr-3">!</span> {weakness}
                  </li>
                ))}
              </ul>
            </div>

            {/* Improvement Roadmap */}
            <div className="bg-white rounded-lg shadow-xl p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">🗺️ Improvement Roadmap</h2>
              <div className="space-y-3 text-gray-700">
                {Object.entries(JSON.parse(result.improvement_roadmap)).map(([key, value]) => (
                  <div key={key} className="border-l-4 border-blue-600 pl-4">
                    <p className="font-semibold">{key}: {value}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => router.push('/')}
                className="px-8 py-3 bg-white text-blue-600 rounded-lg font-bold hover:bg-gray-100"
              >
                Take Another Interview
              </button>
              <button
                onClick={() => window.print()}
                className="px-8 py-3 bg-blue-600 text-white rounded-lg font-bold hover:bg-blue-700"
              >
                Download Results
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
